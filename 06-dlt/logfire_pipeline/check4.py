import duckdb

con = duckdb.connect('logfire_pipeline.duckdb')

result = con.sql("""
    SELECT span_id, span_name, attributes__gen_ai_usage_input_tokens, attributes__gen_ai_usage_output_tokens
    FROM agent_traces.spans
    WHERE trace_id = '019fa51d8ed89c61bee52c50e267a69d'
    ORDER BY start_timestamp
""").fetchall()

print("Все spans с токенами:")
for r in result:
    print(r)

total = con.sql("""
    SELECT SUM(attributes__gen_ai_usage_input_tokens) AS total_input_tokens
    FROM agent_traces.spans
    WHERE trace_id = '019fa51d8ed89c61bee52c50e267a69d'
""").fetchone()

print("\nСумма input_tokens по трейсу:", total)