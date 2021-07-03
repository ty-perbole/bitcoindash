WITH

whirlpool_tx AS (
SELECT
    tx_hash
  , pool
FROM(
SELECT
    tx.hash AS tx_hash
  , input_count
  , output_count
  , CASE
     WHEN output_value * (1e-8) / 5 = 0.001 THEN '100K'
      WHEN output_value * (1e-8) / 5 = 0.01 THEN '1M'
      WHEN output_value * (1e-8) / 5 = 0.05 THEN '5M'
      WHEN output_value * (1e-8) / 5 = 0.5 THEN '50M' ELSE 'Other' END AS pool

  , COUNT(DISTINCT IF(inputs.value * (1e-8) BETWEEN 0.001 AND 0.00105, inputs.index, NULL)) AS num_inputs_0001_ish
  , COUNT(DISTINCT IF(inputs.value * (1e-8) BETWEEN 0.01 AND 0.0105, inputs.index, NULL)) AS num_inputs_001_ish
  , COUNT(DISTINCT IF(inputs.value * (1e-8) BETWEEN 0.05 AND 0.0505, inputs.index, NULL)) AS num_inputs_005_ish
  , COUNT(DISTINCT IF(inputs.value * (1e-8) BETWEEN 0.5 AND 0.505, inputs.index, NULL)) AS num_inputs_05_ish

  , COUNT(DISTINCT IF(outputs.value * (1e-8) = 0.001, outputs.index, NULL)) AS num_output_0001
  , COUNT(DISTINCT IF(outputs.value * (1e-8) = 0.01, outputs.index, NULL)) AS num_output_001
  , COUNT(DISTINCT IF(outputs.value * (1e-8) = 0.05, outputs.index, NULL)) AS num_output_005
  , COUNT(DISTINCT IF(outputs.value * (1e-8) = 0.5, outputs.index, NULL)) AS num_output_05
FROM `bigquery-public-data.crypto_bitcoin.transactions` AS tx,
      tx.inputs AS inputs,
      tx.outputs AS outputs
WHERE block_timestamp_month >= "2019-01-01"
GROUP BY
    1, 2, 3, 4
HAVING
    input_count = 5 AND output_count = 5
    AND (
    num_output_05 = 5 OR num_output_005 = 5
    OR num_output_001 = 5 OR num_output_0001 = 5)
    AND (
    (num_inputs_05_ish = 5 AND num_output_05 = 5)
    OR (num_inputs_005_ish = 5 AND num_output_005 = 5)
    OR (num_inputs_001_ish = 5 AND num_output_001 = 5)
    OR (num_inputs_0001_ish = 5 AND num_output_0001 = 5))
    )
GROUP BY
    1, 2)
    ,

coinjoin_output AS (
  SELECT
    transactions.HASH AS transaction_hash,
    transactions.block_number AS created_block_number,
    transactions.block_timestamp AS created_block_ts,
    outputs.index AS output_index,
    outputs.value AS output_value,
    cj.pool AS cj_pool,
  FROM
    `bigquery-public-data.crypto_bitcoin.transactions` AS transactions,
    transactions.outputs AS outputs
  JOIN
    whirlpool_tx cj
  ON
    transactions.hash = cj.tx_hash
  WHERE block_timestamp_month >= "2019-01-01"
  GROUP BY
      1, 2, 3, 4, 5, 6
    ),

input AS (
  SELECT
    transactions.hash AS spending_transaction_hash,
    inputs.spent_transaction_hash AS spent_transaction_hash,
    transactions.block_number AS destroyed_block_number,
    transactions.block_timestamp AS destroyed_block_ts,
    inputs.spent_output_index,
    inputs.value AS input_value
  FROM
    `bigquery-public-data.crypto_bitcoin.transactions` AS transactions,
    transactions.inputs AS inputs
  WHERE block_timestamp_month >= "2019-01-01"
  GROUP BY
      1, 2, 3, 4, 5, 6
    ),

txs AS (
  SELECT
    co.transaction_hash,
    co.created_block_number,
    DATETIME(co.created_block_ts) AS created_block_ts,
    input.spending_transaction_hash,
    input.spent_transaction_hash,
    input.destroyed_block_number,
    DATETIME(input.destroyed_block_ts) AS destroyed_block_ts,
    co.output_index,
    co.output_value,
    co.cj_pool AS cj_pool
  FROM
    coinjoin_output co
  LEFT JOIN
    input
  ON
    co.transaction_hash = input.spent_transaction_hash
    AND co.output_index = input.spent_output_index
  GROUP BY
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10
  ),

blocks AS (
  SELECT
    DATE(blocks.timestamp) AS date,
    -- Get last block per day
    MAX(blocks.number) AS block_number,
    MAX(DATETIME(blocks.timestamp)) AS block_ts,
  FROM
    `bigquery-public-data.crypto_bitcoin.blocks` AS blocks
  WHERE blocks.timestamp >= "2019-01-01"
  GROUP BY
    date)

SELECT
  date,
  block_number,
  block_ts,

  SUM(output_value * 1e-8) AS unspent_capacity_samourai,
  SUM(IF(cj_pool = '50M', output_value, 0)) * 1e-8 AS unspent_capacity_samourai_50M,
  SUM(IF(cj_pool = '5M', output_value, 0)) * 1e-8 AS unspent_capacity_samourai_5M,
  SUM(IF(cj_pool = '1M', output_value, 0)) * 1e-8 AS unspent_capacity_samourai_1M,
  SUM(IF(cj_pool = '100K', output_value, 0)) * 1e-8 AS unspent_capacity_samourai_100K,
  SUM(IF(cj_pool IN ('50M', '5M', '1M', '100K'), 0, output_value)) * 1e-8 AS unspent_capacity_samourai_other,
FROM
  blocks
CROSS JOIN
  txs
WHERE
  -- CJ output was created in this block or earlier
  blocks.block_number >= txs.created_block_number
  -- CJ output was spent in a later block or remains unspent
  AND (
    blocks.block_number < txs.destroyed_block_number
    OR txs.destroyed_block_number IS NULL)
GROUP BY
  date, block_number, block_ts
ORDER BY
  date ASC;