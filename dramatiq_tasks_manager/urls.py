from django.urls import path

from .views import (ExecuteTaskView, ExecutedListTaskView, ExecutedDetailTaskView,
                    ScheduleJobByDateView, ScheduleJobByIntervalView, ScheduleJobByCronView)

urlpatterns = [
    path('execute', ExecuteTaskView.as_view(), name='task_execute'),
    path('executed', ExecutedListTaskView.as_view(), name='task_executed_list'),
    path('executed/<str:id>', ExecutedDetailTaskView.as_view(), name='task_executed_detail'),
    path('schedule/by_date', ScheduleJobByDateView.as_view(), name="schedule_task_by_date"),
    path('schedule/by_interval', ScheduleJobByIntervalView.as_view(), name="schedule_task_by_interval"),
    path('schedule/by_cron', ScheduleJobByCronView.as_view(), name="schedule_task_by_cron"),
]
