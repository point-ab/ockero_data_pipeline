
from dlt_utils import *
from source import *
import dlt 
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
 

### ------- Pipeline settings --------
    pipeline_ss12000 = dlt.pipeline(
        pipeline_name="dlt-ockero-schoolsoft",
        destination="duckdb",
        dataset_name="dlt_ockero_schoolsoft",
        progress="log", 
    )   


    # TO DO!!! Create logger outside pipeline to get real time values also!
    run_pipeline(pipeline_ss12000, load_schoolsoft_data())

