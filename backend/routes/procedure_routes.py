import os
import uuid
import io
from datetime import datetime

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Procedure, db
from backend.routes.admin_routes import admin_required

procedure_routes = Blueprint('procedure_routes', __name__)

# ─── Path/SFTP helpers ─────────────────────────────────────────────────────────

FLASK_ENV = os.getenv("FLASK_ENV", "development")
VPS_BASE_PATH = os.getenv("VPS_BASE_PATH", "/tmp/uploads")
VPS_PUBLIC_URL_BASE = os.getenv("VPS_PUBLIC_URL_BASE", "http://localhost:5000/uploads")


def _get_sftp():
    """Return an (ssh, sftp) tuple for the VPS (used only in dev mode)."""
    import paramiko  # lazy import — only needed in dev mode
    host = os.getenv("VPS_HOST", "31.220.85.103")
    port = int(os.getenv("VPS_PORT", "22"))
    user = os.getenv("VPS_USER", "root")
    password = os.getenv("VPS_SSH_PASSWORD", None)
    key_path = os.getenv("VPS_SSH_KEY_PATH", None)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if key_path:
        ssh.connect(host, port=port, username=user, key_filename=key_path)
    else:
        ssh.connect(host, port=port, username=user, password=password)

    sftp = ssh.open_sftp()
    return ssh, sftp


def _ensure_remote_dir(sftp):
    """Make sure the remote upload directory exists."""
    parts = VPS_BASE_PATH.split("/")
    current = ""
    for part in parts:
        if not part:
            continue
        current += "/" + part
        try:
            sftp.stat(current)
        except FileNotFoundError:
            sftp.mkdir(current)


def save_file_to_vps(file_storage, filename):
    """
    Save an uploaded file to the VPS.
    - PROD: the Flask process runs ON the VPS → write directly.
    - DEV:  the Flask process runs locally → use SFTP to write to VPS.
    Returns the full remote path.
    """
    remote_path = os.path.join(VPS_BASE_PATH, filename).replace("\\", "/")

    if FLASK_ENV == "production":
        os.makedirs(VPS_BASE_PATH, exist_ok=True)
        file_storage.save(remote_path)
    else:
        ssh, sftp = _get_sftp()
        try:
            _ensure_remote_dir(sftp)
            file_bytes = file_storage.read()
            with sftp.open(remote_path, "wb") as remote_file:
                remote_file.write(file_bytes)
        finally:
            sftp.close()
            ssh.close()

    return remote_path


def delete_file_from_vps(filename):
    """Delete a file from the VPS upload folder."""
    remote_path = os.path.join(VPS_BASE_PATH, filename).replace("\\", "/")

    if FLASK_ENV == "production":
        try:
            os.remove(remote_path)
        except FileNotFoundError:
            pass
    else:
        try:
            ssh, sftp = _get_sftp()
            try:
                sftp.remove(remote_path)
            except FileNotFoundError:
                pass
            finally:
                sftp.close()
                ssh.close()
        except Exception:
            pass  # Don't block deletion if SFTP fails


def read_file_from_vps(filename):
    """Return file bytes from the VPS upload folder (for streaming in dev)."""
    remote_path = os.path.join(VPS_BASE_PATH, filename).replace("\\", "/")

    if FLASK_ENV == "production":
        with open(remote_path, "rb") as f:
            return f.read()
    else:
        ssh, sftp = _get_sftp()
        try:
            with sftp.open(remote_path, "rb") as remote_file:
                return remote_file.read()
        finally:
            sftp.close()
            ssh.close()


# ─── Routes ────────────────────────────────────────────────────────────────────

################################ LIST ##########################################
@procedure_routes.route('/api/procedures', methods=['GET'])
@jwt_required()
@admin_required
def list_procedures():
    procedures = Procedure.query.order_by(Procedure.created_at.desc()).all()
    result = []
    for p in procedures:
        d = p.as_dict()
        d['file_url'] = f"{VPS_PUBLIC_URL_BASE}/{p.filename}"
        result.append(d)
    return jsonify(result), 200
################################################################################


################################ CREATE ########################################
@procedure_routes.route('/api/procedures', methods=['POST'])
@jwt_required()
@admin_required
def create_procedure():
    nome = request.form.get('nome', '').strip()
    file = request.files.get('file')

    if not nome:
        return jsonify({'error': 'O campo "nome" é obrigatório.'}), 400
    if not file or file.filename == '':
        return jsonify({'error': 'Um arquivo é obrigatório.'}), 400

    original_filename = file.filename
    ext = os.path.splitext(original_filename)[1].lower()
    safe_filename = f"{uuid.uuid4().hex}{ext}"

    try:
        save_file_to_vps(file, safe_filename)
    except Exception as e:
        return jsonify({'error': f'Erro ao salvar arquivo na VPS: {str(e)}'}), 500

    user_id = int(get_jwt_identity())
    procedure = Procedure(
        nome=nome,
        filename=safe_filename,
        original_filename=original_filename,
        created_by=user_id,
    )
    db.session.add(procedure)
    db.session.commit()

    d = procedure.as_dict()
    d['file_url'] = f"{VPS_PUBLIC_URL_BASE}/{safe_filename}"
    return jsonify({'message': 'Procedimento criado com sucesso!', 'procedure': d}), 201
################################################################################


################################ UPDATE ########################################
@procedure_routes.route('/api/procedures/<int:procedure_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_procedure(procedure_id):
    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return jsonify({'error': 'Procedimento não encontrado.'}), 404

    nome = request.form.get('nome', '').strip()
    file = request.files.get('file')

    if nome:
        procedure.nome = nome

    if file and file.filename != '':
        # Delete old file, upload new one
        old_filename = procedure.filename
        original_filename = file.filename
        ext = os.path.splitext(original_filename)[1].lower()
        safe_filename = f"{uuid.uuid4().hex}{ext}"

        try:
            save_file_to_vps(file, safe_filename)
        except Exception as e:
            return jsonify({'error': f'Erro ao salvar novo arquivo na VPS: {str(e)}'}), 500

        delete_file_from_vps(old_filename)

        procedure.filename = safe_filename
        procedure.original_filename = original_filename

    procedure.updated_at = datetime.utcnow()
    db.session.commit()

    d = procedure.as_dict()
    d['file_url'] = f"{VPS_PUBLIC_URL_BASE}/{procedure.filename}"
    return jsonify({'message': 'Procedimento atualizado com sucesso!', 'procedure': d}), 200
################################################################################


################################ DELETE ########################################
@procedure_routes.route('/api/procedures/<int:procedure_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_procedure(procedure_id):
    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return jsonify({'error': 'Procedimento não encontrado.'}), 404

    filename = procedure.filename
    db.session.delete(procedure)
    db.session.commit()

    delete_file_from_vps(filename)

    return jsonify({'message': 'Procedimento excluído com sucesso!'}), 200
################################################################################


################################ STREAM FILE ###################################
@procedure_routes.route('/api/procedures/<int:procedure_id>/file', methods=['GET'])
@jwt_required()
@admin_required
def stream_procedure_file(procedure_id):
    """Stream the file bytes — useful for dev where the file lives on the VPS."""
    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return jsonify({'error': 'Procedimento não encontrado.'}), 404

    try:
        data = read_file_from_vps(procedure.filename)
    except Exception as e:
        return jsonify({'error': f'Erro ao ler arquivo da VPS: {str(e)}'}), 500

    return send_file(
        io.BytesIO(data),
        download_name=procedure.original_filename,
        as_attachment=False,
    )
################################################################################
