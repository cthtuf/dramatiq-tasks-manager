from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

GROUP_TASK_SCHEDULERS = 'TASK_SCHEDULERS'
GROUP_TASK_EXECUTORS = 'TASK_EXECUTORS'
GROUP_TASK_REPORTERS = 'TASK_REPORTERS'
TASKS_GROUPS = (GROUP_TASK_SCHEDULERS, GROUP_TASK_EXECUTORS, GROUP_TASK_REPORTERS)


class TaskExecutePermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        # Check on create or edit permissions
        if request.user.groups.filter(name=GROUP_TASK_EXECUTORS).exists():
            return True

        # Check on read permissions for reporters
        if request.method in SAFE_METHODS and request.user.groups.filter(name=GROUP_TASK_REPORTERS).exists():
            return True

        return False


class TaskSchedulePermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        # Check on create or edit permissions
        if request.user.groups.filter(name=GROUP_TASK_SCHEDULERS).exists():
            return True

        # Check on read permissions for reporters
        if request.method in SAFE_METHODS and request.user.groups.filter(name=GROUP_TASK_REPORTERS).exists():
            return True

        return False
