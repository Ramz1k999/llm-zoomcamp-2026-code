import os
import json
import requests

LOGFIRE_READ_TOKEN = os.environ["LOGFIRE_READ_TOKEN"]

LOGFIRE_API_URL = "https://logfire-api.pydantic.dev/v1/query"

query = """
SELECT *
FROM records
ORDER BY start_timestamp DESC
LIMIT 5
"""

headers = {
    "Authorization": f"Bearer {LOGFIRE_READ_TOKEN}",
    "Accept": "application/json",
}
params = {"sql": query}

response = requests.get(LOGFIRE_API_URL, headers=headers, params=params)
print("Status code:", response.status_code)
print("Response text (first 3000 chars):")
print(response.text[:3000])