from dlt_utils import *
from source_schoolsoft import *
from source_elin_testdata import *
import extract_and_transform
import dlt
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


project_root = Path.cwd().parent.parent
duckdb_path = project_root / "data" / "db_pipeline.duckdb"



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
    
if __name__ == "__main__":

    from extract_and_transform.dlt_extract.dlt_utils import run_pipeline
    from extract_and_transform.dlt_extract.source_schoolsoft import schoolsoft_source
    from extract_and_transform.dlt_extract.source_elin_testdata import load_data_from_file

    run_pipeline(pipeline_schoolsoft, schoolsoft_source())
    run_pipeline(pipeline_elin_testdata, load_data_from_file())


