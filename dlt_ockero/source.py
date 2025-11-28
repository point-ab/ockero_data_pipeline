import dlt
from dlt.sources.rest_api import rest_api_source
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get token from environment
token = os.getenv('SS12000_TOKEN')

# Configure the REST API source
def load_schoolsoft_data():
    source = rest_api_source({
        "client": {
            "base_url": "https://sms.schoolsoft.se/ockero/ss12000/v2/",
            "auth": {
                "type": "bearer",
                "token": token
            }
        },
        "resources": [
            # {   "name": "persons",
            #     "endpoint": "persons",
            # },
            
            # {   "name": "duties",
            #     "endpoint":"duties",

            # },    
            # {   "name": "placements",
            #     "endpoint": "placements",
            # },
            
            {   "name": "organisations",
                "endpoint": "organisations",
            },

            {   "name": "groups",
                "endpoint": "groups",
            },
            {   "name": "activities",
                "endpoint": "activities",
            },
        ]
    })
    
    return source


