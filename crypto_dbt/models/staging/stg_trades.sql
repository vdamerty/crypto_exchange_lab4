
{{ config(materialized='view') }}

SELECT
    trade_id,
    trader_id,
    wallet_id,
    currency_id,
    LOWER(TRIM(trade_type)) AS trade_type,
    CAST(quantity AS NUMERIC) AS quantity,
    CAST(price_usd AS NUMERIC) AS price_usd,
    CAST(total_usd AS NUMERIC) AS total_usd,
    CAST(trade_date AS TIMESTAMP) AS trade_date

FROM {{ source('crypto_raw', 'trades') }}

WHERE
    trade_id IS NOT NULL
    AND trader_id IS NOT NULL
    AND quantity > 0
    AND price_usd > 0
