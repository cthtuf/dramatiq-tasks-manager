from django.conf import settings

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

REDIS_HOST = getattr(settings, 'REDIS_HOST', 'redis')
REDIS_ACTORS_LIST_HASH = getattr(settings, 'REDIS_ACTORS_LIST_HASH', 'dramatiqactorslist')
POSTGRESQL_HOST = getattr(settings, 'POSTRESQL_HOST', 'postgres')
RABBIT_HOST = getattr(settings, 'RABBIT_HOST', 'rabbit')
TIME_ZONE = getattr(settings, 'TIME_ZONE', 'UTC')
APSCHEDULER_JOBSTORE_DATABASE = getattr(settings, 'APSCHEDULER_JOBSTORE_DATABASE', 'scheduler')

APSCHEDULER_DEFAULT_SETTINGS = {
    # Store all scheduled tasks in postgresql database
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': f'postgresql+psycopg2://postgres:postgres@{POSTGRESQL_HOST}/{APSCHEDULER_JOBSTORE_DATABASE}'
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler_dramatiq_executor.executor:DramatiqExecutor',
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': TIME_ZONE,
}

APSCHEDULER_SETTINGS = getattr(settings, 'APSCHEDULER_SETTINGS', APSCHEDULER_DEFAULT_SETTINGS)
