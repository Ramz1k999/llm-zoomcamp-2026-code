import pandas as pd
import sqlite3

conn = sqlite3.connect("traces.db")
df = pd.read_sql("SELECT * FROM spans", conn)

df['duration'] = df['end_time'] - df['start_time']

result = (
    df[df['name'] != 'rag']
    .groupby('name')['duration']
    .sum()
)
print(result)

df = pd.read_sql("SELECT * FROM spans WHERE name = 'llm'", conn)
print(df['input_tokens'])


tokens = df['input_tokens']
print(tokens.min(), tokens.max())
print((tokens.max() - tokens.min()) / tokens.min() * 100, "%")

# Name: duration, dtype: int64
# 0    7111
# 1    7111
# 2    7111
# Name: input_tokens, dtype: int64
# 7111 7111
# 0.0 %