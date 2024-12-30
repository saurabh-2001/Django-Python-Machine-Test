from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Client
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.client_name')
    users = UserSerializer(many=True, read_only=True)
    user_ids = serializers.ListField(write_only=True, child=serializers.IntegerField(), required=False)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'client_name', 'users', 'user_ids', 'created_by', 'created_at']

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids', [])
        project = Project.objects.create(**validated_data)
        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            project.users.set(users)
        return project
