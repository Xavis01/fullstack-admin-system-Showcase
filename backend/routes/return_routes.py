from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.models import Return, Sale, Production, db, Client, registrar_movimentacao
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.routes.admin_routes import admin_required

return_routes = Blueprint('return_routes', __name__)

###################################### CREATE - Criar devolução #####################################
@return_routes.route('/api/returns', methods=['POST'])
@jwt_required()
@admin_required
def create_return():
    data = request.get_json()
    sale_id = data.get('sale_id')
    quant_devolvida = data.get('quant_devolvida')
    observacao = data.get('observacao')

    if not sale_id or not quant_devolvida:
        return jsonify({'error': 'Campos obrigatórios: sale_id, quant_devolvida'}), 400

    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({'error': 'Venda não encontrada.'}), 404

    try:
        quant_devolvida = int(quant_devolvida)
        
        # Validar se a quantidade devolvida é válida
        if quant_devolvida <= 0:
            return jsonify({'error': 'Quantidade devolvida deve ser maior que zero.'}), 400
            
        if quant_devolvida > sale.quant_caixa_vendida:
            return jsonify({'error': f'Quantidade devolvida ({quant_devolvida}) não pode ser maior que a quantidade vendida ({sale.quant_caixa_vendida}).'}), 400

        # Subtrai da venda (Stand By logic: sai da venda, mas não volta pro estoque ainda)
        sale.quant_caixa_vendida -= quant_devolvida
        
        # Cria o registro de devolução
        new_return = Return(
            sale_id=sale_id,
            num_lote_origem=sale.num_lote,
            quant_devolvida=quant_devolvida,
            observacao=observacao,
            status='Aberto'
        )
        
        db.session.add(new_return)
        db.session.commit()
        
        return jsonify({'message': 'Devolução registrada com sucesso!', 'return': new_return.as_dict()}), 201

    except ValueError:
        return jsonify({'error': 'Quantidade inválida.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao registrar devolução: {str(e)}'}), 500
#####################################################################################################

###################################### READ - Listar devoluções #####################################
@return_routes.route('/api/returns', methods=['GET'])
@jwt_required()
@admin_required
def get_returns():
    from sqlalchemy.orm import joinedload
    
    # Eager load Sale, Client, and Product to avoid N+1 queries
    query = Return.query.options(
        joinedload(Return.sale).joinedload(Sale.client),
        joinedload(Return.sale).joinedload(Sale.product)
    )
    
    # Filtros
    status = request.args.get('status')
    client_id = request.args.get('client_id')
    num_lote = request.args.get('num_lote')
    product_id = request.args.get('product_id')
    
    if status:
        query = query.filter(Return.status == status)
    
    if num_lote:
        # Filtra tanto pelo lote de origem quanto pelo novo lote
        from sqlalchemy import or_
        query = query.filter(or_(Return.num_lote_origem.ilike(f'%{num_lote}%'), Return.novo_lote_id.ilike(f'%{num_lote}%')))
        
    if client_id:
        query = query.join(Sale).filter(Sale.client_id == client_id)

    if product_id:
        # If we refer to Sale properties in filter without joining, SQLAlchemy might error if not joined.
        # joinedload does NOT essentially join for filtering purposes in some versions, but here we can be explicit if needed.
        # However, if we already used joinedload, the join is present in the query structure.
        # But for FILTERING, we usually need an explicit join if not already joined by the filter logic.
        # Since we might have joined for client_id, we check.
        if not client_id: 
             query = query.join(Sale)
        query = query.filter(Sale.product_id == product_id)
        
    returns = query.order_by(Return.created_at.desc()).all()
    
    return jsonify([r.as_dict() for r in returns]), 200
#####################################################################################################

###################################### UPDATE - Editar ou Dar Baixa #################################
@return_routes.route('/api/returns/<int:return_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_return(return_id):
    return_obj = Return.query.get(return_id)
    if not return_obj:
        return jsonify({'error': 'Devolução não encontrada.'}), 404
        
    data = request.get_json()
    action = data.get('action') # 'edit' or 'finalize'
    
    try:
        if action == 'finalize':
            # Dar Baixa (Status -> Retornada ou Concluída)
            # A lógica do usuário é: preenche data (vire Retornada), depois preenche lote (vira Concluída)
            
            data_retorno_str = data.get('data_retorno')
            novo_lote_id = data.get('novo_lote_id')
            
            if data_retorno_str:
                return_obj.data_retorno = datetime.strptime(data_retorno_str, "%Y-%m-%d")
                return_obj.status = 'Retornada'
                
            if novo_lote_id:
                # Validar lote novo
                new_production = Production.query.get(novo_lote_id)
                if not new_production:
                    return jsonify({'error': 'Novo lote não encontrado.'}), 404
                
                # Se já tiver data de retorno, e agora tem novo lote, finaliza
                if return_obj.data_retorno:
                   return_obj.novo_lote_id = novo_lote_id
                   return_obj.status = 'Concluída'
                   
                   # Adiciona ao estoque do novo lote !!
                   new_production.estoque_lote += return_obj.quant_devolvida
                   registrar_movimentacao(
                       num_lote=novo_lote_id,
                       product_id=new_production.product_id,
                       tipo='return_concluded',
                       quantidade=+return_obj.quant_devolvida,
                       estoque_apos=new_production.estoque_lote,
                       referencia_id=return_id,
                       referencia_tipo='return',
                       created_by=get_jwt_identity()
                   )

                   # Lógica de "Conversão de Devolução em Produção":
                   # Se o lote foi criado com quantidade produzida 0 (ex: criado especificamente para receber esta devolução),
                   # então registramos a quantidade devolvida como a quantidade "Produzida" (ou Inicial) deste lote.
                   # Isso garante que o lote tenha histórico consistente, evitando que fique com "Produzido: 0" e "Estoque: X".
                   if new_production.quant_caixa_produzida == 0:
                       new_production.quant_caixa_produzida = return_obj.quant_devolvida
                else:
                    return jsonify({'error': 'É necessário informar a data de retorno antes de vincular um lote.'}), 400

            db.session.commit()
            return jsonify({'message': 'Devolução atualizada com sucesso!', 'return': return_obj.as_dict()}), 200

        else:
            # Edição Simples (Obs e Quantidade - apenas se não finalizada?)
            # Se alterar quantidade, tem que ajustar na venda original para manter coerência?
            # O usuário disse "botão para alterar (onde vai alterar a quantidade e a OBS)"
            
            if return_obj.status == 'Concluída':
                 return jsonify({'error': 'Não é possível alterar uma devolução concluída (somente excluir).'}), 400
            
            if 'observacao' in data:
                return_obj.observacao = data['observacao']
                
            if 'quant_devolvida' in data:
                new_quant = int(data['quant_devolvida'])
                if new_quant <= 0:
                    return jsonify({'error': 'Quantidade deve ser maior que zero.'}), 400
                
                # Diff logic
                diff = new_quant - return_obj.quant_devolvida
                # Use relationship directly instead of unnecessary query
                sale = return_obj.sale
                
                # Se aumentou devolução (diff > 0), diminui venda. Se diminuiu devolução (diff < 0), aumenta venda.
                # Validar se venda comporta a redução extra (se diff > 0)
                if diff > 0 and (sale.quant_caixa_vendida - diff) < 0:
                     return jsonify({'error': 'Quantidade devolvida excede o restante da venda.'}), 400
                     
                sale.quant_caixa_vendida -= diff
                return_obj.quant_devolvida = new_quant

            db.session.commit()
            return jsonify({'message': 'Devolução alterada com sucesso!', 'return': return_obj.as_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar: {str(e)}'}), 500
#####################################################################################################

###################################### DELETE - Excluir devolução ###################################
@return_routes.route('/api/returns/<int:return_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_return(return_id):
    return_obj = Return.query.get(return_id)
    if not return_obj:
        return jsonify({'error': 'Devolução não encontrada.'}), 404
        
    try:
        # Reverter alterações
        # Se estava concluída, tenta remover do novo lote
        if return_obj.status == 'Concluída' and return_obj.novo_lote_id:
             new_production = Production.query.get(return_obj.novo_lote_id)
             if new_production:
                 # Verificação se o lote tem saldo suficiente para "devolver" a quantidade
                 if new_production.estoque_lote < return_obj.quant_devolvida:
                     return jsonify({'error': f'Não é possível excluir. O Lote #{new_production.num_lote} não possui estoque suficiente ({new_production.estoque_lote}) para reverter esta devolução ({return_obj.quant_devolvida}). Itens já foram vendidos.'}), 400
                 
                 new_production.estoque_lote -= return_obj.quant_devolvida
                 registrar_movimentacao(
                     num_lote=return_obj.novo_lote_id,
                     product_id=new_production.product_id,
                     tipo='return_deleted',
                     quantidade=-return_obj.quant_devolvida,
                     estoque_apos=new_production.estoque_lote,
                     referencia_id=return_id,
                     referencia_tipo='return',
                     created_by=get_jwt_identity()
                 )
                 
                 # Fix for phantom sales detection:
                 # If the lot becomes empty, matches the return quantity, and has NO real sales,
                 # we assume it was created for this return and reset the produced count to 0.
                 if new_production.estoque_lote == 0 and new_production.quant_caixa_produzida == return_obj.quant_devolvida:
                     if not new_production.sales:
                         new_production.quant_caixa_produzida = 0
        
        # Sempre devolve a quantidade para a venda original (sai do "Stand By")
        sale = Sale.query.get(return_obj.sale_id)
        if sale:
            sale.quant_caixa_vendida += return_obj.quant_devolvida
            
        db.session.delete(return_obj)
        db.session.commit()
        return jsonify({'message': 'Devolução excluída com sucesso!'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao excluir: {str(e)}'}), 500
#####################################################################################################
