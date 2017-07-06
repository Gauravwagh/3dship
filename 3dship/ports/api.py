# Third party imports
from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError

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
    This view-set contains all APIs related to a Ports.

    """

    queryset = Ports.objects.all()
    serializer_class = PortsSerializers

    def create(self, request, *args, **kwargs):
        '''
        Overriting the ModelViewSet's create method
        Creating ports and Containers object.

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

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
            #  Call method in utils file ------
            pos_cal(self, port_number, num_of_containers, serializer, all_portss, pos_const)

        main_port_obj = Ports.objects.get(port_number=port_number)
        main_port_container_obj = ContainerPosition.objects.filter(port=main_port_obj)
        ser = ContainerPositionSerializers(main_port_container_obj, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(ser.data, status=status.HTTP_201_CREATED, headers=headers)


class ContainerPositionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This view-set contains all APIs related to a containerpositions.
    This viewset is read only viewset. It does not allow POST request
    """

    queryset = ContainerPosition.objects.all()
    serializer_class = ContainerPositionSerializers
    pagination_class = StandardResultsSetPagination
