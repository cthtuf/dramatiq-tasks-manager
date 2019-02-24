import logging
from functools import lru_cache

from django.conf import settings

from apscheduler.util import ref_to_obj as getactorfunc_by_path
from dramatiq.actor import Actor
from redis import Redis

from typing import Union

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
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


@lru_cache(maxsize=1)
def get_actor_apschedulerpath_by_name(actor_name: str) -> Union[str, None]:
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
        return None


@lru_cache(maxsize=1024)
def getactor_by_name(actor_name: str) -> Union[Actor, None]:
    """
    Get Actor method by actor_name
    :param actor_name:
    :return:
    """
    actor_path = None
    try:
        actor_path = get_actor_apschedulerpath_by_name(actor_name)
        return getactorfunc_by_path(actor_path)
    except Exception:
        logger.exception('Cant get actor by name', extra={'actor_name': actor_name, 'actor_path': actor_path})
        return None
