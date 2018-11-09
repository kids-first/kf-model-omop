# Kids First OMOP CommonDataModel
Experimentation with the OMOP CommonDataModel.

Currently the source code consists of a simple CLI to interact with the omop db.

## Getting Started

### Setup PostgreSQL
Create and start new postgres Docker container
```
docker container run -d -p 5432:5432 --name=omop-pg postgres:10
```

On subsequent starts and stops use:
```
docker container start omop-pg
docker container stop omop-pg
```

### Setup dev environment
Get code
```
git clone git@github.com:kids-first/kf-model-omop.git
cd kf-model-omop
```
Create virtual env
```
python3 -m venv venv
source ./venv/bin/activate
```

### Install
```
pip install -e .
```

### Run
Run the following to view implemented commands:
```
kfmodel --help
```

**Note on init-db command**

This command will drop the current OMOP db, create a new one, and run the setup scripts to create the necessary OMOP tables, indices, and constraints.

Optionally you can supply the `--refresh_schema` flag to refresh the setup scripts.
This entails cloning the Kids First OMOP CommonDataModel repo and getting the latest PostgreSQL scripts.
