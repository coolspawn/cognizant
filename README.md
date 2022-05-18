# cognizant
Weather API

start project:
`docker-compose up --bilid -d`
`uvicorn main:app --reload`
`celery worker -A worker.celery_worker -l info -Q test-queue -c 1`
