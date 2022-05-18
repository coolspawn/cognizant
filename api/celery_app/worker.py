
from time import sleep

from celery import current_task

from celery_main import celery_instance


@celery_instance.task(acks_late=True)
def get_weather_data(word: str) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': i * 10})
    return f"test task return {word}"
