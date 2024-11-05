from rest_framework import viewsets, status
from rest_framework.decorators import action
from ..models import Campaign
from ..serializers import CampaignSerializer
from utils.custom_response import custom_response
from apps.subscribers.models import SubscriberList
from apps.subscribers.serializers import SubscriberListSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    ordering_fields = ['created_at', 'name']  # Fields allowed for ordering
    ordering = ['-created_at']
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        total_count = self.get_queryset().count()
        limit = self.paginator.page_size
        total_page = self.paginator.page.paginator.num_pages
        meta = {
            "page": self.paginator.page.number,
            "total_page": total_page,
            "total_count": total_count,
            "limit": limit,
        }
        return custom_response(data=serializer.data, message="success retrie data", meta=meta)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(data=serializer.data, message="success retrieve data")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return custom_response(data=serializer.data, message="successfully created", code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_response(data=serializer.data, message="successfully updated")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return custom_response(message="successfully deleted", code=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='add-subscriber-list')
    def add_subscriber_list(self, request, pk=None):
        """Custom action to add a subscriber list to a campaign."""
        campaign = self.get_object()  # Get the Campaign instance by ID
        subscriber_list_id = request.data.get("subscriber_list_id")

        if not subscriber_list_id:
            return custom_response(
                message="Subscriber List ID is required.",
                code=status.HTTP_400_BAD_REQUEST,
                errors={"detail": "Missing subscriber_list_id"}
            )

        try:
            if subscriber_list_id:
                subscriber_list = SubscriberList.objects.get(id=subscriber_list_id)
        except subscriber_list.DoesNotExist:
            return custom_response(
                message="Subscriber List not found.",
                code=status.HTTP_404_NOT_FOUND,
                errors={"detail": "No subscriber list found with the given ID."}
            )

        # Add the subscriber to the list if not already added
        if subscriber_list not in campaign.subscriber_lists.all():
            campaign.subscriber_lists.add(subscriber_list)
            return custom_response(
                data={"subscriber_list_id": subscriber_list.id},
                message="Subscriber list successfully added to the campaign.",
                code=status.HTTP_200_OK
            )
        else:
            return custom_response(
                message="Subscriber list is already in the campaign.",
                code=status.HTTP_400_BAD_REQUEST,
                errors={"detail": "This subscriber list is already associated with the campaign."}
            )
    
    @action(detail=True, methods=['post'], url_path='remove-subscriber-list')
    def remove_subscriber_list(self, request, pk=None):
        """Custom action to add a subscriber list to a campaign."""
        campaign = self.get_object()  # Get the Campaign instance by ID
        subscriber_list_id = request.data.get("subscriber_list_id")

        if not subscriber_list_id:
            return custom_response(
                message="Subscriber List ID is required.",
                code=status.HTTP_400_BAD_REQUEST,
                errors={"detail": "Missing subscriber_list_id"}
            )

        try:
            if subscriber_list_id:
                subscriber_list = SubscriberList.objects.get(id=subscriber_list_id)
        except subscriber_list.DoesNotExist:
            return custom_response(
                message="Subscriber List not found.",
                code=status.HTTP_404_NOT_FOUND,
                errors={"detail": "No subscriber list found with the given ID."}
            )

        # Add the subscriber to the list if not already added
        if subscriber_list in campaign.subscriber_lists.all():
            campaign.subscriber_lists.remove(subscriber_list)
            return custom_response(
                data={"subscriber_list_id": subscriber_list.id},
                message="Subscriber list successfully removed from the campaign.",
                code=status.HTTP_200_OK
            )
        else:
            return custom_response(
                message="Subscriber list is already removed from campaign.",
                code=status.HTTP_400_BAD_REQUEST,
                errors={"detail": "This subscriber list is already removed from the campaign."}
            )
            
    @action(detail=True, methods=['get'], url_path='subscriber-lists')
    def subscriber_lists(self, request, pk=None):
        """Retrieve and paginate subscribers in a subscriber list."""
        campaign = self.get_object()  # Get the specific Campaign instance
        subscriber_lists = campaign.subscriber_lists.all()  # Get all subscriber lists in the campaign

        # Paginate the subscriber lists queryset
        page = self.paginate_queryset(subscriber_lists)
        if page is not None:
            serializer = SubscriberListSerializer(page, many=True)
            total_count = self.get_queryset().count()
            limit = self.paginator.page_size
            total_page = self.paginator.page.paginator.num_pages
            meta = {
                "page": self.paginator.page.number,
                "total_page": total_page,
                "total_count": total_count,
                "limit": limit,
            }
            return custom_response(data=serializer.data, message="success retrieve data", meta=meta)

        # If pagination is disabled or not applied
        serializer = SubscriberListSerializer(subscriber_lists, many=True)
        return custom_response(data=serializer.data, message="success retrieve data")