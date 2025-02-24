# Project for integration Gitlab CI into FastAPI project

## The Pipeline contains
* Build
* Mypy - Linter
* Pytest - Testing
* Bandit - is a tool designed to find common security issues in Python code. + downloadable log artifacts
* Safely - is a Python dependency vulnerability scanner. + downloadable log artifacts

![images/pipeline.png](/images/pipeline.png)
![images/coverage.png](/images/coverage.png)

### Clone the repo
```shell
git clone project_url
```
### Generate ED25519 public and private keys in certs/ directory
```shell
mkdir certs/ && cd certs/
openssl genpkey -algorithm Ed25519 -out private_key.pem
openssl pkey -in private_key.pem -pubout -out public_key.pem
```
### Rename .env.template to .env
```shell
 mv .env.template .env
```
### Adjust Access token expiration
```shell
APP_CONFIG__AUTH__ACCESS_TOKEN_EXPIRES_IN_MINUTES=45 # minutes
```
### Modify project name and sqlite3 db name
```shell
APP_CONFIG__DB__URL=sqlite:///{DB_NAME}
APP_CONFIG__PROJECT_NAME=Your-project-name
```
### Run the server
```shell
python3 main.py
```
### Endpoints:
```http request
POST  /api/v1/users/create-user/              # create user
GET  /api/v1/users/user/{user_id}             # get user by id
PATCH  /api/v1/users/user/{user_id}           # update users data
DELETE  /api/v1/users/user/{user_id}          # delete a user
GET  /api/v1/users/me                         # get info 

POST  /api/jwt/login/                         # issue a jwt bearer token
