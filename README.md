# TEST_ABC
TEST_ABC is a python app used to manage data between different internal and external databases.

Currently, the implementation of this app involves more python code than raw SQL queries. In the next versions, scalability will be thoroughly considered to speed up the queries and computations.

## Installation
First step is to make sure that you have docker installed in your system. Visit [Docker](https://docs.docker.com/engine/install/) to check if your current platform supports it.

We can also assume that you have Git installed in your system. Let's just make sure you have it with this.
```bash
git version
```
If it outputs a version, then we're good to go.

Now, time to get the repository. Clone this repository:
```bash
git clone https://github.com/leonidguadalupe/byoinai.git aquila
cd aquila
```

This is a private repository for now until we have a final prototype.

Next, we need to setup the external MS Sql database. So there are a few steps that we need to do:
1. download the .bak file from George
2. create the container for the MSSQL server. You need to do a docker pull first on the MSSQL 2019 image.
```bash
docker pull mcr.microsoft.com/mssql/server:2019-latest
```
3. Then create the aquila-mssql container by running this in your command line.
```bash
docker run \
    --rm \
	--name aquila-mssql \
	-e "ACCEPT_EULA=Y" \
	-e "SA_PASSWORD=<your_password>" \
	-e "MSSQL_AGENT_ENABLED=true" \
	-e "-e MSSQL_PID=Developer" \
	-v sqldata:/var/opt/mssql/data \
	-v $PWD/backup:/backup \
	-p 1433:1433 \
	-d mcr.microsoft.com/mssql/server:2019-latest
```
Take note of the password because you will need it later for the migrate.load file.

Also, you have to make sure that 1433 is not occupied btw. so maybe you can do a:
```bash
lsof -i -P -n | grep 1433
```
if there are some, kill those processes.

4. using the helpers folders, restore the the bak file by doing:
```bash
./helper/restore.sh CONTAINER_NAME DATABASE_NAME BACKUP_NAME
```

Then, we need to get the schema of the external database across the lake postgres database.
One way to do this is to use pgloader with the migrate.load file.

In backup folder, this is how migrate.load file looks like
```bash
load database
    from mssql://SA:<mssqlpassword>@<your.docker.host.IP>/mssqldb
    into postgresql://aquila:<lakepostgrespassword>@<postgres_host_name>:5432/<postgres_db_name>
    alter schema 'dbo' rename to 'public'
set work_mem to '1024MB', maintenance_work_mem to '1024MB';
```
modify that file with the necessary info. and make an .env file as well and make sure you have similar info with the env file you will be making. 

Here's an example of a .env file that you need to have setup in the root directory of your project:
```bash
LAKE_DB_NAME=lake
LAKE_DB_USER=aquila
LAKE_DB_PASSWORD=pa33sw0rd
LAKE_DB_HOST=db
LAKE_DB_PORT=5433
MART_DB_NAME=mart
MART_DB_USER=aquila
MART_DB_PASSWORD=pa33sw0rd
MART_DB_HOST=db_mart
MART_DB_PORT=5432
LAKE_MSSQL_DB_NAME=mssqldb
LAKE_MSSQL_DB_USER=SA
LAKE_MSSQL_DB_PASSWORD=p@ssw0rdm1cr0s0ft
LAKE_MSSQL_DB_HOST=docker.for.mac.localhost
```

After adding all those information, we need to build the docker-compose yaml file. You need to create the docker volumes first though so do:
```bash
docker volume create store_lake
docker volume create store_mart
docker volume create aquila_logs
docker volume create aquila_celery_logs
```
Then start building the images from the compose file. Do it by entering:
```bash
build
```

After build, you can now launch the containers for your app.
```bash
up
```
You can now move the data from the external database. So, let's login to our postgres lake container:
```bash
docker exec -it postgreslake sh
```

then we run
```bash
pgloader migrate.load
```
For demo sake, you need to delete all the entries in lake postgres to see that the data from external moves to internal. so we login to lake and do delete

```bash
docker exec -it postgreslake sh
psql -U aquila lake
delete from departments; delete from events; delete from instrument; delete from instrument_group;
```

You need to login to the aquila container with the django app to migrate your database.
```bash
docker exec -it aquila sh
python3 manage.py migrate
```
Now, go to http://localhost:8000/api/v1/create and submit a sync.. you can check if it loads by logging in to postgreslake container

