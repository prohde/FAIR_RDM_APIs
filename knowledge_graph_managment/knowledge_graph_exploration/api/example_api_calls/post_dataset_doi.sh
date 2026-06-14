#! /bin/bash -xe

curl -X 'POST' 'http://0.0.0.0:5742/get_dataset_information_by_dataset_doi' \
     -H 'Content-Type: application/json' \
     -d '{"dataset_dois": ["https://doi.org/10.1594/PANGAEA.959660", "https://doi.org/10.1594/PANGAEA.804388"]}'
