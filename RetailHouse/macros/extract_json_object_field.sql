{% macro extract_json_object_field(json_column, field, data_type='text') -%}

({{ json_column }}::jsonb ->> '{{ field }}')::{{ data_type }}

{%- endmacro %}