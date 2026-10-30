
{{ config(materialized='view') }}

WITH ranked_traders AS (
    SELECT
        trader_id,
        TRIM(full_name) AS full_name,
        NULLIF(LOWER(TRIM(email)), '') AS email,
        CAST(registered_at AS DATE) AS registered_at,

        ROW_NUMBER() OVER (
            PARTITION BY trader_id
            ORDER BY registered_at DESC NULLS LAST
        ) AS row_num

    FROM {{ source('crypto_raw', 'traders') }}

    WHERE trader_id IS NOT NULL
)

SELECT
    trader_id,
    full_name,
    email,
    registered_at

FROM ranked_traders
WHERE row_num = 1
