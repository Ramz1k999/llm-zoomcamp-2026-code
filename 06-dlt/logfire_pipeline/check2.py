import duckdb

con = duckdb.connect('logfire_pipeline.duckdb')

print("Все схемы:")
print(con.sql("SELECT schema_name FROM information_schema.schemata").fetchall())

print("\nВсе таблицы (любая схема):")
print(con.sql("SELECT table_schema, table_name FROM information_schema.tables").fetchall())