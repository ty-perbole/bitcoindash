cd /home/admin/bitcoindash

/home/admin/google/google-cloud-sdk/bin/gsutil -m rsync gs://bitcoinkpis-data/data ./data

python data_cm.py
python data_node.py
python data_wp.py

/home/admin/google/google-cloud-sdk/bin/gsutil -m rsync ./data gs://bitcoinkpis-data/data
/home/admin/google/google-cloud-sdk/bin/gcloud --quiet beta app deploy