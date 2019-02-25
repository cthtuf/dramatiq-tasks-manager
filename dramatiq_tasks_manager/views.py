from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from django_dramatiq.models import Task

from .permissions import TaskExecutePermission, TaskSchedulePermission
from .serializers import (
    ExecuteTaskSerializer, ScheduleJobCronSerializer, ScheduleJobDateSerializer, ScheduleJobIntervalSerializer,
    ScheduleJobSerializer, TaskDetailSerializer, TaskListSerializer)


class ExecuteTaskView(CreateAPIView):
    permission_classes = (TaskExecutePermission, )
    serializer_class = ExecuteTaskSerializer


class ExecutedListTaskView(ListAPIView):
    permission_classes = (TaskExecutePermission,)
    serializer_class = TaskListSerializer
    queryset = Task.tasks.all()


class ExecuteDetailTaskView(RetrieveAPIView):
    permission_classes = (TaskExecutePermission, )
    serializer_class = TaskDetailSerializer
    queryset = Task.tasks.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


class ScheduleJobsListCreateView(CreateAPIView):
    permission_classes = (TaskSchedulePermission, )

    def get_serializer_class(self):
        trigger = self.request.data.get('trigger')
        if trigger == ScheduleJobSerializer.TRIGGER_DATE:
            return ScheduleJobDateSerializer
        elif trigger == ScheduleJobSerializer.TRIGGER_INTERVAL:
            return ScheduleJobIntervalSerializer
        elif trigger == ScheduleJobSerializer.TRIGGER_CRON:
            return ScheduleJobCronSerializer
        else:
            raise ValidationError(f"Unknown trigger. Should be one of {ScheduleJobSerializer.AVAILABLE_TRIGGERS}")
