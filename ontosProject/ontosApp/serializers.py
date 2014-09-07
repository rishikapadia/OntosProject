from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('firstName', 'lastName', 'username', 'email', 'top10hits', 'metadata')

