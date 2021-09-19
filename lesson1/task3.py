"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2. Но в данном случае
результат должен быть итоговым по всем ip-адресам, представленным в табличном формате (использовать модуль tabulate).
Таблица должна состоять из двух колонок и выглядеть примерно так:
Reachable

10.0.0.1
10.0.0.2
Unreachable

10.0.0.3
10.0.0.4
"""
import ipaddress
import platform
import subprocess
from tabulate import tabulate


def host_range_ping(host_range: str, packets: int) -> None:
    """
    Ping hosts from the specified host range sequentally and print total table with result.
    """
    option = '-n' if platform.system().lower() == 'windows' else '-c'

    try:
        network = ipaddress.ip_network(host_range)
    except Exception as error:
        print(error)
        return

    ping_result = {'Reachable': [host for host in network.hosts() if not
                                subprocess.call(('ping', option, str(packets), str(host)), stdout=subprocess.DEVNULL)]}
    ping_result.update({'Unreachable': [host for host in network.hosts() if host not in ping_result['Reachable']]})

    print(tabulate(ping_result, headers='keys', tablefmt='simple'))


if __name__ == '__main__':
    HOST_RANGE = '87.250.250.0/29'

    try:
        host_range_ping(HOST_RANGE, 2)
    except Exception as e:
        print(e)
