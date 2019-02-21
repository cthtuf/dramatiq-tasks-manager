from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from django_dramatiq.models import Task

from .serializers import (
    ExecuteTaskSerializer, ScheduleJobCronSerializer, ScheduleJobDateSerializer, ScheduleJobIntervalSerializer,
    ScheduleJobSerializer, TaskDetailSerializer, TaskListSerializer)


class ExecuteTaskView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ExecuteTaskSerializer


class ExecutedListTaskView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TaskListSerializer
    queryset = Task.tasks.all()


class ExecuteDetailTaskView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = TaskDetailSerializer
    queryset = Task.tasks.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


class ScheduleJobsListCreateView(CreateAPIView):
    permission_classes = (AllowAny, )

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
