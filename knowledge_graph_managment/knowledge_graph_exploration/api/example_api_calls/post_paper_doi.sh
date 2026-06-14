#! /bin/bash -xe

curl -X 'POST' 'http://0.0.0.0:5742/get_dataset_information_by_paper_doi' \
     -H 'Content-Type: application/json' \
     -d '{"paper_dois":["http://orkg.org/orkg/resource/R576987","https://doi.org/10.1016/j.websem.2005.06.005"]}'
