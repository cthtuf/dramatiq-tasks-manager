from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from django_dramatiq.models import Task

from .permissions import TaskExecutePermission, TaskSchedulePermission
from .serializers import (
    ExecuteTaskSerializer, ScheduleJobCronSerializer, ScheduleJobDateSerializer, ScheduleJobIntervalSerializer,
    TaskDetailSerializer, TaskListSerializer)


class ExecuteTaskView(CreateAPIView):
    """
    Execute an actor with given params
    """
    permission_classes = (TaskExecutePermission, )
    serializer_class = ExecuteTaskSerializer


class ExecutedListTaskView(ListAPIView):
    """
    The list of executed tasks
    """
    permission_classes = (TaskExecutePermission,)
    serializer_class = TaskListSerializer
    queryset = Task.tasks.all()


class ExecutedDetailTaskView(RetrieveAPIView):
    """
    Details of executed task
    """
    permission_classes = (TaskExecutePermission, )
    serializer_class = TaskDetailSerializer
    queryset = Task.tasks.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


class ScheduleJobByDateView(CreateAPIView):
    """
    Schedule task in the certain date
    """
    permission_classes = (TaskSchedulePermission, )
    serializer_class = ScheduleJobDateSerializer


class ScheduleJobByIntervalView(CreateAPIView):
    """
    Schedule task to execute in certain interval of time. E.g. every 10 minutes
    """
    permission_classes = (TaskSchedulePermission, )
    serializer_class = ScheduleJobIntervalSerializer


class ScheduleJobByCronView(CreateAPIView):
    """
    Advanced schedule method. Provides the power of cron to customize execution time and period
    """
    permission_classes = (TaskSchedulePermission, )
    serializer_class = ScheduleJobCronSerializer
