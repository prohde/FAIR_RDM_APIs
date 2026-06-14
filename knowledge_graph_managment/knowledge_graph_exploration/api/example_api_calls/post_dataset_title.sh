#! /bin/bash -xe

curl -X 'POST' 'http://0.0.0.0:5742/get_dataset_information_by_dataset_title' \
     -H 'Content-Type: application/json' \
     -d '{"dataset_titles": ["Hydrochemistry measured on water bottle samples during Le Suroît cruise DYNAPROC", "Sea surface trace gases during Maria S. Merian cruise MSM105"]}'
