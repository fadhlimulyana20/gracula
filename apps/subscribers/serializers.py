from rest_framework import serializers
from .models import Subscriber, SubscriberList

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'full_name', 'email', 'status', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']

    def validate_email(self, value):
        """Ensure email is unique, except for the current subscriber."""
        # Retrieve the subscriber ID from the context if it exists
        subscriber_id = self.instance.id if self.instance else None

        # Check if another subscriber with the same email exists
        if Subscriber.objects.filter(email=value).exclude(id=subscriber_id).exists():
            raise serializers.ValidationError("A subscriber with this email already exists.")
        
        return value
    
    def create(self, validated_data):
        """Custom create method to set initial status."""
        return Subscriber.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Allow status update only if subscriber is not deleted."""
        if instance.deleted_at:
            raise serializers.ValidationError("Cannot update a deleted subscriber.")
        return super().update(instance, validated_data)

class SubscriberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberList
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']