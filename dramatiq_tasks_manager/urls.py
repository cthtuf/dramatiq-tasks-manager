from django.urls import path

from .views import ExecuteTaskView, ExecutedListTaskView, ExecuteDetailTaskView, ScheduleJobsListCreateView

urlpatterns = [
    path('execute', ExecuteTaskView.as_view()),
    path('executed', ExecutedListTaskView.as_view()),
    path('executed/<str:id>', ExecuteDetailTaskView.as_view()),
    path('schedule', ScheduleJobsListCreateView.as_view()),
]
