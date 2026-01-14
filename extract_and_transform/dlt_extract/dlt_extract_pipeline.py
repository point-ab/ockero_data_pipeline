from dlt_utils import *
from source_schoolsoft import *
from source_elin_testdata import *

import dlt
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


# Resolve duckdb inside project/data/db_.duckdb
project_root = Path(__file__).resolve().parent.parent.parent
duckdb_path = project_root / "data" / "db_pipeline.duckdb"


if __name__ == "__main__":
 
# ### ------- Pipeline settings --------
    # pipeline_ss12000 = dlt.pipeline(
    #     pipeline_name="dlt-ss12000",
    #     destination=dlt.destinations.duckdb(duckdb_path), # absolut path, to sync with dbt project path!
    #     dataset_name="dlt_ss12000",
    #     progress="log", 
    # )   

    # Create a DLT pipeline
    pipeline_schoolsoft = dlt.pipeline(
        pipeline_name="schoolsoft_pipeline",
        destination=dlt.destinations.duckdb(duckdb_path), # absolut path, to sync with dbt project path!
        dataset_name="dlt_schoolsoft"
    )
        # Create a DLT pipeline
    pipeline_elin_testdata = dlt.pipeline(
        pipeline_name="elin_testdata",
        destination=dlt.destinations.duckdb(duckdb_path), # absolut path, to sync with dbt project path!
        dataset_name="dlt_elin_testdata"
    )
    




    #run_pipeline(pipeline_ss12000, load_ss12000_data())
    run_pipeline(pipeline_schoolsoft, schoolsoft_source())
    run_pipeline(pipeline_elin_testdata, load_data_from_file())
