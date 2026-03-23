from backend import create_app, db
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    # 1) Cria tabelas novas
    db.create_all()

    # 2) Adiciona colunas faltantes em tabelas existentes
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()
    added = []

    for table in db.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue

        db_columns = {col['name'] for col in inspector.get_columns(table.name)}

        for column in table.columns:
            if column.name not in db_columns:
                col_type = column.type.compile(dialect=db.engine.dialect)
                nullable = "NULL" if column.nullable else "NOT NULL"
                
                default_clause = ""
                if column.default is not None:
                    default_val = column.default.arg
                    if isinstance(default_val, bool):
                        default_clause = f"DEFAULT {1 if default_val else 0}"
                    elif isinstance(default_val, (int, float)):
                        default_clause = f"DEFAULT {default_val}"
                    elif isinstance(default_val, str):
                        default_clause = f"DEFAULT '{default_val}'"
                
                sql = f"ALTER TABLE `{table.name}` ADD COLUMN `{column.name}` {col_type} {nullable} {default_clause}"
                db.session.execute(text(sql))
                added.append(f"{table.name}.{column.name}")

    db.session.commit()

    if added:
        print(f"Tabelas sincronizadas! Colunas adicionadas: {', '.join(added)}")
    else:
        print("Tabelas criadas com sucesso! Nenhuma coluna nova necessária.")
