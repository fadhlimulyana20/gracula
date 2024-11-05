from rest_framework import serializers
from .models import Campaign, SubscriberList

class CampaignSerializer(serializers.ModelSerializer):
    subscriber_lists = serializers.PrimaryKeyRelatedField(
        queryset=SubscriberList.objects.all(),
        many=True
    )

    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'subject', 'content', 'status',
            'subscriber_lists', 'scheduled_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Custom validation for Campaign fields."""
        if data.get('status') == 'scheduled' and not data.get('scheduled_time'):
            raise serializers.ValidationError({
                'scheduled_time': 'Scheduled time is required for scheduled campaigns.'
            })
        return data

    def create(self, validated_data):
        """Create a new Campaign with associated subscriber lists."""
        subscriber_lists = validated_data.pop('subscriber_lists')
        campaign = Campaign.objects.create(**validated_data)
        campaign.subscriber_lists.set(subscriber_lists)
        return campaign

    def update(self, instance, validated_data):
        """Update an existing Campaign and its subscriber lists."""
        subscriber_lists = validated_data.pop('subscriber_lists', None)
        instance = super().update(instance, validated_data)

        if subscriber_lists is not None:
            instance.subscriber_lists.set(subscriber_lists)

        return instance
