"""View's filters."""
from datetime import datetime
from rest_framework.filters import BaseFilterBackend

from event_manager_test.app.serializers import EventQueryParamSerializer


class EventFilter(BaseFilterBackend):
    """Backend event filters."""
    def filter_queryset(self, request, queryset, view):
        query = EventQueryParamSerializer(data=request.query_params)
        query.is_valid()

        filters_dict = {}

        user_only = query.validated_data.get('user_only', False)
        if user_only:
            filters_dict['owner'] = request.user.id

        # Only past_event or future_event will filter based on today's date.
        # If date is specified these fields will work together with the date.
        field_plus = ''
        if query.validated_data.get('past_event_only'):
            field_plus = '__lt'
        elif query.validated_data.get('future_event_only'):
            field_plus = '__gt'

        date = query.validated_data.get('date')
        if date or field_plus:
            field_name = f'start_datetime{field_plus}'
            date = date or datetime.now().date()

            filters_dict[field_name] = date

        e_type = query.validated_data.get('e_type')
        if e_type:
            filters_dict['e_type'] = e_type

        status = query.validated_data.get('status')
        if status:
            filters_dict['status'] = status

        return queryset.filter(**filters_dict)
