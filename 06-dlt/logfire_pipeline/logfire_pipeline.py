import os
import dlt
from dlt.sources.helpers import requests

LOGFIRE_READ_TOKEN = os.environ["LOGFIRE_READ_TOKEN"]

LOGFIRE_API_URL = "https://logfire-api.pydantic.dev/v1/query"


@dlt.resource(name="spans", write_disposition="replace")
def logfire_spans():
    query = """
    SELECT *
    FROM records
    ORDER BY start_timestamp DESC
    LIMIT 1000
    """
    headers = {
        "Authorization": f"Bearer {LOGFIRE_READ_TOKEN}",
        "Accept": "application/json",
    }
    params = {"sql": query}

    response = requests.get(LOGFIRE_API_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    columns = data["columns"]
    col_names = [c["name"] for c in columns]
    col_values = [c["values"] for c in columns]

    if not col_values:
        return

    n_rows = len(col_values[0])

    for i in range(n_rows):
        row = {col_names[j]: col_values[j][i] for j in range(len(col_names))}
        yield row


def load_logfire_traces():
    pipeline = dlt.pipeline(
        pipeline_name="logfire_pipeline",
        destination="duckdb",
        dataset_name="agent_traces",
    )
    load_info = pipeline.run(logfire_spans())
    print(load_info)


if __name__ == "__main__":
    load_logfire_traces()