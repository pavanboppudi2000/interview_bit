from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import find_dotenv, load_dotenv

from server.app.config import Config

logger = get_task_logger(__name__)


load_dotenv(find_dotenv(), verbose=True)


#
# https://github.com/celery/celery/issues/2570
# celery tasks in different files is pain
#
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL,
                backend=Config.CELERY_RESULT_BACKEND)

celery.autodiscover_tasks(['server.tasks.email'])
