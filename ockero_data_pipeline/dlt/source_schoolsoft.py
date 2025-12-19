from ockero_data_pipeline import dlt
import requests
import csv
from io import StringIO
from typing import Iterator, Dict, Any, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


# Configuration
API_PASSWORD = os.getenv('SS12000_SECRET')
BASE_URL = f"https://sms.schoolsoft.se/ockero/"


def fetch_schoolsoft_data(endpoint: str, params: Optional[Dict[str, str]] = None) -> str:
    url = f"{BASE_URL}{endpoint}"
    headers = {"X-REMOTEPWD": API_PASSWORD}
    
    # Default to txt (tab-delimited) format
    if params is None:
        params = {}
    if "fileFormat" not in params:
        params["fileFormat"] = "txt"
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.text


def parse_tsv_to_dicts(tsv_text: str) -> list[Dict[str, Any]]:
    try:
        # Use csv.DictReader with tab delimiter
        reader = csv.DictReader(StringIO(tsv_text), delimiter='\t')
        items = list(reader)
        
        print(f"Parsed {len(items)} rows from TSV")
        if items:
            print(f"Columns: {list(items[0].keys())}")
        
        return items
    
    except Exception as e:
        print(f"TSV parsing error: {e}")
        print(f"Response preview: {tsv_text[:500]}")
        return [{"raw_response": tsv_text, "parse_error": str(e)}]



@dlt.resource(name="schools", write_disposition="replace")
def schools_resource() -> Iterator[Dict[str, Any]]:
    """Fetch schools data"""
    print("Fetching schools...")
    tsv_data = fetch_schoolsoft_data("/export/schools.jsp")
    items = parse_tsv_to_dicts(tsv_data)
    
    for item in items:
        yield item

def schoolsoft_resource(name: str, endpoint: str, params: Dict[str, Any] | None = None):

    @dlt.resource(name=name, write_disposition="replace")
    def _resource():
        print(f"Fetching resource: {name} from {endpoint}")
        tsv_data = fetch_schoolsoft_data(endpoint, params)
        items = parse_tsv_to_dicts(tsv_data)

        for item in items:
            yield item

    return _resource()

@dlt.source
def schoolsoft_source():
    return [
        schoolsoft_resource("schools", "/export/schools.jsp"),
        schoolsoft_resource("students", "/export/students.jsp"),
        schoolsoft_resource("studentgrades", "/export/studentgradesubjects.jsp"),
        schoolsoft_resource("subjects", "/export/gradesubjects.jsp"),

        #schoolsoft_resource("teachers", "/export/teachers.jsp", {"schoolType": "9"}),        
        # Example: dynamic attendance
        # schoolsoft_resource("attendance_w1", "/export/attendance.jsp", {"week": 1})
    ]
