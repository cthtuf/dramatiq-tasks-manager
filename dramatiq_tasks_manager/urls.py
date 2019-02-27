from django.urls import path

from .views import ExecuteTaskView, ExecutedListTaskView, ExecuteDetailTaskView, ScheduleJobsListCreateView

urlpatterns = [
    path('execute', ExecuteTaskView.as_view(), name='task_execute'),
    path('executed', ExecutedListTaskView.as_view(), name='task_executed_list'),
    path('executed/<str:id>', ExecuteDetailTaskView.as_view(), name='task_executed_detail'),
    path('schedule', ScheduleJobsListCreateView.as_view(), name='task_schedule'),
]
