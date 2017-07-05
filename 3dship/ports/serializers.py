# Third party imports
from rest_framework import serializers


# Import from apps
from .models import Ports, ContainerPosition, PositionConstants


class PortsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ports
        exclude = ['id']



class ContainerPositionSerializers(serializers.ModelSerializer):
    port = serializers.SerializerMethodField('get_port_number')
    class Meta:
        model = ContainerPosition
        exclude = ['id']

    def get_port_number(self, obj):
        return obj.port.port_number
