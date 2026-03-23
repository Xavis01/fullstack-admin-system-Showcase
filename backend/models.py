from datetime import datetime
from backend import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    primeiro_nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    dt_nascimento = db.Column(db.Date, nullable=True)
    password_hash = db.Column(db.String(512), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_master = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'primeiro_nome': self.primeiro_nome,
            'email': self.email,
            'dt_nascimento': self.dt_nascimento.strftime("%Y-%m-%d") if self.dt_nascimento else None,
            'is_admin': self.is_admin,
            'is_master': self.is_master,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }



class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)  # razão social
    telefone = db.Column(db.BigInteger, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total_compras(self):
        return len(self.sales)

    @property
    def total_caixas(self):
        return sum([s.quant_caixa_vendida for s in self.sales])

    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'total_compras': self.total_compras,
            'total_caixas': self.total_caixas,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }
        
        
        
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    unidades_por_caixa = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Não guarda o acumulado em campo fixo: faz a soma dinâmica via property
    productions = db.relationship('Production', backref='product', lazy=True)

    @property
    def total_acumulado_caixa(self):
        # Soma estoque_lote de todos os lotes desse produto
        return sum([p.estoque_lote for p in self.productions])
    
    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'total_acumulado_caixa': self.total_acumulado_caixa,
            'unidades_por_caixa': self.unidades_por_caixa,
            'image_path': self.image_path,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }

        
        
        
class Production(db.Model):
    __tablename__ = 'productions'
    num_lote = db.Column(db.String(50), primary_key=True)  # chave primária
    data_producao = db.Column(db.Date, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quant_caixa_produzida = db.Column(db.Integer, nullable=False)
    estoque_lote = db.Column(db.Integer, nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='created_productions')

    def as_dict(self):
        sales_dates = [s.data_venda for s in self.sales if s.data_venda]
        first_sale = min(sales_dates) if sales_dates else None
        last_sale = max(sales_dates) if sales_dates else None

        return {
            'num_lote': self.num_lote,
            'data_producao': self.data_producao.strftime("%Y-%m-%d") if self.data_producao else None,
            'product_id': self.product_id,
            'quant_caixa_produzida': self.quant_caixa_produzida,
            'estoque_lote': self.estoque_lote,
            'created_by': self.created_by,
            'created_by_name': self.user.nome if self.user else 'Desconhecido',
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'has_sales': len(self.sales) > 0,
            'first_sale_date': first_sale.strftime("%Y-%m-%d") if first_sale else None,
            'last_sale_date': last_sale.strftime("%Y-%m-%d") if last_sale else None
        }

        
        
class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    num_lote = db.Column(db.String(50), db.ForeignKey('productions.num_lote'), nullable=False)  # FK igual PK de Production
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    data_venda = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    quant_caixa_vendida = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Vínculo opcional com item de expedição (NULL = venda avulsa)
    order_product_id = db.Column(db.Integer, db.ForeignKey('order_products.id'), nullable=True)

    client = db.relationship('Client', backref='sales')
    user = db.relationship('User', backref='created_sales')
    product = db.relationship('Product', backref='sales')
    production = db.relationship('Production', backref='sales')
    order_product = db.relationship('OrderProduct', backref=db.backref('linked_sale', uselist=False))

    def as_dict(self):
        return {
            'id': self.id,
            'num_lote': self.num_lote,
            'product_id': self.product_id,
            'data_venda': self.data_venda.strftime("%Y-%m-%d") if self.data_venda else None,
            'client_id': self.client_id,
            'quant_caixa_vendida': self.quant_caixa_vendida,
            'created_by': self.created_by,
            'created_by_name': self.user.nome if self.user else 'Desconhecido',
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'order_product_id': self.order_product_id
        }
        
        
class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    meta_final = db.Column(db.Integer, nullable=False)
    meta_atual = db.Column(db.Integer, default=0)
    achieved = db.Column(db.Boolean, default=False)
    is_locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to link specifically tracked productions
    productions = db.relationship('GoalProduction', backref='goal', cascade="all, delete-orphan")

    def as_dict(self):
        return {
            'id': self.id,
            'data_inicio': self.data_inicio.strftime("%Y-%m-%d") if self.data_inicio else None,
            'data_fim': self.data_fim.strftime("%Y-%m-%d") if self.data_fim else None,
            'meta_final': self.meta_final,
            'meta_atual': self.meta_atual,
            'achieved': self.achieved,
            'is_locked': self.is_locked,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'linked_productions': [
                {
                    'num_lote': gp.num_lote,
                    'quantidade': gp.quant_caixa_produzida,
                    'data_producao': gp.production.data_producao.strftime("%Y-%m-%d") if gp.production and gp.production.data_producao else None
                }
                for gp in self.productions
            ]
        }


class GoalProduction(db.Model):
    __tablename__ = 'goal_productions'
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)
    num_lote = db.Column(db.String(50), db.ForeignKey('productions.num_lote'), nullable=False)
    quant_caixa_produzida = db.Column(db.Integer, nullable=False)
    
    # Relationship to Production (optional if not strictly needed for backref, but good for access)
    production = db.relationship('Production', backref='goal_links')


class Return(db.Model):
    __tablename__ = 'returns'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    # Rastrear de onde veio (lote original) facilita consultas
    num_lote_origem = db.Column(db.String(50), db.ForeignKey('productions.num_lote'), nullable=False)
    
    quant_devolvida = db.Column(db.Integer, nullable=False)
    
    # Status: 'Aberto', 'Retornada', 'Concluída'
    status = db.Column(db.String(20), default='Aberto', nullable=False)
    
    # Quando o usuário diz que a mercadoria fisicamente chegou (Status -> Retornada)
    data_retorno = db.Column(db.Date, nullable=True)
    
    # Quando o usuário vincula a um novo lote (Status -> Concluída)
    novo_lote_id = db.Column(db.String(50), db.ForeignKey('productions.num_lote'), nullable=True)
    
    observacao = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sale = db.relationship('Sale', backref='returns')
    lote_origem = db.relationship('Production', foreign_keys=[num_lote_origem], backref='returns_origin')
    novo_lote = db.relationship('Production', foreign_keys=[novo_lote_id], backref='returns_destination')

    def as_dict(self):
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'num_lote_origem': self.num_lote_origem,
            'quant_devolvida': self.quant_devolvida,
            'status': self.status,
            'data_retorno': self.data_retorno.strftime("%Y-%m-%d") if self.data_retorno else None,
            'novo_lote_id': self.novo_lote_id,
            'observacao': self.observacao,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            # Extra fields helpful for UI
            # Extra fields helpful for UI - Safe navigation
            'client_name': self.sale.client.nome if self.sale and hasattr(self.sale, 'client') and self.sale.client else 'Desconhecido',
            'product_name': self.sale.product.nome if self.sale and hasattr(self.sale, 'product') and self.sale.product else 'Desconhecido',
            'product_image': self.sale.product.image_path if self.sale and hasattr(self.sale, 'product') and self.sale.product else None,
            'product_id': self.sale.product_id if self.sale else None
        }


class SaleOrder(db.Model):
    __tablename__ = 'sale_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    quant_caixa_solicitada = db.Column(db.Integer, nullable=False)
    achieved = db.Column(db.Boolean, default=False, nullable=False)
    separado = db.Column(db.Boolean, default=False, nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    client = db.relationship('Client', backref='sale_orders')
    user = db.relationship('User', backref='created_sale_orders')
    products = db.relationship('OrderProduct', backref='order', cascade='all, delete-orphan')

    def as_dict(self):
        lotes = []
        for op in self.products:
            prod = op.production
            product = prod.product if prod else None
            image_url = None
            if product and product.image_path:
                path = product.image_path
                if path.startswith('http'):
                    image_url = path
                else:
                    clean_path = path.replace('backend\\\\', '').replace('backend/', '').replace('\\\\', '/')
                    if not clean_path.startswith('/'):
                        clean_path = f'/{clean_path}'
                    image_url = clean_path
            lotes.append({
                'id': op.id,
                'num_lote': op.num_lote,
                'quantidade': op.quantidade,
                'product_name': product.nome if product else 'Desconhecido',
                'product_image': image_url,
                'estoque_lote': prod.estoque_lote if prod else 0,
                'sold': op.linked_sale is not None,
                'sale_id': op.linked_sale.id if op.linked_sale else None
            })

        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_name': self.client.nome if self.client else 'Desconhecido',
            'quant_caixa_solicitada': self.quant_caixa_solicitada,
            'lotes': lotes,
            'achieved': self.achieved,
            'separado': self.separado,
            'observacao': self.observacao,
            'created_by': self.created_by,
            'created_by_name': self.user.nome if self.user else 'Desconhecido',
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }


class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('sale_orders.id'), nullable=False)
    num_lote = db.Column(db.String(50), db.ForeignKey('productions.num_lote'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)

    production = db.relationship('Production', backref='order_products')


class Procedure(db.Model):
    __tablename__ = 'procedures'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)           # safe stored filename on disk
    original_filename = db.Column(db.String(255), nullable=False)  # original name for display
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='created_procedures')

    def as_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'created_by': self.created_by,
            'created_by_name': self.user.nome if self.user else 'Desconhecido',
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
        }


class StockMovement(db.Model):
    __tablename__ = 'stock_movements'
    id = db.Column(db.Integer, primary_key=True)
    num_lote = db.Column(db.String(50), db.ForeignKey('productions.num_lote'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    estoque_apos = db.Column(db.Integer, nullable=False)
    referencia_id = db.Column(db.String(50), nullable=True)
    referencia_tipo = db.Column(db.String(50), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    production = db.relationship('Production', backref='stock_movements')
    product = db.relationship('Product', backref='stock_movements')
    user = db.relationship('User', backref='stock_movements')

    def as_dict(self):
        return {
            'id': self.id,
            'num_lote': self.num_lote,
            'product_id': self.product_id,
            'tipo': self.tipo,
            'quantidade': self.quantidade,
            'estoque_apos': self.estoque_apos,
            'referencia_id': self.referencia_id,
            'referencia_tipo': self.referencia_tipo,
            'created_by': self.created_by,
            'created_by_name': self.user.nome if self.user else None,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }


def registrar_movimentacao(num_lote, product_id, tipo, quantidade, estoque_apos,
                           referencia_id=None, referencia_tipo=None, created_by=None):
    """Registra uma movimentação de estoque na tabela stock_movements."""
    mov = StockMovement(
        num_lote=num_lote,
        product_id=product_id,
        tipo=tipo,
        quantidade=quantidade,
        estoque_apos=estoque_apos,
        referencia_id=str(referencia_id) if referencia_id else None,
        referencia_tipo=referencia_tipo,
        created_by=created_by
    )
    db.session.add(mov)
