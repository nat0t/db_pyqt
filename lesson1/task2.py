"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только последний
октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.
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
    ping_result = [{'host': str(host),
                    'reachability': subprocess.call(('ping', option, str(packets), str(host)),
                                                    stdout=subprocess.DEVNULL)} for host in network.hosts()]
    for result in ping_result:
        result['reachability'] = 'Host unreachable' if result['reachability'] else 'Host reachable'

    print(tabulate(ping_result, headers='keys', tablefmt='pipe'))


if __name__ == '__main__':
    HOST_RANGE = '87.250.250.0/29'

    try:
        host_range_ping(HOST_RANGE, 2)
    except Exception as e:
        print(e)
