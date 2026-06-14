#! /bin/bash -xe

curl -X 'POST' 'http://0.0.0.0:5742/get_dataset_information_by_dataset_ldm_id' \
     -H 'Content-Type: application/json' \
     -d '{"dataset_ldm_ids": ["https://research.tib.eu/ldm/00023be0-7b88-4bed-9805-21259c5f2bc2", "https://research.tib.eu/ldm/00033075-0c3e-471a-a95a-f8cb52c221b5"]}'
