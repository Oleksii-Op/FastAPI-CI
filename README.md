# Project for integration Gitlab CI into FastAPI project

## The Pipeline contains
* Build
* Mypy - Linter
* Pytest - Testing
* Bandit - is a tool designed to find common security issues in Python code. + downloadable log artifacts
* Safely - is a Python dependency vulnerability scanner. + downloadable log artifacts


### Clone the repo
```shell
git clone project_url
```
### Rename .env.template to .env
```shell
 mv .env.template .env
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