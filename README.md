# Kids First OMOP CommonDataModel
Experimentation with the OMOP CommonDataModel.

Currently the source code consists of a simple CLI to interact with the omop db.

## Getting Started - Users

### Install
```
pip install -e git+https://github.com/kids-first/kf-model-omop.git#egg=kf-model-omop
```

### Use a Local OMOP database
Create and start new postgres Docker container
```
docker container run -d -p 5432:5432 --name=omop-pg postgres:10
```
On subsequent starts and stops use:
```
docker container start omop-pg
docker container stop omop-pg
```

Create the OMOP database
```
export OMOP_CONFIG=development
kfmodel create_omop
```

Run the following to view other commands:
```
kfmodel --help
```

or to view help for subcommands:

```
kfmodel <command> --help
```

### Use a Remote OMOP database
If you'd like to use the CLI with a remote Postgres database, configure the
following environment variables:

- `PG_HOST` - the host postgres is running on
- `PG_PORT` - the port postgres is listening on
- `PG_NAME` - the name of the database in postgres
- `PG_USER` - the postgres user to connect with
- `PG_PASS` - the password of the user

------------------------------------------------------------------------
## Getting Started - Developers

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
Install min dependencies and CLI
```
pip install -e .
```
Install docs dependencies (needed to generate ERD)
```
pip install -r doc-requirements.txt
```

### Test
Follow steps above to create and start a Dockerized Postgres container

Then create the test database:
```
docker container exec omop-pg psql -U postgres -c "CREATE DATABASE test;"
```

Install dependencies and run tests
```
pip install -r dev-requirements.txt
python -m pytest tests
```
