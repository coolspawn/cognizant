# Weather API
https://openweathermap.org/current#name


```code 
git clone git@github.com:coolspawn/cognizant.git
```
### start project (locally in root project directory):
```code
export ENVIRONMENT=LOCAL
docker-compose -f docker-compose.local.yml up --bilid -d
uvicorn api.main:app --reload
```

#### start celery and celery_beat:

```code
celery -A api.celery_app worker [-l debug]
celery -A api.celery_app beat [-l debug]
```
### initialize database
```code
localhost:8000/init_db
```

### acess to services

rabbitMQ (test/test):
```code
localhost:15672
```
flower
```code
localhost:5555
```
clickhouse
```code
http://localhost:8123/play
```

api
```code
localhost:8000/api/v1/historical_data/Prague
```


