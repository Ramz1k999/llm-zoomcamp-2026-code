import duckdb

con = duckdb.connect('logfire_pipeline.duckdb')

# Посмотрим на колонки таблицы spans, которые касаются токенов
cols = con.sql("""
    SELECT column_name FROM information_schema.columns
    WHERE table_schema = 'agent_traces' AND table_name = 'spans'
    AND column_name ILIKE '%token%'
""").fetchall()
print("Колонки с 'token' в spans:")
for c in cols:
    print(c)

# Проверим сам трейс
result = con.sql("""
    SELECT span_id, span_name, trace_id
    FROM agent_traces.spans
    WHERE trace_id = '019fa51d8ed89c61bee52c50e267a69d'
""").fetchall()
print("\nSpans в нужном трейсе:")
for r in result:
    print(r)