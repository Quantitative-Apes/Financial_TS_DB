# Financial time series database

## Install

- Download QuestDB from [here](https://questdb.io/get-questdb/)
- Extract the tarball
```
tar -xvf <tarball.tar.gz>
```
- Install QuestDB
```
(questdb-path)/questdb.exe install
```
- Install dependencies
```
pip install -r requirements.txt
```
- Set environment variables
```
QUESTDB_PATH=???
```
DB_DIR is the path where the database should be stored

## Run the database

- python start_db.py

## Stop the database

- python stop_db.py

## Access web console

http://localhost:9000/