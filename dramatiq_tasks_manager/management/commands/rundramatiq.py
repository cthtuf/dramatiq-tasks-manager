from time import sleep

from django.conf import settings

import pika
import redis
from django_dramatiq.management.commands import rundramatiq
from pika.exceptions import ConnectionClosed as PikaConnectionClosed
from pika.exceptions import IncompatibleProtocolError


class Command(rundramatiq.Command):
    def check_connection_to_rabbit(self):
        try:
            if settings.RABBIT_HOST:
                connection_attempts = 10
                while connection_attempts > 0:
                    try:
                        conn = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBIT_HOST, 5672, '/'))
                        self.stdout.write(' * Rabbit is ready')
                        return
                    except (PikaConnectionClosed, IncompatibleProtocolError):
                        self.stdout.write(' . Seems like Rabbit not ready')
                        connection_attempts -= 1
                        sleep(2)
                self.stdout.write(f' !!! Rabbit not available after 10 attempts to connect')
                raise Exception("Can't connect to Rabbit")
        except AttributeError:
            self.stdout.write(' ! Skip waiting for Rabbit because RABBIT_HOST not set.')
            return

    def check_connection_to_redis(self):
        try:
            if settings.REDIS_HOST:
                connection_attempts = 10
                while connection_attempts > 0:
                    try:
                        rs = redis.Redis(settings.REDIS_HOST)
                        rs.client_list()
                        self.stdout.write(' * Redis is ready')
                        return
                    except Exception:
                        self.stdout.write(' . Seems like Redis not ready')
                        connection_attempts -= 1
                        sleep(2)
                self.stdout.write(f' !!! Redis not available after 10 attempts to connect')
                raise Exception("Can't connect to Redis")
        except AttributeError:
            self.stdout.write(' !!! REDIS_HOST not set in settings. ')
            raise Exception

    def wait_for_backends(self):
        """
        Waiting for Redis or\and Rabbit backends
        :return:
        """
        self.stdout.write(' * Waiting for backends')
        self.check_connection_to_redis()
        self.check_connection_to_rabbit()

    def flush_actors_list(self):
        self.stdout.write(' * Trying to flush actors list')
        try:
            redis_obj = redis.Redis(host=settings.REDIS_HOST)
            redis_obj.delete(settings.REDIS_ACTORS_LIST_HASH)
        except Exception as e:
            self.stdout.write(f' ! Exception on flush actors list e={e}')
        else:
            self.stdout.write(' * Actors list was flushed successfull')

    def handle(self, use_watcher, use_polling_watcher, use_gevent, path, processes, threads, verbosity, queues,
               pid_file, log_file, **options):
        self.wait_for_backends()
        self.flush_actors_list()

        super().handle(use_watcher, use_polling_watcher, use_gevent, path, processes, threads, verbosity, queues,
                       pid_file, log_file, **options)
