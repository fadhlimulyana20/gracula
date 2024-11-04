from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import SubscriberList, Subscriber
from ..serializers import SubscriberListSerializer, SubscriberSerializer
from utils.custom_response import custom_response

class SubscriberListViewSet(viewsets.ModelViewSet):
    queryset = SubscriberList.objects.all()
    serializer_class = SubscriberListSerializer

    def list(self, request, *args, **kwargs):
        """List all subscriber lists with pagination metadata."""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return custom_response(data=serializer.data, message="success retrieve data")

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific subscriber list."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(data=serializer.data, message="success retrieve data")

    def create(self, request, *args, **kwargs):
        """Create a new subscriber list."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return custom_response(data=serializer.data, message="successfully created", code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update an existing subscriber list."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_response(data=serializer.data, message="successfully updated")

    def destroy(self, request, *args, **kwargs):
        """Delete a subscriber list."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return custom_response(message="successfully deleted", code=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='add-subscriber')
    def add_subscriber(self, request, pk=None):
        """Custom action to add a subscriber to a list."""
        subscriber_list = self.get_object()  # Get the SubscriberList instance by ID
        subscriber_id = request.data.get("subscriber_id")
        email = request.data.get("email")

        if not subscriber_id and not email:
            return custom_response(
                message="Subscriber ID or email is required.",
                code=status.HTTP_400_BAD_REQUEST,
                errors={"detail": "Missing subscriber_id or email."}
            )

        try:
            if subscriber_id:
                subscriber = Subscriber.objects.get(id=subscriber_id)
            elif email:
                subscriber = Subscriber.objects.get(email=email)
        except Subscriber.DoesNotExist:
            return custom_response(
                message="Subscriber not found.",
                code=status.HTTP_404_NOT_FOUND,
                errors={"detail": "No subscriber found with the given ID or email."}
            )

        # Add the subscriber to the list if not already added
        if subscriber not in subscriber_list.subscribers.all():
            subscriber_list.subscribers.add(subscriber)
            return custom_response(
                data={"subscriber_id": subscriber.id},
                message="Subscriber successfully added to the list.",
                code=status.HTTP_200_OK
            )
        else:
            return custom_response(
                message="Subscriber is already in the list.",
                code=status.HTTP_400_BAD_REQUEST,
                errors={"detail": "This subscriber is already associated with the list."}
            )

    @action(detail=True, methods=['post'], url_path='remove-subscriber')
    def remove_subscriber(self, request, pk=None):
        """Custom action to add a subscriber to a list."""
        subscriber_list = self.get_object()  # Get the SubscriberList instance by ID
        subscriber_id = request.data.get("subscriber_id")
        email = request.data.get("email")

        if not subscriber_id and not email:
            return custom_response(
                message="Subscriber ID or email is required.",
                code=status.HTTP_400_BAD_REQUEST,
                errors={"detail": "Missing subscriber_id or email."}
            )

        try:
            if subscriber_id:
                subscriber = Subscriber.objects.get(id=subscriber_id)
            elif email:
                subscriber = Subscriber.objects.get(email=email)
        except Subscriber.DoesNotExist:
            return custom_response(
                message="Subscriber not found.",
                code=status.HTTP_404_NOT_FOUND,
                errors={"detail": "No subscriber found with the given ID or email."}
            )

        # Add the subscriber to the list if not already added
        if subscriber in subscriber_list.subscribers.all():
            subscriber_list.subscribers.remove(subscriber)
            return custom_response(
                data={"subscriber_id": subscriber.id},
                message="Subscriber successfully removed from the list.",
                code=status.HTTP_200_OK
            )
        else:
            return custom_response(
                message="Subscriber is already removed from the list.",
                code=status.HTTP_400_BAD_REQUEST,
                errors={"detail": "This subscriber is already removed from the list."}
            )

    @action(detail=True, methods=['get'], url_path='subscribers')
    def subscribers(self, request, pk=None):
        """Retrieve and paginate subscribers in a subscriber list."""
        subscriber_list = self.get_object()  # Get the specific SubscriberList instance
        subscribers = subscriber_list.subscribers.all()  # Get all subscribers in the list

        # Paginate the subscribers queryset
        page = self.paginate_queryset(subscribers)
        if page is not None:
            serializer = SubscriberSerializer(page, many=True)
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
        serializer = SubscriberSerializer(subscribers, many=True)
        return custom_response(data=serializer.data, message="success retrieve data")