import subprocess
import sys
import os
from pathlib import Path
from ockero_data_pipeline.utils.logger import PipelineLogger, Timer

# Set folder name for different steps
dlt_folder = "dlt"
dlt_pipeline_file = "pipeline.py" 
dbt_folder = "dbt"


def run_dlt_pipeline(logger, timer):
    """Step 1: Run dlt data extraction"""
    logger.print_section("STEP 1: DLT")
    
    timer.start()
    dlt_dir = Path(__file__).parent /dlt_folder
    os.chdir(dlt_dir)
    
    logger.print_step(1, 2, "START", "dlt run")
    
    try:
        result = subprocess.run(
            [sys.executable, "pipeline.py"],
            check=True,
            capture_output=True,
            text=True
        )
        
        logger.print_output(result.stdout)
        
        elapsed = timer.elapsed()
        logger.print_with_timestamp("")
        logger.print_step(1, 2, "OK", "DLT completed", elapsed)
        logger.print_with_timestamp("") # NEW
        return True
        
    except subprocess.CalledProcessError as e:
        elapsed = timer.elapsed()
        logger.print_step(1, 2, "ERROR", "DLT failed", elapsed)
        logger.print_error(e.stderr)
        logger.print_with_timestamp("")
        return False


def run_dbt_transformations(logger, timer):
    """Step 2: Run dbt transformations"""
    logger.print_section("STEP 2: DBT")
    
    timer.start()
    dbt_dir = Path(__file__).parent /dbt_folder
    os.chdir(dbt_dir)
    
    logger.print_step(2, 2, "START", "dbt run")
    logger.print_with_timestamp("")

    try:
        # Run dbt deps silently
        subprocess.run(["dbt", "deps"], check=True, capture_output=True)
        
        # Run dbt models with output directly to terminal
        subprocess.run(["dbt", "run"], check=True)
        
        elapsed = timer.elapsed()
        logger.print_with_timestamp("")
        logger.print_step(2, 2, "OK", "DBT completed", elapsed)
        logger.print_with_timestamp("")
        return True
        
    except subprocess.CalledProcessError as e:
        elapsed = timer.elapsed()
        logger.print_step(2, 2, "ERROR", "DBT transformations failed", elapsed)
        logger.print_with_timestamp("")
        return False


def run_all():
    """Run the complete pipeline"""
    # Initialize utilities
    logger = PipelineLogger()
    timer = Timer()
    original_dir = os.getcwd()
    
    # Print header
    logger.print_header("DATA PIPELINE")
    
    # Start total timer
    timer.start()
    
    try:
        # Step 1: Extract data with dlt
        if not run_dlt_pipeline(logger, Timer()):
            logger.print_failure("Step 1: Running DLT")
            sys.exit(1)
        
        # Step 2: Transform data with dbt
        if not run_dbt_transformations(logger, Timer()):
            logger.print_failure("Step 2: Running DBT")
            sys.exit(1)
        
        # Success summary
        total_elapsed = timer.elapsed()
        steps = [
            {"name": "Step 1: DLT run"},
            {"name": "Step 2: DBT run"}
        ]
        logger.print_success_summary(total_elapsed, steps)
        
    except Exception as e:
        logger.print_unexpected_error(e)
        sys.exit(1)
    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    run_all()
