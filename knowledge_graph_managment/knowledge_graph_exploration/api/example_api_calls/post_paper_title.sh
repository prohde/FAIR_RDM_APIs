#! /bin/bash -xe

curl -X 'POST' 'http://0.0.0.0:5742/get_dataset_information_by_paper_title' \
     -H 'Content-Type: application/json' \
     -d '{"paper_titles": ["The Open Research Knowledge Graph", "Attention Is All You Need"]}'
