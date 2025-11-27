
from pipeline import *
from sources.test_source import *
from sources.wint_source import *
import dlt 
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
 

### ------- Pipeline settings --------
    pipeline_wint = dlt.pipeline(
        pipeline_name="dlt-ockero_ss12000",
        destination="filesystem",
        dataset_name="dlt_ockero",
        progress="log",  # This will show detailed progress
    )   



    #Crete logger outside pipeline to get real time values also!
    run_pipeline(pipeline_wint, wint_source)

