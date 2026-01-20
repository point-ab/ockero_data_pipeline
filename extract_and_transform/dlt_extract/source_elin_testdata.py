import json
import dlt
from pathlib import Path


project_root = Path.cwd().parent.parent
target_path = project_root / "data_in" / "TestDataElin.txt"


@dlt.resource(name="students", write_disposition="replace")
def load_data_from_file():
    if not target_path.exists():
        raise FileNotFoundError(
            f"Missing input file:\n  {target_path}"
        )

    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    yield from data if isinstance(data, list) else [data]