import logging

from django.core.exceptions import ImproperlyConfigured

import redis
from dramatiq.middleware import Middleware

from .settings import REDIS_ACTORS_LIST_HASH, REDIS_HOST

logger = logging.getLogger("dramatiq_tasks_manager.SaveActorsToRedisMiddleware")


class SaveActorsToRedisMiddleware(Middleware):
    """This middleware save actors to redis for validation purpose"""

    def after_declare_actor(self, broker, actor):
        """Called after an actor has been declared."""
        host = REDIS_HOST
        actors_hash = REDIS_ACTORS_LIST_HASH
        actor_name = getattr(actor, 'actor_name', None)
        # It's dirty hack to get actor module from logger name. It could be broken if logging configuration
        # will changed. If you want to use it in production, don't hesitate to wrap this case in test
        actor_logger_name = getattr(getattr(actor, 'logger', None), 'name', "")
        actor_module = actor_logger_name.rsplit('.', 1)[0]
        if not all((host, actors_hash, )):
            logger.error('Improperly configured. To using SaveActorsToRedisMiddleware you must set REDIS_HOST and'
                         'REDIS_ACTORS_LIST_HASH value in project settings')
            raise ImproperlyConfigured()
        if not all((actor_name, actor_module)):
            logger.error('Incorrect value for actor_name or actor_module')
            raise ImproperlyConfigured()
        actor_path = ":".join((actor_module, actor_name))
        try:
            redis_obj = redis.Redis(host=host)
            redis_obj.hset(actors_hash, actor_name, actor_path)
        except Exception:
            logger.exception("Error on saving actor to redis")
        else:
            logger.info(f"Actor {actor_name}:{actor_path} saved to HASH:{actors_hash}")
