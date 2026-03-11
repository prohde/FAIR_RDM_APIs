# api documentation

The api presented here contain the route for the integration of datasets

## routes

integration [POST]

# Integration dataset metadata into a set template.
## Example of Input Mapping
```json
{
  "source":"openaire.json",
  "owner":"openaire",
  "iterator":"$.results[*]",
  "properties": [
    {"source_property":"mainTitle","ldm_property":"title"},
    {"source_property":"descriptions","ldm_property":"description"},
    {"source_property":"language.label","ldm_property":"language"}
  ],
  "resources":{
    "iterator":"", 
    "properties":[
      {"source_resource_property":"formats","ldm_resource_property":"format"}, 
      {"source_resource_property":"publicationDate","ldm_resource_property":"publicationDate"},   
      {"source_resource_property":"embargoEndDate","ldm_resource_property":"embargoPeriod.end"}
    ]
  }
}
```
## Example of Source Data
```json
[
  {
            "mainTitle": "Alexander Pope to Richard Boyle, 3rd earl of Burlington, 1716–1744 [popealOU0030517a1c]",
            "subTitle": null,
            "descriptions": null,
            "language": {
                "code": "eng",
                "label": "English"
            },
            "publicationDate": "2025-03-01",
            "publisher": "Bodleian Libraries, University of Oxford",
            "embargoEndDate": null,
            "sources": [
                "Crossref"
            ],
            "formats": null,
            "contributors": null,
            "coverages": null,
            "bestAccessRight": null,
            "container": null,
            "documentationUrls": null,
            "codeRepositoryUrl": null,
            "programmingLanguage": null,
            "contactPeople": null,
            "contactGroups": null,
            "tools": null,
            "size": null,
            "version": null,
            "geoLocations": null,
            "dateOfCollection": null,
            "lastUpdateTimeStamp": null,
            "indicators": {
                "citationImpact": {
                    "citationCount": 0.0,
                    "influence": 2.583162e-09,
                    "popularity": 3.0103313e-09,
                    "impulse": 0.0,
                    "citationClass": "C5",
                    "influenceClass": "C5",
                    "impulseClass": "C5",
                    "popularityClass": "C5"
                }
            },
            "projects": null,
            "organizations": null,
            "communities": null,
            "collectedFrom": [
                {
                    "key": "openaire____::081b82f96300b6a6e3d282bad31cb6e2",
                    "value": "Crossref"
                }
            ]
        }
]
```
## Example of Output
```json
[
  {
        "title": "Alexander Pope to Richard Boyle, 3rd earl of Burlington, 1716–1744 [popealOU0030517a1c]",
        "description": null,
        "language": "English",
        "resources": [
            {
                "format": null,
                "cpublicationDate": "2025-03-01",
                "embargoEndDate" : null
            }
        ]
    }
]
```

## POST request example
```bash
curl -X POST http://127.0.0.1:8001/integration \
  -F "mapping=/home/enrique/Documents/LDM_API/data_sources/integration/input_openaire.json" \
  -F "output=/home/enrique/Documents/LDM_API/data_sources/integration"
```

## Parameters
- mapping: Indicates the path to the input mapping file.
- output: Indicates path to the folder where the output file will be generated.