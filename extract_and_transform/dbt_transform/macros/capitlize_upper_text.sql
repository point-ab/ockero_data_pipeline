{% macro clean_uppercase_text(column_name) %}
{% set replacements = {
    'Ab': 'AB',
    'Of': 'of',
    'The': 'the'
} %}

CASE
    WHEN {{ column_name }} IS NULL THEN NULL

    -- Only transform fully-uppercase strings
    WHEN {{ column_name }} = upper({{ column_name }})
    THEN array_to_string(
        array_apply(
            string_split(trim({{ column_name }}), ' '),
            word ->

                -- Split on hyphens AND rejoin with hyphens after processing parts
                array_to_string(
                    array_apply(
                        string_split(word, '-'),
                        part ->

                            -- Capitalize first letter of the part
                            CASE
                                {% for key, val in replacements.items() %}
                                WHEN upper(part) = upper('{{ key }}')
                                    THEN '{{ val }}'
                                {% endfor %}
                                ELSE upper(substr(part,1,1)) || lower(substr(part,2))
                            END
                    ),
                    '-'
                )
        ),
        ' '
    )

    ELSE trim({{ column_name }})
END
{% endmacro %}