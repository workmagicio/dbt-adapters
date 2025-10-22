
{% macro database__list_relations_without_caching(schema_relation) %}
  {% call statement('list_relations_without_caching', fetch_result=True) %}
    select
      null,
      table_name,
      table_schema,
      case
        when table_type = 'BASE TABLE' then 'table'
        when table_type = 'VIEW' then 'view'
        else table_type
      end
    from
      information_schema.tables
    where
      table_schema = '{{ schema_relation.schema }}'
  {% endcall %}
  {{ return(load_result('list_relations_without_caching').table) }}
{% endmacro %}

{% macro database__list_schemas(database) %}
  {% call statement('list_schemas', fetch_result=True, auto_begin=False) %}
    select distinct
      schema_name
    from
      information_schema.schemata
  {% endcall %}
  {{ return(load_result('list_schemas').table) }}
{% endmacro %}
