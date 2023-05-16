# Santex API Challenge

This project provides a proprietary API to retrieve football data from the public http://football-data.org API.

## Installation
```shell
# Clone repo
$ git clone https://github.com/LMartinezEXEX/football-API.git && cd football-API

# Create and activate a virtual environment
$ python3 -m venv venv && source venv/bin/activate

# Install requierements
$ python -m pip install -r requirements.txt
```

## Stack

This challenge was met using two main technologies:
- [FastAPI](https://fastapi.tiangolo.com/): a simple and fast high performance framework that allows to deploy an API in a few minutes with automatic documentation. It is also a technology that I have used before and that is somehow familiar to me.
- [PonyORM](https://ponyorm.org/): To store data in a database and map it to the logic models of a small application, this simple lightweight ORM is a perfect fit. PonyORM allows you to connect to some of the most popular SQL DBMS and automatically build the schema.

## Endpoints
This API deploys 5 endpoints:

1. **GET** _"/"_: 

Base root path that returns the version of this API.
```python
{
    "v": "1.0"
}
```

2. **POST** _"/league"_: 

Load the current competition to the database with the _competition code_ provided in the request body. Due to the use of the free tier http://football-data.org token, only 10 requests per minute are allowed; this limitation was enforced through the use of [slowapi](https://github.com/laurentS/slowapi)'s limiter.

> The use of **per user limits** is not applicable because you could have 11 users at the same time poking this endpoint and collapsing the free token capabilities.

- Body: 
    - code: code of the league requested to load (e.g. `'PL'`, `'CL'`, `'PD'`).
```python
"code": str
```

- Response (`Status 200`): Same code as requested to load.
```python
"code": str
```

- Error response:
    - (`Status 400`): This could arise if the competition was already loaded and present in the database, or calling the http://football-data.org resulted in something other than `200 ok`.

3. **GET** _/{league_code}/players_: 

Retrieves an unsorted list of players from teams competing in the competition with _league\_code_. If provided, also allows filtering based on team name. 

> The returned data could also be packed by team, but in order to keep the expected results and knowing that this grouping could be done in the front, I decided to keep it simple this way.

- Path params:
    - `league_code`: code of the league to get the teams from (e.g. `'PL'`, `'CL'`, `'PD'`). **Validated** to be equal to or less than 10 chars.

- Query params:
    - `in_team` (_Optional_): team name to filter the resulting players. **Validated** (if provided) to be equal to or less than 50 chars.

> Example url: http://127.0.0.1:8000/PL/players?in_team=Arsenal%20FC

- Response (`Status 200`): Players data in an array:
```python
{
    "players": [
        {
            "name": str,
            "dateOfBirth": str,
            "position": str,
            "nationality": str,
            "team": str
        },
        ...
    ]
}
```

> If a team name is specified to filter players, the `"team"` field is not present.

- Error response:
    - `Status 400`: If `league_code` refers to a competition that wasn't loaded through the **POST** _"/league"_ endpoint.
    - `Status 422`: If at least one of the **Validated** fields are not valid.

4. **GET** _"/team/{name}"_

Get team data and, optionally, players **and** coach data of the team specified as the path parameter. This endpoint also allows to get **only** the players or **only** the coach of the team.

- Path params:
    - `name`: team name to retrieve players and/or coach information from. **Validated** to be equal to or less than 50 chars.

- Query params:
    - `detail` (_Optional_): value to decide what other team data to retrieve. Possible values:
        - `'ALL'`: Retrieves players and coach data.
        - `'PLAYERS'`: Retrieves only players data.
        - `'COACH'`: Retrieves only coach data.
    **Validated** to be only one of the values described.

> Example url: http://127.0.0.1:8000/team/Arsenal%20FC?detail=PLAYERS

- Response (`Status 200`): team data with additional requested data under the `'requested'` field:
```python
{
    "team": {
        "name": str,
        "tla": str,
        "shortName": str,
        "areaName": str,
        "address": str,
        "requested": {
            "players": [ 
                ... 
            ],
            "coach": {
                "name": str,
                "dateOfBirth": str,
                "nationality": str,
            }
        }
    }
}
```

- Error response:
    - `Status 400`: If `name` refers to a team that wasn't loaded prevously.
    - `Status 422`: If at least one of the **Validated** fields are not valid.

5. **GET** _"/team/{name}/players"_

Same functionality than the last endpoint described with `details` query parameter as `'ALL'`.

- Path params:
    - `name`: team name to retrieve players and coach information from. **Validated** to be equal to or less than 50 chars.

> Example url: http://127.0.0.1:8000/team/Arsenal%20FC/players

- Response (`Status 200`): Players and coach data:
```python
{
    "players": [
        {
            "name": str,
            "dateOfBirth": str,
            "position": str,
            "nationality": str
        },
        ...
    ],
    "coach": {
        "name": str,
        "dateOfBirth": str,
        "nationality": str,
    }
}
```

- Error response:
    - `Status 400`: If `name` refers to a team that wasn't loaded prevously.
    - `Status 422`: If at least one of the **Validated** fields are not valid.


## Considerations
-   Because of the dimensions of the data used and the overall API developed, the use of SQLite seems reasonable to me, but this could easily be changed for a powerful one with PonyORM.

-   One of the biggest differences in functionality comes from these last two endpoints. As requested, if the player list of a team is empty, the coach data should be retrieved. 

    Due to the lack of additional information and trying to model this application as close to the real world as possible, getting the coach data when asked for players, even though its emtpy, seems wrong (again from modeling a real world scenario). This is why, to fulfill the endpoint requierment, the `'ALL'` value to `detail` returns not only the players, even if its empty, but also the coach data; but this approach is flexible, because you could add more value options to `detail` to filter the requested data. At the moment only `PLAYERS'` and `COACH'` seem natural to me.

## Tests

Test for testing the endpoints are located in `test/app_test.py` and make use of [PyTest](https://docs.pytest.org/en/7.3.x/). You can run them easly inside the git cloned folder with:

```shell
$ pytest
```

## Limitations, known issues and things to enhance

- The tests use the "production" database, so any data in it would be wiped out once the tests run.

- The `dateOfBirth` field should be cast to a `Date` object to get more functionality out of it (e.g. filtering players by age).

- Revise the coach relationship with the team and the current competition. Could happens that if a team is loaded with the competition A with coach 'Roger', if competition B is loaded with a different coach the database dont gets the update.