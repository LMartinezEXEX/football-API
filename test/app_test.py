from fastapi.testclient import TestClient
from main import app
from Database.database import *
import pytest
import urllib.parse

client = TestClient(app)

# -- Set up database --

@pytest.fixture(scope='session', autouse=True)
def init_db(request):
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    request.addfinalizer(clean_db)

# -- Tear down --

def clean_db():
    db.drop_all_tables(with_all_data=True)
    db.create_tables()

# -- Tests --

def test_root():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"v": "1.0"}

def test_ok_competition_loading():
    response = client.post("/league", json={"code": "PL"})

    assert response.status_code == 200
    assert response.json() == {"code": "PL"}

def test_repeated_competition_loading():
    response = client.post("/league", json={"code": "PL"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Competition already in database"}

def test_nonexistent_competition_code():
    response = client.post("/league", json={"code": "TIbUroNcin"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Error during competition data request"}

def test_get_players_from_competition():
    response = client.get("/PL/players")

    assert response.status_code == 200
    assert len(response.json()['players']) > 0

def test_get_players_from_team_in_competition():
    team_name = "Chelsea FC"
    response = client.get("/PL/players?in_team=" + urllib.parse.quote(team_name))

    assert response.status_code == 200
    for player in response.json()['players']:
        assert player['team'] == team_name

def test_get_players_from_team_NOT_in_competition():
    team_name = "Bayer 04 Leverkusen"
    response = client.get("/PL/players?in_team=" + urllib.parse.quote(team_name))

    assert response.status_code == 200
    assert len(response.json()['players']) == 0

def test_get_players_from_nonexistent_team_in_competition():
    team_name = "Not really a team here"
    response = client.get("/PL/players?in_team=" + urllib.parse.quote(team_name))

    assert response.status_code == 200
    assert len(response.json()['players']) == 0

def test_get_players_from_team_in_competition_with_invalid_code():
    code = 'A' * 11
    team_name = "Chelsea FC"
    response = client.get("/" + code + "/players?in_team=" + urllib.parse.quote(team_name))

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "ensure this value has at most 10 characters"

def test_get_players_from_team_in_competition_with_invalid_name():
    team_name = "C" * 51
    response = client.get("/PL/players?in_team=" + urllib.parse.quote(team_name))

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "ensure this value has at most 50 characters"

def test_get_default_team_data():
    team_name = "Chelsea FC"
    detail = "ALL"
    response = client.get("/team/{}?detail={}".format(urllib.parse.quote(team_name), urllib.parse.quote(detail)))
                          
    payload = response.json()
    assert response.status_code == 200
    assert payload['team']['name'] == team_name
    assert len(payload['team']['requested']['players']) >= 0
    assert len(payload['team']['requested']['coaches']) == 1

def test_get_players_only_team_data():
    team_name = "Chelsea FC"
    detail = "PLAYERS"
    response = client.get("/team/{}?detail={}".format(urllib.parse.quote(team_name), urllib.parse.quote(detail)))
                          
    payload = response.json()
    assert response.status_code == 200
    assert payload['team']['name'] == team_name
    assert len(payload['team']['requested']['players']) >= 0
    assert 'coaches' not in payload['team']['requested']

def test_get_coaches_only_team_data():
    team_name = "Chelsea FC"
    detail = "COACHES"
    response = client.get("/team/{}?detail={}".format(urllib.parse.quote(team_name), urllib.parse.quote(detail)))
                          
    payload = response.json()
    assert response.status_code == 200
    assert payload['team']['name'] == team_name
    assert 'players' not in payload['team']['requested']
    assert len(payload['team']['requested']['coaches']) == 1

def test_get_team_data_of_nonexistent_team():
    team_name = "Not really a team here"
    detail = "ALL"
    response = client.get("/team/{}?detail={}".format(urllib.parse.quote(team_name), urllib.parse.quote(detail)))
                          
    assert response.status_code == 400
    assert response.json() == {"detail": "Team is not present in the database"}

def test_get_team_data_with_invalid_name():
    team_name = "C" * 51
    detail = "ALL"
    response = client.get("/team/{}?detail={}".format(urllib.parse.quote(team_name), urllib.parse.quote(detail)))
                          
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "ensure this value has at most 50 characters"

def test_get_team_data_with_invalid_detail():
    team_name = "Chelsea FC"
    detail = "NO_VALID_OPTION"
    response = client.get("/team/{}?detail={}".format(urllib.parse.quote(team_name), urllib.parse.quote(detail)))
                          
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "value is not a valid enumeration member; permitted: 'ALL', 'PLAYERS', 'COACHES'"

def test_get_team_players():
    team_name = "Chelsea FC"
    response = client.get("/team/{}/players".format(urllib.parse.quote(team_name)))

    assert response.status_code == 200
    assert len(response.json()['players']) >= 0

def test_get_nonexistent_team_players():
    team_name = "Not really a team here"
    response = client.get("/team/{}/players".format(urllib.parse.quote(team_name)))

    assert response.status_code == 400
    assert response.json() == {"detail": "Team is not present in the database"}

def test_get_invalid_team_players():
    team_name = "C" * 51
    response = client.get("/team/{}/players".format(urllib.parse.quote(team_name)))
                          
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "ensure this value has at most 50 characters"