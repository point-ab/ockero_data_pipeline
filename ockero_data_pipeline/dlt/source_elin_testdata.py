from ockero_data_pipeline import dlt
import json
from pathlib import Path




file_path = Path(__file__).resolve()
target_path = file_path.parent.parent / "data"/ "data_in" / "TestDataElin.txt"



@dlt.resource(name="students", write_disposition="replace")
def load_data_from_file():    
    # Read the file
    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # If it's an array, yield each item
    if isinstance(data, list):
        for item in data:
            yield item
    else:
        # If it's a single object, yield it
        yield data

