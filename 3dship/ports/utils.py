from .serializers import ContainerPositionSerializers
from .models import Ports, ContainerPosition

def pos_cal(self, port_number, num_of_containers, serializer, all_portss, pos_const):
    '''
    :param self:
    :param port_number:
    :param num_of_containers:
    :param serializer:
    :param all_portss:
    :param pos_const:
    :return: "Success string"
    '''
    x = pos_const.x_constant
    y = pos_const.y_constant
    z = pos_const.z_constant
    counter = 1
    for i in range(z, 6):
        if counter > num_of_containers:
            break
        z = i
        for j in range(y, 6):
            if counter > num_of_containers:
                break
            y = j
            if y == 5:
                y = 1
            for k in range(x, 11):
                if counter > num_of_containers:
                    break
                counter += 1
                x = k + 1
                if x == 11:
                    x = 1
                if len(all_portss) == 1:
                    data = {"port": serializer.data['id'], "x_position": k, "y_position": j,
                            "z_position": i}
                    ser1 = ContainerPositionSerializers(data=data)
                    ser1.is_valid(raise_exception=True)
                    self.perform_create(ser1)
                else:
                    all_pots_values = Ports.objects.values_list('port_number', flat=True)
                    ac = []
                    for dat in all_pots_values:
                        ac.append(dat)
                    ac.sort()
                    l1 = []
                    l2 = []

                    for dl in ac:
                        if dl >= port_number:
                            l2.append(dl)
                        else:
                            l1.append(dl)
                    if len(l2) == 1:
                        data = {"port": serializer.data['id'], "x_position": k, "y_position": j,
                                "z_position": i}
                        ser1 = ContainerPositionSerializers(data=data)
                        ser1.is_valid(raise_exception=True)
                        self.perform_create(ser1)
                    else:
                        for index, element in enumerate(l2):
                            main_port = Ports.objects.get(port_number=port_number)
                            if len(ContainerPosition.objects.filter(port=main_port)) < num_of_containers:
                                try:
                                    next_index = l2[index + 1]
                                    port_by_port_no = Ports.objects.get(port_number=next_index)
                                    all_containers_for_port = ContainerPosition.objects.filter(
                                        port=port_by_port_no)[:num_of_containers]
                                    for onecont in all_containers_for_port:
                                        onecont.port = main_port
                                        onecont.save()
                                except:
                                    pass
                        last_port = l2[-1]
                        last_port_obj = Ports.objects.get(port_number=last_port)
                        data = {"port": last_port_obj.id, "x_position": k, "y_position": j,
                                "z_position": i}
                        ser1 = ContainerPositionSerializers(data=data)
                        ser1.is_valid(raise_exception=True)
                        self.perform_create(ser1)

    pos_const.x_constant = x
    pos_const.y_constant = y
    pos_const.z_constant = z
    pos_const.save()
    return "Success"
