import duckdb

con = duckdb.connect('logfire_pipeline.duckdb')

result = con.sql("""
    SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'agent_traces'
""").fetchall()

print("Количество таблиц:", result)

tables = con.sql("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'agent_traces'
""").fetchall()

print("Список таблиц:")
for t in tables:
    print(t)