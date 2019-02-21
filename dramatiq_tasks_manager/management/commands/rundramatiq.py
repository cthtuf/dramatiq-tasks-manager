import redis
from django.conf import settings

from django_dramatiq.management.commands import rundramatiq


class Command(rundramatiq.Command):
    def handle(self, use_watcher, use_polling_watcher, use_gevent, path, processes, threads, verbosity, queues,
               pid_file, log_file, **options):
        self.stdout.write(' * Trying to flush actors list')
        try:
            redis_obj = redis.Redis(host=settings.REDIS_HOST)
            redis_obj.delete(settings.REDIS_ACTORS_LIST_HASH)
        except Exception as e:
            self.stdout.write(f' ! Exception on flush actors list e={e}')
        else:
            self.stdout.write(' * Actors list was flushed successfull')

        super().handle(use_watcher, use_polling_watcher, use_gevent, path, processes, threads, verbosity, queues,
                       pid_file, log_file, **options)
