#! /bin/bash -xe

curl -X 'POST' 'http://0.0.0.0:5742/get_dataset_information_by_author_ldm_id' \
     -H 'Content-Type: application/json' \
     -d '{"author_ldm_ids":["https://research.tib.eu/ldm/6","https://research.tib.eu/ldm/1731"]}'
