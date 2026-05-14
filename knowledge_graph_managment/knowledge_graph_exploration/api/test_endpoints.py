import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Import your FastAPI app instance
from api import app

client = TestClient(app)

# --- Common Mock Data ---
MOCK_DATA = {"https://research.tib.eu/ldm/6": {"prop": "value"}}
MOCK_EMPTY = {}


# ==========================================
# AUTHOR ORCID ENDPOINTS
# ==========================================

@patch("api.get_dataset_information_by_author_orcid_helper")
def test_get_author_orcid_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.get("/get_dataset_information_by_author_orcid?author_orcid=0000-0003-1160-8727")
    assert response.status_code == 200
    assert response.json()["author_orcid"] == "0000-0003-1160-8727"
    assert response.json()["results"] == MOCK_DATA

@patch("api.get_dataset_information_by_author_orcid_helper")
def test_get_author_orcid_not_found(mock_helper):
    mock_helper.return_value = MOCK_EMPTY
    response = client.get("/get_dataset_information_by_author_orcid?author_orcid=bad-orcid")
    assert response.status_code == 404

@patch("api.get_dataset_information_by_several_author_orcid_helper")
def test_post_author_orcid_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.post("/get_dataset_information_by_several_author_orcid", json={"author_orcids": ["0000"]})
    assert response.status_code == 200
    assert response.json()["found_count"] == 1

@patch("api.get_dataset_information_by_several_author_orcid_helper")
def test_post_author_orcid_empty_list(mock_helper):
    response = client.post("/get_dataset_information_by_several_author_orcid", json={"author_orcids": []})
    assert response.status_code == 400


# ==========================================
# AUTHOR NAME ENDPOINTS
# ==========================================

@patch("api.get_dataset_information_by_author_name_helper")
def test_get_author_name_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.get("/get_dataset_information_by_author_name?author_name=Maria")
    assert response.status_code == 200
    assert "results" in response.json()

@patch("api.get_dataset_information_by_author_name_helper")
def test_get_author_name_not_found(mock_helper):
    mock_helper.return_value = MOCK_EMPTY
    response = client.get("/get_dataset_information_by_author_name?author_name=Unknown")
    assert response.status_code == 404

@patch("api.get_dataset_information_by_several_author_name_helper")
def test_post_author_name_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.post("/get_dataset_information_by_several_author_name", json={"author_names": ["Maria"]})
    assert response.status_code == 200


# ==========================================
# AUTHOR LDM ID ENDPOINTS
# ==========================================

@patch("api.get_dataset_information_by_author_ldm_id_helper")
def test_get_author_ldm_id_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.get("/get_dataset_information_by_author_ldm_id?author_ldm_id=ldm123")
    assert response.status_code == 200

@patch("api.get_dataset_information_by_several_author_ldm_id_helper")
def test_post_author_ldm_id_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.post("/get_dataset_information_by_several_author_ldm_id", json={"author_ldm_ids": ["ldm123"]})
    assert response.status_code == 200


# ==========================================
# PAPER DOI ENDPOINTS
# ==========================================

@patch("api.get_dataset_information_by_paper_doi_helper")
def test_get_paper_doi_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.get("/get_dataset_information_by_paper_doi?paper_doi=10.123/abc")
    assert response.status_code == 200

@patch("api.get_dataset_information_by_several_paper_doi_helper")
def test_post_paper_doi_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.post("/get_dataset_information_by_several_paper_doi", json={"paper_dois": ["10.123/abc"]})
    assert response.status_code == 200


# ==========================================
# PAPER TITLE ENDPOINTS
# ==========================================

@patch("api.get_dataset_information_by_paper_title_helper")
def test_get_paper_title_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.get("/get_dataset_information_by_paper_title?paper_title=Graph Theory")
    assert response.status_code == 200

@patch("api.get_dataset_information_by_several_paper_title_helper")
def test_post_paper_title_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.post("/get_dataset_information_by_several_paper_title", json={"paper_titles": ["Graph Theory"]})
    assert response.status_code == 200


# ==========================================
# DATASET DOI ENDPOINTS
# ==========================================

@patch("api.get_dataset_information_by_dataset_doi_helper")
def test_get_dataset_doi_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.get("/get_dataset_information_by_dataset_doi?dataset_doi=10.data/123")
    assert response.status_code == 200

@patch("api.get_dataset_information_by_several_dataset_doi_helper")
def test_post_dataset_doi_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.post("/get_dataset_information_by_several_dataset_doi", json={"dataset_dois": ["10.data/123"]})
    assert response.status_code == 200


# ==========================================
# DATASET TITLE ENDPOINTS
# ==========================================

@patch("api.get_dataset_information_by_dataset_title_helper")
def test_get_dataset_title_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.get("/get_dataset_information_by_dataset_title?dataset_title=My Data")
    assert response.status_code == 200

@patch("api.get_dataset_information_by_several_dataset_title_helper")
def test_post_dataset_title_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.post("/get_dataset_information_by_several_dataset_title", json={"dataset_titles": ["My Data"]})
    assert response.status_code == 200


# ==========================================
# DATASET LDM ID ENDPOINTS
# ==========================================

@patch("api.get_dataset_information_by_dataset_ldm_id_helper")
def test_get_dataset_ldm_id_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.get("/get_dataset_information_by_dataset_ldm_id?dataset_ldm_id=ldm_data_1")
    assert response.status_code == 200

@patch("api.get_dataset_information_by_several_dataset_ldm_id_helper")
def test_post_dataset_ldm_id_success(mock_helper):
    mock_helper.return_value = MOCK_DATA
    response = client.post("/get_dataset_information_by_several_dataset_ldm_id", json={"dataset_ldm_ids": ["ldm_data_1"]})
    assert response.status_code == 200

# ==========================================
# VALIDATION ERRORS (422)
# ==========================================

def test_missing_query_parameter():
    # Calling GET without the required query parameter
    response = client.get("/get_dataset_information_by_author_orcid")
    assert response.status_code == 422
