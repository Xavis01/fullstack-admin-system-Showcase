from flask import Blueprint, jsonify, request
from backend.models import Sale, Production, Product, Client, StockMovement, db
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta

dashboard_routes = Blueprint('dashboard_routes', __name__)

def apply_filters(query, model, date_field):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    product_id = request.args.get('product_id')
    client_id = request.args.get('client_id')
    months = request.args.get('months')  # Comma-separated month numbers
    years = request.args.get('years')    # Comma-separated year numbers
    
    if start_date:
        query = query.filter(date_field >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(date_field <= datetime.strptime(end_date, '%Y-%m-%d'))
    
    # Month/Year filtering
    if months:
        month_list = [int(m) for m in months.split(',') if m.strip()]
        if month_list:
            query = query.filter(extract('month', date_field).in_(month_list))
    
    if years:
        year_list = [int(y) for y in years.split(',') if y.strip()]
        if year_list:
            query = query.filter(extract('year', date_field).in_(year_list))
    
    if product_id and hasattr(model, 'product_id'):
        query = query.filter(model.product_id == product_id)
    
    if client_id and hasattr(model, 'client_id'):
        query = query.filter(model.client_id == client_id)
        
    return query

@dashboard_routes.route('/api/dashboard/summary', methods=['GET'])
def get_summary():
    try:
        # Base queries
        sales_q = db.session.query(func.sum(Sale.quant_caixa_vendida))
        prod_q = db.session.query(func.sum(Production.quant_caixa_produzida))
        stock_q = db.session.query(func.sum(Production.estoque_lote))
        clients_q = db.session.query(func.count(Client.id))

        # Apply filters
        # Note: client_id is automatically handled in apply_filters for models that have it (Sale)
        sales_q = apply_filters(sales_q, Sale, Sale.data_venda)
        prod_q = apply_filters(prod_q, Production, Production.data_producao)
        
        product_id = request.args.get('product_id')
        if product_id:
            stock_q = stock_q.filter(Production.product_id == product_id)
        
        total_sales_volume = sales_q.scalar() or 0
        total_production_volume = prod_q.scalar() or 0
        current_stock = stock_q.scalar() or 0
        total_clients = clients_q.scalar() or 0 

        # Growth Logic (Only if NO date filters are applied)
        sales_growth = 0
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date and not end_date:
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            first_day_curr = datetime(current_year, current_month, 1)
            last_month_date = first_day_curr - timedelta(days=1)
            first_day_prev = datetime(last_month_date.year, last_month_date.month, 1)

            # Re-query for growth specifically to ignore other potential noise, but respect product filter if needed
            growth_curr_q = db.session.query(func.sum(Sale.quant_caixa_vendida)).filter(Sale.data_venda >= first_day_curr)
            growth_prev_q = db.session.query(func.sum(Sale.quant_caixa_vendida)).filter(Sale.data_venda >= first_day_prev, Sale.data_venda < first_day_curr)
            
            if product_id:
                growth_curr_q = growth_curr_q.filter(Sale.product_id == product_id)
                growth_prev_q = growth_prev_q.filter(Sale.product_id == product_id)

            curr_month_sales = growth_curr_q.scalar() or 0
            prev_month_sales = growth_prev_q.scalar() or 0
            
            if prev_month_sales > 0:
                sales_growth = ((curr_month_sales - prev_month_sales) / prev_month_sales) * 100
        
        return jsonify({
            'total_sales_volume': total_sales_volume,
            'total_production_volume': total_production_volume,
            'current_stock': current_stock,
            'total_clients': total_clients,
            'sales_growth': round(sales_growth, 2)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_routes.route('/api/dashboard/charts', methods=['GET'])
def get_charts_data():
    try:
        # Defaults
        today = datetime.now()
        one_year_ago = today - timedelta(days=365)
        
        # Check params
        start_date = request.args.get('start_date')
        granularity = request.args.get('granularity', 'month') # 'month' or 'day'
        
        # Sales Query Construction
        if granularity == 'day':
            sales_sel = [
                extract('year', Sale.data_venda).label('year'),
                extract('month', Sale.data_venda).label('month'),
                extract('day', Sale.data_venda).label('day'),
                func.sum(Sale.quant_caixa_vendida)
            ]
            prod_sel = [
                extract('year', Production.data_producao).label('year'),
                extract('month', Production.data_producao).label('month'),
                extract('day', Production.data_producao).label('day'),
                func.sum(Production.quant_caixa_produzida)
            ]
        else:
             sales_sel = [
                extract('year', Sale.data_venda).label('year'),
                extract('month', Sale.data_venda).label('month'),
                func.sum(Sale.quant_caixa_vendida)
            ]
             prod_sel = [
                extract('year', Production.data_producao).label('year'),
                extract('month', Production.data_producao).label('month'),
                func.sum(Production.quant_caixa_produzida)
            ]
            
        # Execute Sales
        sales_query = db.session.query(*sales_sel)
        sales_query = apply_filters(sales_query, Sale, Sale.data_venda)
        
        if not start_date and granularity == 'month':
            sales_query = sales_query.filter(Sale.data_venda >= one_year_ago)
        elif not start_date and granularity == 'day':
            # Default to last 30 days if day view requested without date
            last_30 = today - timedelta(days=30)
            sales_query = sales_query.filter(Sale.data_venda >= last_30)

        if granularity == 'day':
            sales_results = sales_query.group_by('year', 'month', 'day').order_by('year', 'month', 'day').all()
            sales_data = [{'month': f"{int(y)}-{int(m):02d}-{int(d):02d}", 'total': float(t or 0)} for y, m, d, t in sales_results]
        else:
            sales_results = sales_query.group_by('year', 'month').order_by('year', 'month').all()
            sales_data = [{'month': f"{int(y)}-{int(m):02d}", 'total': float(t or 0)} for y, m, t in sales_results]

        # Execute Production
        prod_query = db.session.query(*prod_sel)
        prod_query = apply_filters(prod_query, Production, Production.data_producao)
        
        if not start_date and granularity == 'month':
            prod_query = prod_query.filter(Production.data_producao >= one_year_ago)
        elif not start_date and granularity == 'day':
            last_30 = today - timedelta(days=30)
            prod_query = prod_query.filter(Production.data_producao >= last_30)

        if granularity == 'day':
            prod_results = prod_query.group_by('year', 'month', 'day').order_by('year', 'month', 'day').all()
            production_data = [{'month': f"{int(y)}-{int(m):02d}-{int(d):02d}", 'total': float(t or 0)} for y, m, d, t in prod_results]
        else:
            prod_results = prod_query.group_by('year', 'month').order_by('year', 'month').all()
            production_data = [{'month': f"{int(y)}-{int(m):02d}", 'total': float(t or 0)} for y, m, t in prod_results]

        # MERGING LOGIC for Chart Data Alignment
        data_map = {}
        
        # Populate with sales
        for item in sales_data:
            key = item['month']
            if key not in data_map:
                data_map[key] = {'date': key, 'sales': 0, 'production': 0}
            data_map[key]['sales'] = item['total']
            
        # Populate with production
        for item in production_data:
            key = item['month']
            if key not in data_map:
                data_map[key] = {'date': key, 'sales': 0, 'production': 0}
            data_map[key]['production'] = item['total']
            
        # Sort by date
        sorted_keys = sorted(data_map.keys())
        over_time_data = [data_map[k] for k in sorted_keys]

        # Product Distribution (Sales)
        sales_prod_query = db.session.query(Product.nome, func.sum(Sale.quant_caixa_vendida)).join(Sale)
        sales_prod_query = apply_filters(sales_prod_query, Sale, Sale.data_venda)
        sales_by_product = sales_prod_query.group_by(Product.nome).all()

        # Product Distribution (Production)
        prod_prod_query = db.session.query(Product.nome, func.sum(Production.quant_caixa_produzida)).join(Production)
        prod_prod_query = apply_filters(prod_prod_query, Production, Production.data_producao)
        prod_by_product = prod_prod_query.group_by(Product.nome).all()

        return jsonify({
            'over_time': over_time_data,
            'sales_by_product': [{'product': p, 'total': float(t or 0)} for p, t in sales_by_product],
            'production_by_product': [{'product': p, 'total': float(t or 0)} for p, t in prod_by_product]
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@dashboard_routes.route('/api/dashboard/available-years', methods=['GET'])
def get_available_years():
    """Get all years that have sales or production records"""
    try:
        # Get years from sales
        sales_years = db.session.query(
            extract('year', Sale.data_venda).label('year')
        ).distinct().all()
        
        # Get years from production
        prod_years = db.session.query(
            extract('year', Production.data_producao).label('year')
        ).distinct().all()
        
        # Combine and sort
        all_years = set()
        for (year,) in sales_years:
            if year:
                all_years.add(int(year))
        for (year,) in prod_years:
            if year:
                all_years.add(int(year))
        
        sorted_years = sorted(list(all_years), reverse=True)
        
        return jsonify(sorted_years), 200
    except Exception as e:
        print("Error in get_available_years:")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@dashboard_routes.route('/api/report', methods=['GET'])
def get_report():
    """Generate a comprehensive report with filters for products, clients, months, and years."""
    try:
        product_ids_raw = request.args.get('product_ids', '')
        client_ids_raw = request.args.get('client_ids', '')
        months_raw = request.args.get('months', '')
        years_raw = request.args.get('years', '')

        product_ids = [int(p) for p in product_ids_raw.split(',') if p.strip()] if product_ids_raw else []
        client_ids = [int(c) for c in client_ids_raw.split(',') if c.strip()] if client_ids_raw else []
        month_list = [int(m) for m in months_raw.split(',') if m.strip()] if months_raw else []
        year_list = [int(y) for y in years_raw.split(',') if y.strip()] if years_raw else []

        # --- Stock by Product (current, not filtered by date) ---
        stock_query = db.session.query(
            Product.nome,
            func.sum(Production.estoque_lote)
        ).join(Production).group_by(Product.nome)

        if product_ids:
            stock_query = stock_query.filter(Product.id.in_(product_ids))

        stock_by_product = [{'product': name, 'stock': int(total or 0)} for name, total in stock_query.all()]

        # --- Sales by Product (filtered by period) ---
        sales_query = db.session.query(
            Product.nome,
            func.sum(Sale.quant_caixa_vendida)
        ).join(Sale).group_by(Product.nome)

        if product_ids:
            sales_query = sales_query.filter(Product.id.in_(product_ids))
        if month_list:
            sales_query = sales_query.filter(extract('month', Sale.data_venda).in_(month_list))
        if year_list:
            sales_query = sales_query.filter(extract('year', Sale.data_venda).in_(year_list))

        sales_by_product = [{'product': name, 'total': int(total or 0)} for name, total in sales_query.all()]

        # --- Production by Product (filtered by period) ---
        prod_query = db.session.query(
            Product.nome,
            func.sum(Production.quant_caixa_produzida)
        ).join(Production).group_by(Product.nome)

        if product_ids:
            prod_query = prod_query.filter(Product.id.in_(product_ids))
        if month_list:
            prod_query = prod_query.filter(extract('month', Production.data_producao).in_(month_list))
        if year_list:
            prod_query = prod_query.filter(extract('year', Production.data_producao).in_(year_list))

        production_by_product = [{'product': name, 'total': int(total or 0)} for name, total in prod_query.all()]

        # --- Totals ---
        total_sales = sum(item['total'] for item in sales_by_product)
        total_production = sum(item['total'] for item in production_by_product)

        # --- Purchases by Client (filtered by period and optionally by client and product) ---
        client_query = db.session.query(
            Client.nome,
            func.sum(Sale.quant_caixa_vendida)
        ).join(Sale).group_by(Client.nome)

        if client_ids:
            client_query = client_query.filter(Client.id.in_(client_ids))
        if product_ids:
            client_query = client_query.filter(Sale.product_id.in_(product_ids))
        if month_list:
            client_query = client_query.filter(extract('month', Sale.data_venda).in_(month_list))
        if year_list:
            client_query = client_query.filter(extract('year', Sale.data_venda).in_(year_list))

        purchases_by_client = [{'client': name, 'total': int(total or 0)} for name, total in client_query.all()]

        # --- Period Label ---
        month_names = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }

        period_parts = []
        if month_list:
            period_parts.append(', '.join(month_names.get(m, str(m)) for m in sorted(month_list)))
        if year_list:
            period_parts.append(', '.join(str(y) for y in sorted(year_list)))

        period_label = ' / '.join(period_parts) if period_parts else 'Todos os períodos'

        return jsonify({
            'stock_by_product': stock_by_product,
            'sales_by_product': sales_by_product,
            'production_by_product': production_by_product,
            'total_sales': total_sales,
            'total_production': total_production,
            'purchases_by_client': purchases_by_client,
            'period_label': period_label
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@dashboard_routes.route('/api/stock-movements', methods=['GET'])
def get_stock_movements():
    """Return stock movements with optional filters."""
    try:
        from sqlalchemy.orm import joinedload

        query = StockMovement.query.options(
            joinedload(StockMovement.product),
            joinedload(StockMovement.user),
            joinedload(StockMovement.production)
        )

        # Filters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        product_id = request.args.get('product_id')
        tipo = request.args.get('tipo')
        num_lote = request.args.get('num_lote')

        if start_date:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            if start_time:
                h, m = start_time.split(':')
                start_dt = start_dt.replace(hour=int(h), minute=int(m))
            
            from datetime import timedelta
            start_dt_utc = start_dt + timedelta(hours=3)
            query = query.filter(StockMovement.created_at >= start_dt_utc)

        if end_date:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            if end_time:
                h, m = end_time.split(':')
                end_dt = end_dt.replace(hour=int(h), minute=int(m))
            else:
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
            
            from datetime import timedelta
            end_dt_utc = end_dt + timedelta(hours=3)
            query = query.filter(StockMovement.created_at <= end_dt_utc)

        if product_id:
            query = query.filter(StockMovement.product_id == product_id)

        if tipo:
            query = query.filter(StockMovement.tipo == tipo)

        if num_lote:
            query = query.filter(StockMovement.num_lote.ilike(f'%{num_lote}%'))

        movements = query.order_by(StockMovement.created_at.desc()).all()

        result = []
        for m in movements:
            d = m.as_dict()
            d['product_name'] = m.product.nome if m.product else 'Desconhecido'
            # Add product image
            image_url = None
            if m.product and m.product.image_path:
                path = m.product.image_path
                if path.startswith('http'):
                    image_url = path
                else:
                    clean_path = path.replace('backend\\', '').replace('backend/', '').replace('\\', '/')
                    if not clean_path.startswith('/'):
                        clean_path = f'/{clean_path}'
                    image_url = clean_path
            d['product_image'] = image_url
            result.append(d)

        return jsonify(result), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@dashboard_routes.route('/api/stock-at-date', methods=['GET'])
def get_stock_at_date():
    """Calculate total stock per product at a specific date/time."""
    try:
        target_date = request.args.get('date')
        target_time = request.args.get('time')
        product_id = request.args.get('product_id')

        if not target_date:
            return jsonify({'error': 'Parâmetro "date" é obrigatório (YYYY-MM-DD).'}), 400

        target_dt = datetime.strptime(target_date, '%Y-%m-%d')
        if target_time:
            h, m = target_time.split(':')
            target_dt = target_dt.replace(hour=int(h), minute=int(m), second=59)
        else:
            target_dt = target_dt.replace(hour=23, minute=59, second=59)

        # Convert local time (BRT UTC-3) to UTC for DB comparison
        from datetime import timedelta
        target_dt_utc = target_dt + timedelta(hours=3)

        # Subquery: get the latest movement ID for each lot up to target date
        subq = db.session.query(
            StockMovement.num_lote,
            func.max(StockMovement.id).label('last_id')
        ).filter(
            StockMovement.created_at <= target_dt_utc
        ).group_by(StockMovement.num_lote).subquery()

        # Main query: get the estoque_apos from each latest movement
        query = db.session.query(
            StockMovement.num_lote,
            StockMovement.product_id,
            Product.nome.label('product_name'),
            Product.image_path.label('product_image'),
            StockMovement.estoque_apos
        ).join(
            subq, StockMovement.id == subq.c.last_id
        ).join(
            Product, StockMovement.product_id == Product.id
        )

        if product_id:
            query = query.filter(StockMovement.product_id == int(product_id))

        results = query.all()

        # Aggregate by product
        product_stocks = {}
        lotes_detail = []

        for num_lote, prod_id, prod_name, prod_image, estoque in results:
            image_url = None
            if prod_image:
                if prod_image.startswith('http'):
                    image_url = prod_image
                else:
                    clean_path = prod_image.replace('backend\\', '').replace('backend/', '').replace('\\', '/')
                    if not clean_path.startswith('/'):
                        clean_path = f'/{clean_path}'
                    image_url = clean_path

            lotes_detail.append({
                'num_lote': num_lote,
                'product_id': prod_id,
                'product_name': prod_name,
                'product_image': image_url,
                'estoque_lote': estoque
            })
            if prod_name not in product_stocks:
                product_stocks[prod_name] = {
                    'product_name': prod_name, 
                    'product_id': prod_id, 
                    'product_image': image_url,
                    'total_stock': 0, 
                    'lotes_count': 0
                }
            product_stocks[prod_name]['total_stock'] += estoque
            product_stocks[prod_name]['lotes_count'] += 1

        stock_by_product = sorted(product_stocks.values(), key=lambda x: x['product_name'])

        return jsonify({
            'date': target_date,
            'time': target_time or '23:59',
            'stock_by_product': stock_by_product,
            'stock_by_lote': lotes_detail,
            'total_geral': sum(p['total_stock'] for p in stock_by_product)
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
