#!/bin/bash

docker run \
	--name aquila-mssql \
	-e "ACCEPT_EULA=Y" \
	-e "SA_PASSWORD=yourStrong(!)Password" \
	-e "MSSQL_AGENT_ENABLED=true" \
	-e "-e MSSQL_PID=Developer" \
	-v sqldata:/var/opt/mssql/data \
	-v $PWD/backup:/backup \
	-p 1433:1433 \
	-d mcr.microsoft.com/mssql/server:2019-latest

