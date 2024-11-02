from rest_framework.routers import DefaultRouter
from .views import SubscriberViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'subscribers', SubscriberViewSet)

urlpatterns = [
    # other URL patterns
    path('', include(router.urls)),
]