# telethon-flaskio

set up docker (database)

```
$docker run --name tele-db -e POSTGRES_USER=tommy -e POSTGRES_PASSWORD=0000 -e POSTGRES_DB=telegram -v tele-data:var/lib/postgresql/data -p 5432:5432 -d postgres:12-alpine
```

run application

```
$python telegram.py
```

then navigate to localhost:5000 (default port for flask)
only the buttons "message" and "connect" works now.  
