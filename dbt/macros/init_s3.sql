{% macro init_s3_sources() -%}
    {% set sources = [
    'DROP TABLE IF EXISTS src_covid_cases',
    'CREATE TABLE IF NOT EXISTS src_covid_cases (
date_rep String,
day UInt8,
month UInt8,
year UInt16,
cases UInt16,
deaths UInt16,
geo_id String
) engine = S3(\'https://storage.yandexcloud.net/ch-data-course/covid_cases/raw_covid__cases.csv\', \'CSVWithNames\')',
    'DROP TABLE IF EXISTS ref_country_codes',
    'CREATE TABLE IF NOT EXISTS ref_country_codes(
	country String,
	alpha_2code String,
	alpha_3code String,
	numeric_code UInt16,
	latitude_avg Decimal(10,4),
	longitude_avg Decimal(10,4)
) engine = S3(\'https://storage.yandexcloud.net/ch-data-course/covid_cases/reference/ref__country_codes.csv\', \'CSVWithNames\')'
    ] %}

    {% for src in sources %}
        {% set statement = run_query(src) %}
    {% endfor %}
{%- endmacro %}