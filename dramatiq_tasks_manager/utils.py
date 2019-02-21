import logging

from django.conf import settings

from redis import Redis

logger = logging.getLogger(__name__)


def get_declared_actors() -> list:
    """
    Get the list of declared actors from Redis.
    This list is filling while dramatiq worker starts
    :return:
    """
    try:
        redis_obj = Redis(host=settings.REDIS_HOST, decode_responses=True)
        return redis_obj.hkeys(settings.REDIS_ACTORS_LIST_HASH)
    except Exception:
        logger.exception('Cant get declared actors')
        return []


def get_actor_apschedulerpath_by_name(actor_name: str) -> str:
    """
    Get the path where actor is located. It needs to apscheduler when it scheduling a job.
    :param actor_name:
    :return:
    """
    try:
        redis_obj = Redis(host=settings.REDIS_HOST, decode_responses=True)
        return redis_obj.hget(settings.REDIS_ACTORS_LIST_HASH, actor_name)
    except Exception:
        logger.exception('Cant get actor data')
        return ""
