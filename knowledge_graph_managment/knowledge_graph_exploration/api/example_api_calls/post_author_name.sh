#! /bin/bash -xe

curl -X 'POST' 'http://0.0.0.0:5742/get_dataset_information_by_author_name' \
     -H 'Content-Type: application/json' \
     -d '{"author_names":["Maria-Esther Vidal","Philipp D. Rohde"]}'
