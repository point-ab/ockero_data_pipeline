{% macro export_parquet_to_folder(model_name) %}
  {% set export_path = '../data/' ~ model_name.name ~ '.parquet' %}
  {% set sql %}
    COPY (SELECT * FROM {{ model_name }})
    TO '{{ export_path }}'
    (FORMAT PARQUET, COMPRESSION ZSTD);
  {% endset %}
  {% do run_query(sql) %}
  {{ log("✅ Exported " ~ model_name.name ~ " to " ~ export_path, info=True) }}
{% endmacro %}
