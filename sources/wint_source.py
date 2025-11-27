import dlt
from dlt.sources.rest_api import rest_api_source
from dlt.sources.helpers.rest_client import RESTClient
from dlt.common.configuration import configspec
from dlt.sources.helpers.rest_client.auth import AuthConfigBase
from dlt.sources.rest_api.config_setup import register_auth
from dlt.sources.helpers import requests
from requests.models import Response
from dlt.common import json


import base64
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
import os

API_KEY = os.getenv("WINT_AUTH")

@configspec
class CustomAuth(AuthConfigBase):
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = dlt.secrets["WINT_AUTH"]  # <-- runtime, safe
        self.api_key = base64.b64encode(api_key.encode('utf-8'))

    def __call__(self, request):
        request.headers["Authorization"] = f"Basic {self.api_key.decode('utf-8')}"
        return request

register_auth("custom_auth", CustomAuth)



wint_source = rest_api_source({
        "client": {
            "base_url": "https://superkollapi.wint.se/api",
            "auth": {
                "type": "custom_auth",
                "api_key": dlt.secrets["WINT_AUTH"],
            },

            "paginator": {
                "type": "page_number",
                "page_param": "Page",
                "total_path": "TotalItems",  # Let it paginate until empty
                "base_page": 0,  # If your API starts at page 1 (most do)
            },
        },
        "resource_defaults": {
            "write_disposition": "replace",

        },

        "resources": [
            #Accounts
            {   "name": "Account", 

                "endpoint": {
                    "path": "Account",
                    "paginator": "single_page" 
                        },
                },

            # Customers
            {   "name": "customer",
                "endpoint": "customer", 
            }, 
            # Dimensions
            {   "name": "dimension",
                "endpoint": "dimension",      
            },

            #Employess
            {   "name":  "employees",
                "endpoint": "employees", 
            },

            # Transactions
            {   "name": "transaction", 
                "write_disposition": "replace",

                "endpoint": {
                    "path": "transaction",
                    "params": {
                        "NumPerPage": 10000},          
                
                        },
            },

            # TimeReport
            {   "name": "time_report", 
                "write_disposition": "replace",

                "endpoint": {
                    "path": "Timereport/Report",
                    "paginator": "single_page" 
                        },
                },

        ],
    })




## Need to add custom fix to time_report due to its nested on so manu levels so its superslow 
## if we dont normalize it before

# @dlt.resource(
#     name = "time_report",
#     write_disposition = "replace"
# )
# def get_time_reports(page_size: int = 5000):

#     session = requests.Session()
#     session.auth = (API_KEY, "")
#     base_url = "https://superkollapi.wint.se/api/TimeReport/Report"

#     params = {
#         "Page": 0,
#         "NumPerPage": page_size
#     }

#     flattened_rows = []

#     def recurse(node, parent_fields):
#         """
#         Recursively flatten person -> columns -> children
#         """
#         base_fields = parent_fields.copy()
#         base_fields.update({
#             "PersonId": node.get("PersonId"),
#             "Description": node.get("Description"),
#             "TimeReportingReportRowLevel": node.get("TimeReportingReportRowLevel"),
#             "TimeReportingReportRowType": node.get("TimeReportingReportRowType"),
#         })

#         # Flatten columns
#         for col in node.get("Columns", []):
#             row = base_fields.copy()
#             for k, v in col.items():
#                 if k not in ("Invoices", "Children"):
#                     row[k] = v
#             flattened_rows.append(row)

#         # Process nested children
#         for child in node.get("Children") or []:
#             recurse(child, base_fields)

#     while True:
#         response = session.get(base_url, params=params)
#         response.raise_for_status()

#         data = response.json()

#         # no more data → break
#         if not data:
#             break

#         for item in data:
#             recurse(item, parent_fields={})

#         # last page if fewer results
#         if len(data) < page_size:
#             break

#         params["Page"] += 1

#     # yield all rows at once (MUCH faster)
#     for row in flattened_rows:
#         yield row