# FAIR_RDM_APIs
[TODO] infotext

# 1) Return Datasets in correlation to a DOI
## Input
```json

```
## Output
```json
{
  "doi": "http://orkg.org/orkg/resource/TR3",
  "results": [
    {
      "dataset": "https://research.tib.eu/ldm/9e7d3aa5-120c-499e-83b9-28c45b79060f",
      "author": "https://research.tib.eu/ldm/17",
      "author_label": "Anna Beer",
      "title": "LDM Demo",
      "contact_person": "nodeID://b10200",
      "license": "http://www.opendefinition.org/licenses/cc-by-sa"
    },
    {
      "dataset": "https://research.tib.eu/ldm/9e7d3aa5-120c-499e-83b9-28c45b79060f",
      "author": "https://research.tib.eu/ldm/18",
      "author_label": "Mauricio Brunet",
      "title": "LDM Demo",
      "contact_person": "nodeID://b10200",
      "license": "http://www.opendefinition.org/licenses/cc-by-sa"
    },
    {
      "dataset": "https://research.tib.eu/ldm/9e7d3aa5-120c-499e-83b9-28c45b79060f",
      "author": "https://research.tib.eu/ldm/19",
      "author_label": "Vibhav Srivastava",
      "title": "LDM Demo",
      "contact_person": "nodeID://b10200",
      "license": "http://www.opendefinition.org/licenses/cc-by-sa"
    },
    {
      "dataset": "https://research.tib.eu/ldm/9e7d3aa5-120c-499e-83b9-28c45b79060f",
      "author": "https://research.tib.eu/ldm/20",
      "author_label": "Maria-Esther Vidal",
      "title": "LDM Demo",
      "contact_person": "nodeID://b10200",
      "license": "http://www.opendefinition.org/licenses/cc-by-sa"
    }
  ]
}
```
## GET request example
```bash
curl -X 'GET' 'http://127.0.0.1:5000/get_paper_info_by_doi?doi=http://orkg.org/orkg/resource/TR3'
```
# 2) Return Datasets in correlation with several DOI
## Input
```json
```
## Output
```json
```
## GET request example
```bash
```
# 3) Return Datasets in correlation to a Authors ORCID
## Input
```json
```
## Output
```json
```
## GET request example
```bash
```
# 4) Return Datasets that cite a Dataset in correlation to the Authors ORCID
## Input
```json
```
## Output
```json
```
## GET request example
```bash
```
