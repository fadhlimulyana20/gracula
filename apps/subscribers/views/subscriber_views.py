# views.py
from rest_framework import viewsets, status
from ..models import Subscriber
from ..serializers import SubscriberSerializer
from utils.custom_response import custom_response

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

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
        return custom_response(data=serializer.data, message="success retrieve data", meta=meta)

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
