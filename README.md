# cognizant
Weather API

start project:
`docker-compose up --bilid -d`
`uvicorn main:app --reload`
`celery worker -A celery_app.worker -l info -Q test-queue -c 1`
