from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)

urlpatterns = [
    # other URL patterns
    path('', include(router.urls)),
]