from ockero_data_pipeline.run_pipeline import *

import typer

app = typer.Typer()

@app.command()
def run_pipeline_all():
    """This command runs a pipeline of dlt and dbt """

    run_all() ## from my run_pipeline, function that runs two functions inside run_pipeline.py


if __name__ == "__main__":
    app()