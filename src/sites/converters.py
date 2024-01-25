from django.urls import converters


class RawConverter(converters.StringConverter):
    regex = ".*?"
