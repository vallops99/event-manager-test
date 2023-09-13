"""View's serializers."""
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    Serializer, ModelSerializer, CharField, EmailField, ChoiceField,
    BooleanField, DateField
)

from event_manager_test.app.models import Event
from event_manager_test.utils.exceptions.signup import SignUpPasswordException
from event_manager_test.utils.exceptions.event import (
    BadStartDatetimeError, BadEndDatetimeError, MaxEventCapacityError,
    UserAlreadyRegisteredError, UserNotRegisteredYetError,
    PastEventRegistrationError
)


class EventQueryParamSerializer(Serializer):
    """Event query parameters serializer."""
    date = DateField(required=False)
    user_only = BooleanField(default=False)
    past_event_only = BooleanField(default=False)
    future_event_only = BooleanField(default=False)
    e_type = ChoiceField(choices=Event.Type.choices, required=False)
    status = ChoiceField(choices=Event.Status.choices, required=False)


class SignUpSerializer(ModelSerializer):
    """
    Sign up serializer.

    `password_copy` is the 'type password again' field that will not be stored
    in DB, but just used to validate.
    """
    username = CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = EmailField(required=True)
    password = CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password_copy = CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_copy')

    def validate(self, attrs):
        # Password and "write password again" can not be different.
        if attrs.get('password') != attrs.get('password_copy'):
            raise SignUpPasswordException()

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
        )

        user.set_password(validated_data.get('password'))
        user.save()

        return user


class EventSerializer(ModelSerializer):
    """Event serializer."""
    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, attrs):
        """Validate event method."""
        # Register and de-register action will be treated differently in
        # order to updated only the `registered_users` field and avoid
        # the possibility of adding out of context information.
        # eg. editing the name of the event while registering.
        user_to_add = self.context.get('add_user')
        user_to_remove = self.context.get('remove_user')
        if user_to_add:
            users = self.instance.registered_users.filter(pk=user_to_add)

            if len(users) > 0:
                raise UserAlreadyRegisteredError()

            if self.instance.partecipants_quantity >= self.instance.capacity:
                raise MaxEventCapacityError()

            if self.instance.start_datetime.date() <= datetime.now().date():
                raise PastEventRegistrationError()

            return {'add_user': user_to_add}
        elif user_to_remove:
            users = self.instance.registered_users.filter(pk=user_to_remove)

            if len(users) < 1:
                raise UserNotRegisteredYetError()

            return {'remove_user': user_to_remove}

        now = datetime.now().date()
        end_datetime: datetime = attrs.get('end_datetime')
        start_datetime: datetime = attrs.get('start_datetime')

        # Start date can not be lower or equal today.
        if start_datetime and start_datetime.date() <= now:
            raise BadStartDatetimeError()

        # End date can not be lower or equal start date.
        if end_datetime and end_datetime <= start_datetime:
            raise BadEndDatetimeError()

        if attrs.get('registered_users'):
            del attrs['registered_users']

        return attrs

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user_to_add = validated_data.get('add_user')
        user_to_remove = validated_data.get('remove_user')

        if user_to_add:
            instance.registered_users.add(user_to_add)
            return instance
        elif user_to_remove:
            instance.registered_users.remove(user_to_remove)
            return instance

        return super().update(instance, validated_data)
