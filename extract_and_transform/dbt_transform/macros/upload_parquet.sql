{% macro upload_parquet() %}
{% do run_query("python scripts/upload_parquet_to_azure.py") %}
{% endmacro %}
