#! /bin/bash -xe

curl -X 'POST' 'http://0.0.0.0:5742/get_dataset_information_by_author_orcid' \
     -H 'Content-Type: application/json' \
     -d '{"author_orcids":["https://orcid.org/0000-0003-1160-8727","https://orcid.org/0000-0002-9835-4354"]}'
