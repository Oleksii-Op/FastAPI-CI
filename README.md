# Project for integration Gitlab CI into FastAPI project


### Clone the repo
```shell
git clone project_url
```
### Rename .env.template to .env
```shell
project_dir $ mv .env.template .env
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