{{
    config(
        engine = 'MergeTree()',
        order_by = 'date_rep'
    )
}}

select
toDate(parseDateTimeBestEffort(date_rep)) as date_rep,
cases, deaths, geo_id
from {{source('dbgen', 'src_covid_cases')}}