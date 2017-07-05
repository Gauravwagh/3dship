from functools import reduce

from django.db.models import Q
from django.conf import settings
import datetime
from django.contrib.contenttypes.models import ContentType

# Third party imports
from rest_framework import viewsets
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication

# from app imports ------
from .serializers import ContainerPositionSerializers, PortsSerializers
from .models import Ports, ContainerPosition, PositionConstants
from .utils import pos_cal

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PortsViewSet(viewsets.ModelViewSet):
    """
    This view-set contains all APIs related to a booking.
    """

    queryset = Ports.objects.all()
    serializer_class = PortsSerializers

    def create(self, request, *args, **kwargs):

        data = Ports.objects.filter(port_number=int(request.data['port_number']))
        if data:
            raise APIException("Port is already created with same port number.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        port_number = serializer.data['port_number']
        num_of_containers = serializer.data['number_of_containers']
        pos_const = PositionConstants.objects.all()[0]
        all_portss = Ports.objects.all()
        all_cont = ContainerPosition.objects.all()
        all_cont_new = len(all_cont) + num_of_containers
        if all_cont_new > 250:
            raise ParseError("Container count should not be greater than 250.")
        else:
            pos_cal(self, port_number, num_of_containers, serializer, all_portss, pos_const)

        main_port_obj = Ports.objects.get(port_number=port_number)
        main_port_container_obj = ContainerPosition.objects.filter(port=main_port_obj)
        ser = ContainerPositionSerializers(main_port_container_obj, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(ser.data, status=status.HTTP_201_CREATED, headers=headers)


class ContainerPositionViewSet(viewsets.ModelViewSet):
    """
    This view-set contains all APIs related to a booking.
    """

    queryset = ContainerPosition.objects.all()
    serializer_class = ContainerPositionSerializers

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    # filter_class = BlogPageFilter
    # pagination_class = StandardResultsSetPagination

    # search_fields = (
    #     'id', 'tags__name', 'title', 'live', 'date', 'is_featured', 'body',
    # )
