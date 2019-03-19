from apscheduler.schedulers.background import BackgroundScheduler

from .settings import APSCHEDULER_SETTINGS


class Scheduler(BackgroundScheduler):
    """
    Singleton class for apscheduler.
    Scheduling will be started after first using of this class.
    """
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, BackgroundScheduler):
            cls._instance = BackgroundScheduler(APSCHEDULER_SETTINGS)
            cls._instance.start()
        return cls._instance
