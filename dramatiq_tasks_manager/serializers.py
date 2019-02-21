from rest_framework import serializers

from django_dramatiq.models import Task
from dramatiq.broker import get_broker
from dramatiq.errors import ActorNotFound

from .scheduler import Scheduler
from .utils import get_actor_apschedulerpath_by_name, get_declared_actors


class ExecuteTaskSerializer(serializers.Serializer):
    actor_name = serializers.CharField(max_length=255)
    kwargs = serializers.JSONField(required=False, write_only=True)
    message_id = serializers.UUIDField(required=False, read_only=True)

    def validate_name(self, value):
        if value not in get_declared_actors():
            raise serializers.ValidationError('Unknown actor name')

        return value

    def create(self, validated_data):
        actor_name = validated_data.get('actor_name')
        kwargs = validated_data.get('kwargs', {})
        try:
            job = get_broker().get_actor(actor_name).send(**kwargs)
            return job
        except ActorNotFound as anf:
            raise serializers.ValidationError(f"Actor '{anf}' not found")
        except Exception as e:
            raise serializers.ValidationError(e)


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'status', 'created_at', 'updated_at')


class TaskDetailSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'status', 'created_at', 'updated_at', 'message')

    def get_message(self, obj):
        message = getattr(obj, 'message', None)
        return message.asdict() if message else None


class ScheduleJobSerializer(serializers.Serializer):
    TRIGGER = None
    TRIGGER_DATE = 'date'
    TRIGGER_INTERVAL = 'interval'
    TRIGGER_CRON = 'cron'
    AVAILABLE_TRIGGERS = (TRIGGER_DATE, TRIGGER_INTERVAL, TRIGGER_CRON, )

    func = serializers.CharField()

    args = serializers.ListField(default=None)
    kwargs = serializers.DictField(default=None)
    name = serializers.CharField(default=None)
    misfire_grace_time = serializers.IntegerField(default=None)
    coalesce = serializers.BooleanField(default=None)
    max_instances = serializers.IntegerField(default=1, min_value=1)
    replace_existing = serializers.BooleanField(default=False)
    # ToDo: Add timezone support

    id = serializers.CharField(default=None, required=False)
    executor = serializers.CharField(default='default')

    next_run_time = serializers.DateTimeField(read_only=True)

    def validate_func(self, value):
        declared_actors = get_declared_actors()
        if value not in declared_actors:
            raise serializers.ValidationError('Unknown actor name')
        actor_func_path = get_actor_apschedulerpath_by_name(value)
        if not actor_func_path:
            raise serializers.ValidationError('Incorrect actor path')

        return actor_func_path

    def create(self, validated_data):
        data = {**{'trigger': self.TRIGGER}, **validated_data}
        try:
            job = Scheduler().add_job(**data)
            return job
        except Exception as e:
            raise serializers.ValidationError(e)


class ScheduleJobDateSerializer(ScheduleJobSerializer):
    TRIGGER = 'date'

    run_date = serializers.DateTimeField(write_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['run_date'] = getattr(instance.trigger, 'run_date', None)

        return ret


class ScheduleJobIntervalSerializer(ScheduleJobSerializer):
    TRIGGER = 'interval'

    start_date = serializers.DateTimeField(default=None, write_only=True)
    end_date = serializers.DateTimeField(default=None, write_only=True)
    jitter = serializers.IntegerField(default=None, write_only=True)

    weeks = serializers.IntegerField(default=0, write_only=True)
    days = serializers.IntegerField(default=0, write_only=True)
    hours = serializers.IntegerField(default=0, write_only=True)
    minutes = serializers.IntegerField(default=0, write_only=True)
    seconds = serializers.IntegerField(default=0, write_only=True)

    interval_length = serializers.FloatField(read_only="True", source="trigger.interval_length")

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['start_date'] = getattr(instance.trigger, 'start_date', None)
        ret['end_date'] = getattr(instance.trigger, 'end_date', None)
        ret['jitter'] = getattr(instance.trigger, 'jitter', None)
        ret['days'] = getattr(instance.trigger.interval, 'days', None)
        ret['seconds'] = getattr(instance.trigger.interval, 'seconds', None)

        return ret


class ScheduleJobCronSerializer(ScheduleJobSerializer):
    TRIGGER = 'cron'

    start_date = serializers.DateTimeField(required=False, write_only=True)
    end_date = serializers.DateTimeField(required=False, write_only=True)
    jitter = serializers.IntegerField(default=0, min_value=0)

    year = serializers.CharField(default=None, write_only=True)
    month = serializers.CharField(default=None, write_only=True)
    week = serializers.CharField(default=None, write_only=True)
    day = serializers.CharField(default=None, write_only=True)
    day_of_week = serializers.CharField(default=None, write_only=True)
    hour = serializers.CharField(default=None, write_only=True)
    minute = serializers.CharField(default=None, write_only=True)
    second = serializers.CharField(default=None, write_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['start_date'] = getattr(instance.trigger, 'start_date', None)
        ret['end_date'] = getattr(instance.trigger, 'end_date', None)
        ret['jitter'] = getattr(instance.trigger, 'jitter', None)

        fieldname_map = {value: idx for idx, value in enumerate(getattr(instance.trigger, 'FIELD_NAMES', []))}

        ret['year'] = str(instance.trigger.fields[fieldname_map['year']])
        ret['month'] = str(instance.trigger.fields[fieldname_map['month']])
        ret['week'] = str(instance.trigger.fields[fieldname_map['week']])
        ret['day'] = str(instance.trigger.fields[fieldname_map['day']])
        ret['day_of_week'] = str(instance.trigger.fields[fieldname_map['day_of_week']])
        ret['hour'] = str(instance.trigger.fields[fieldname_map['hour']])
        ret['minute'] = str(instance.trigger.fields[fieldname_map['minute']])
        ret['second'] = str(instance.trigger.fields[fieldname_map['second']])

        return ret
