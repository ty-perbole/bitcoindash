cd /home/admin/bitcoindash

/home/admin/google/google-cloud-sdk/bin/gsutil -m rsync gs://bitcoinkpis-data/data ./data

python data_cm.py
python data_node.py
python data_wp.py

{
  rm lnchannels.dump
  } || {
    echo norm
}
{
  wget https://ln.bigsun.xyz/lnchannels.dump
  dropdb ln
  createdb ln
  psql ln < lnchannels.dump
  psql ln -c "\COPY (
  SELECT
      short_channel_id
    , satoshis
    , nodes::json->0 AS node1
    , nodes::json->1 AS node2
    , (open->>'time')::int AS open_ts
    , (open->>'block')::int AS open_block
    , (close->>'time')::int AS close_ts
    , (close->>'block')::int AS close_block
    , last_update
  FROM channels)
  TO '/home/admin/bitcoindash/ln_channels.csv' DELIMITER ',' CSV HEADER;"
} || {
  echo ln import failed
}

python data_ln.py

/home/admin/google/google-cloud-sdk/bin/gsutil -m rsync ./data gs://bitcoinkpis-data/data
/home/admin/google/google-cloud-sdk/bin/gcloud --quiet app deploy
