```console 
pip freeze > requirements.txt
```

```console 
python manage.py shell
```

```console 
python manage.py migrate
```

```console 
docker-compose build

docker-compose up -d

docker-compose logs -f

docker-compose exec web bash

docker-compose run --rm web bash

docker-compose exec web python manage.py shell
```



```console 
docker-compose exec celery_worker bash

telnet 127.0.0.1 6915

(pdb) args

(pdb) help

(pdb) c

docker-compose down -v

docker-compose up -d --build

docker-compose down -v

docker-compose up -d --build

docker-compose logs -f

docker-compose exec web bash

python manage.py shell
```

```console 
docker-compose exec web bash
python manage.py shell
```


```console 
docker-compose exec web python manage.py shell
```


```console 
docker-compose stop

docker-compose -f docker-compose.yml -p django-web up -d --build

docker-compose -f docker-compose.yml -p django-web logs -f
```

# cleanup
```console 
docker-compose -f docker-compose.yml -p django-web stop
```

# delete containers and volumes
```console 
docker-compose -f docker-compose.yml -p django-web down -v
```

# verify
```console 
docker-compose -f docker-compose.yml -p django-web ps
```

Name Command State Ports
------------------------------

```console 
docker-compose -f docker-compose.yml -p django-web exec web python manage.py shell

docker-compose -f docker-compose.yml -p django-web stop

docker-compose -f docker-compose.yml -p django-web up -d --build

docker-compose -f docker-compose.yml -p django-web exec web python manage.py shell
```

