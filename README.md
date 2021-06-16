# team-api
This api containes logic to create team and roles based on one to many relationship between team and roles.

endpoint 1:
/get-roles/?team_name=DevOps
Method : GET
Query string : team_name
Response: 
{
    "details": [
        {
			"team_name": "DevOps",
      "role_name": "DevOpsEnginner"
        }
    ]
}
Status Code:200


endpoint 2:
/create-team
Method: POST
Payload:
{
    "team_name": "DevOps",
    "role_name": "DevOpsEnginner"
}
Response:
{"message": "Team DevOps with Role DevOpsEnginner is successfully created"}
Status Code: 201

steps to run application:
1) cd to team_api project dir
2) run command > python app.py
	it will run api on port 5000
3) send request to above endpoints using postman

DB Details:
DB name: postgresql
user name: postgres
password : testpassword
Ip : localhost
db name: testdb


tech stack:

programming language: python
frmawork: flask
orm: SQLAlchemy


