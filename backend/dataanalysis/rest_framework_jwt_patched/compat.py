from rest_framework import serializers


class Serializer(serializers.Serializer):
    @property
    def object(self):
        return self.validated_data
