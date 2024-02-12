{{ config(
    materialized='view',
    schema='your_schema'
) }}

select
  *
from {{ ref('raw_data') }}
