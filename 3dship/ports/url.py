from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


# -- from app imports ---
from.api import PortsViewSet, ContainerPositionViewSet

router = DefaultRouter()

router.register(r'ports', PortsViewSet, base_name='ports')
router.register(r'containers', ContainerPositionViewSet, base_name='containers')

urlpatterns = router.urls
