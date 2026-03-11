from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from SPARQLWrapper import SPARQLWrapper, JSON
import uvicorn

app = FastAPI(title="Knowledge Graph Exploration API")

ENDPOINT = "https://labs.tib.eu/sdm/ldm_kg/sparql"

class DOIRequest(BaseModel):
    dois: List[str]

class ORCIDRequest(BaseModel):
    orcid: str

def config_generation(mapping_file,output):
    config_file = "[default]\nmain_directory: .\n\n"
    config_file += "[datasets]\nnumber_of_datasets: 1\noutput_folder: " + output
    config_file += "\nremove_duplicate: yes\nall_in_one_file: no\nordered: yes\nenrichment: yes\nname: KG\n"
    config_file += "\n"
    config_file += "[dataset1]\nname: KG\n"
    config_file += "mapping: " + mapping_file + "\n"
    mapping_file = open(output + "/config.ini","w")
    mapping_file.write(config_file)
    mapping_file.close()

def execute_fuction(value, func_dic):
    func_list = {"toLower":"",
                 "tagsToList":"",
                 "edxTagsToList":"",
                 "osfApiStoragetoHtmlStorage":"",
                 "normalizeName":"",
                 "doiLink":""}
    if func_dic["function"] in func_list:
        if "toLower" == func_dic["function"]:
            value = value.lower()
        elif "tagsToList" == func_dic["function"]:
            return_value = []
            for i in value:
                return_value.append({"name": i})
            value = return_value
        elif "edxTagsToList" == func_dic["function"]:
            return_value = []
            for i in value:
                return_value.append({"name": i["name"]})
            value = return_value
        elif "osfApiStoragetoHtmlStorage" == func_dic["function"]:
            pattern = r"^https://api\.osf\.io/v2/nodes/([a-zA-Z0-9]+)/files/.*$"
            replacement = r"https://osf.io/\1/files"
            formatted_url = re.sub(pattern, replacement, value)
            if formatted_url == value:
                return "Error: URL did not match expected API format."
            value = formatted_url
        elif "normalizeName" == func_dic["function"]:
            if "," in value:
                temp_value_list = value.split(",")
                value = temp_value_list[1] + " " + temp_value_list[0]
        elif "doiLink" == func_dic["function"]:
            value = "https://doi.org/" + value
    return value

def get_dataset_attributes_by_paper_doi_helper(input_paper_doi: str):
    sparql = SPARQLWrapper(ENDPOINT)

    query = f"""
    PREFIX rdfs:     <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dcat:     <http://www.w3.org/ns/dcat#>
    PREFIX dct:      <http://purl.org/dc/terms/>
    PREFIX datacite: <http://purl.org/spar/datacite/>
    PREFIX vcard:    <http://www.w3.org/2006/vcard/ns#>

    SELECT DISTINCT
      ?dataset ?doi ?author ?author_label ?title ?contact_person ?license
    WHERE {{
      bind (<{input_paper_doi}> as ?doi)
      ?dataset    a                         dcat:Dataset .
      ?dataset    datacite:isDescribedBy    ?doi .
      optional {{
        ?dataset dct:creator ?author .
        ?author rdfs:label ?author_label
      }} .
      optional {{ ?dataset dct:title ?title }} .
      optional {{ ?dataset vcard:fn ?contact_person }} .
      optional {{ ?dataset dct:license ?license }} .
    }}
    """

    print(query)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        bindings = results["results"]["bindings"]

        return [{k: v['value'] for k, v in row.items()} for row in bindings]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SPARQL Error: {str(e)}")

def get_dataset_attributes_by_several_paper_doi_helper(input_paper_doi_list: List[str]):
    sparql = SPARQLWrapper(ENDPOINT)

    formatted_dois = " ".join([f"<{d}>" for d in input_paper_doi_list])

    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX datacite: <http://purl.org/spar/datacite/>
    PREFIX vcard:    <http://www.w3.org/2006/vcard/ns#>

    SELECT DISTINCT
      ?dataset ?doi ?author ?author_label ?title ?contact_person ?license
    WHERE {{
      VALUES ?doi {{ {formatted_dois} }}
      ?dataset    a                         dcat:Dataset .
      ?dataset    datacite:isDescribedBy    ?doi .
     optional {{
        ?dataset dct:creator ?author .
        ?author rdfs:label ?author_label
      }} .
      optional {{ ?dataset dct:title ?title }} .
      optional {{ ?dataset ?contact_person }} .
      optional {{ ?dataset dct:license ?license }} .
    }}
    """

    # print(query)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        bindings = results["results"]["bindings"]

        return [{k: v['value'] for k, v in row.items()} for row in bindings]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SPARQL Error: {str(e)}")

def get_dataset_attributes_by_author_orcid_helper(orcid: str):
    sparql = SPARQLWrapper(ENDPOINT)

    # get the ldm id of a author from the orcid
    author_query = f"""
    PREFIX pro: <http://purl.org/spar/pro/>

    SELECT DISTINCT ?author
    WHERE {{
        ?author rdf:type pro:Author .
        ?author owl:sameAS <{orcid}> .
    }}
    """

    #print(query)

    sparql.setQuery(author_query)
    sparql.setReturnFormat(JSON)

    try:
        author_id = sparql.query().convert()["results"]["bindings"][0]["author"]["value"]

        dataset_query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX datacite: <http://purl.org/spar/datacite/>
        PREFIX pro: <http://purl.org/spar/pro/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT
          ?dataset ?author ?author_label ?orcid ?title ?contact_person ?license
        WHERE {{
          BIND (<{author_id}> as ?author)
          ?author     rdf:type             pro:Author .
          ?author     owl:sameAS           ?orcid .
          ?author     rdfs:label           ?author_label .
          ?dataset    rdf:type             dcat:Dataset .
          ?dataset    dct:creator          ?author .
          ?dataset    dct:title            ?title .
          optional {{ ?dataset vcard:fn ?contact_person }} .
          optional {{ ?dataset dct:license ?license }} .
        }}
        """

        # print(dataset_query)

        sparql.setQuery(dataset_query)
        sparql.setReturnFormat(JSON)

        try:
            bindings = sparql.query().convert()["results"]["bindings"]

            return [{k: v['value'] for k, v in row.items()} for row in bindings]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"SPARQL Error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SPARQL Error: {str(e)}")
    return {}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {}

@app.get("/get_dataset_attributes_by_paper_doi")
async def get_dataset_attributes_by_paper_doi(doi: str = Query(..., description="return papers belonging to a doi")):
    data = get_dataset_attributes_by_paper_doi_helper(doi)

    if not data:
        raise HTTPException(status_code=404, detail="no paper found with that DOI.")

    return {"doi": doi, "results": data}

@app.post("/get_dataset_attributes_by_paper_doi")
async def get_dataset_attributes_by_paper_doi(request: DOIRequest):
    if not request.dois:
        raise HTTPException(status_code=400, detail="DOI list cannot be empty.")

    data = get_dataset_attributes_by_several_paper_doi_helper(request.dois)

    if not data:
        raise HTTPException(status_code=404, detail="no paper found with that DOI.")

    return {
        "requested_count": len(request.dois),
        "found_count": len(data),
        "results": data
    }

@app.get("/get_dataset_attributes_by_author_orcid")
async def get_dataset_attributes_by_author_orcid(orcid: str = Query(..., description="return papers belonging to a doi")):
    data = get_dataset_attributes_by_author_orcid_helper(orcid)

    if not data:
        raise HTTPException(status_code=404, detail="no dataset found in correlation to that author.")

    return {"orcid": orcid, "results": data}

@app.post("/get_dataset_attributes_by_author_orcid")
async def get_dataset_attributes_by_author_orcid(request: ORCIDRequest):
    if not request.orcid:
        raise HTTPException(status_code=400, detail="ORCID can not be empty.")

    data = get_dataset_attributes_by_author_orcid_helper(request.orcid)

    if not data:
        raise HTTPException(status_code=404, detail="no dataset found in correlation to that author.")

    return {"orcid": request.orcid, "results": data}

@app.route("/integration", methods=["POST"])
def metadata_parser():
    ldm_list_datasets = []
    mapping = request.form.get("mapping")
    output = request.form.get("output")

    with open(mapping, "r") as file:
        property_list = json.load(file)
        with open(property_list["source"], "r") as source_file:
            metadata = json.load(source_file)
            jsonpath_expr = parse(property_list["iterator"])
            datasets = [match.value for match in jsonpath_expr.find(metadata)]
            for row in datasets:
                ldm_dataset = {}
                for dic_property in property_list["properties"]:
                    if dic_property["ldm_property"] == "authors":
                        jsonpath_expr = parse(dic_property["source_property"])
                        matches = [match.value for match in jsonpath_expr.find(row)]
                        if len(matches) > 1:
                            ldm_dataset["extra_authors"] = []
                        ldm_dataset["author"] = ""
                        if matches != []:
                            for value in matches:
                                if value == matches[0]:
                                    if "transformation_function" in dic_property:
                                        new_value = execute_fuction(value,dic_property["transformation_function"])
                                        ldm_dataset["author"] = new_value
                                    else:
                                        ldm_dataset["author"] = value
                                else:
                                    if "transformation_function" in dic_property:
                                        new_value = execute_fuction(value,dic_property["transformation_function"])
                                        ldm_dataset["extra_authors"].append(new_value)
                                    else:
                                        ldm_dataset["extra_authors"].append(value)
                    elif dic_property["ldm_property"] == "keywords":
                        jsonpath_expr = parse(dic_property["source_property"])
                        matches = [match.value for match in jsonpath_expr.find(row)]
                        if len(matches) > 1:
                            ldm_dataset["keywords"] = []
                            for value in matches:
                                if "transformation_function" in dic_property:
                                    new_value = execute_fuction(value,dic_property["transformation_function"])
                                    ldm_dataset["keywords"].append(new_value)
                                else:
                                    ldm_dataset["keywords"].append(value)
                    else:
                        jsonpath_expr = parse(dic_property["source_property"])
                        matches = [match.value for match in jsonpath_expr.find(row)]
                        if matches[0] != None:
                            if "transformation_function" in dic_property:
                                value = execute_fuction(matches[0],dic_property["transformation_function"])
                                ldm_dataset[dic_property["ldm_property"]] = value
                            else:
                                ldm_dataset[dic_property["ldm_property"]] = matches[0]
                if "resources" in property_list:
                    ldm_dataset["resources"] = []
                    if property_list["resources"]["iterator"] == "":
                        resources_list = [row]
                    else:
                        jsonpath_expr = parse(property_list["resources"]["iterator"])
                        resources_list = [match.value for match in jsonpath_expr.find(row)]
                    for resource in resources_list:
                        ldm_resource = {}
                        for resource_property in property_list["resources"]["properties"]:
                            jsonpath_expr = parse(resource_property["source_resource_property"])
                            matches = [match.value for match in jsonpath_expr.find(resource)]
                            if matches[0] != None:
                                if "transformation_function" in resource_property:
                                    value = execute_fuction(matches[0],resource_property["transformation_function"])
                                    ldm_resource[resource_property["ldm_resource_property"]] = value
                                else:
                                    ldm_resource[resource_property["ldm_resource_property"]] = matches[0]
                        ldm_dataset["resources"].append(ldm_resource)
                if ldm_dataset["author"] != "" and "title" in ldm_dataset:
                    print(ldm_dataset["title"])
                    ldm_list_datasets.append(ldm_dataset)

            with open(output + "/metadata.json", "w") as file:
                json.dump(ldm_list_datasets, file, indent=4)

            return "Metadata file generated succesfully.\n"

@app.route("/kg_creation", methods=["POST"])
def kg_creation():
    mapping = request.form.get("mapping")
    output = request.form.get("output")
    config_generation(mapping,output)
    semantify(output + "/config.ini")
    return "Knowledge Graph generated succesfully.\n"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
