{% macro extract_json_fields(json_column, field, data_type) %}

({{ json_column }} ->> '{{ field }}')::{{ data_type }}

{% endmacro %}