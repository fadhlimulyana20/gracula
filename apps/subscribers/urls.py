from rest_framework.routers import DefaultRouter
from .views import SubscriberViewSet, SubscriberListViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'subscribers', SubscriberViewSet)
router.register(r'subscriber-lists', SubscriberListViewSet)

urlpatterns = [
    # other URL patterns
    path('', include(router.urls)),
]