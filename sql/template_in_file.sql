  
-- create local variable and get value from predefined global variable
{% set my_lovely_variable = yesterday_ds %}

-- create local variable and get value from xcom

SELECT
-- define for loop to generate columns
    {% for i in range(1, 5) %}
    -- jinja loop has `index` which allow us to get index of the current element
        {% if loop.index > 1 %}
         ,
        {% endif %}
        -- inside block variables must be used without {}
        {% if i%2==0 %}
            {{i}}  -- outside the block we need {} to have value evaluated.
        {% else %}
            {{i}} || 'is prime'
        {% endif %}
    {% endfor %}
    , 'my_lovely_variable=' || {{ my_lovely_variable }}
;

SELECT 1 as "{{ params.my_param }}" ;