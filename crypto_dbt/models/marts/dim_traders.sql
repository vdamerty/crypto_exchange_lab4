
{{ config(materialized='table') }}

SELECT
    trader_id,
    full_name,
    email,
    registered_at

FROM {{ ref('stg_traders') }}
