
{{ config(materialized='table') }}

SELECT
    trade_id,
    trader_id,
    wallet_id,
    currency_id,
    trade_type,
    quantity,
    price_usd,
    total_usd,
    trade_date

FROM {{ ref('stg_trades') }}
