"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов. Аргументом
функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом. В функции
необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения («Узел доступен», «Узел
недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
"""
import ipaddress
import os
import platform
import socket
import subprocess
from tabulate import tabulate


def get_adresses(hosts: list) -> list:
    """
    Validate and convert the list of hosts to the list of IP-addresses.
    """
    if type(hosts) is not list:
        raise ValueError(f'The passed object must be a list type. {type(hosts)} is given.')
    try:
        addresses = [ipaddress.ip_address(socket.gethostbyname(host)) for host in hosts]
    except socket.gaierror:
        raise ValueError('One or more of the passed addresses is not a valid hostname or IP-address.')
    return addresses


def host_ping(addresses: list, packets: int) -> None:
    """
    Ping the specified IP-addresses sequentally and print total table with result.
    """
    option = '-n' if platform.system().lower() == 'windows' else '-c'

    ping_result = [{'host': str(address),
                    'reachability': subprocess.call(('ping', option, str(packets), str(address)),
                                                    stdout=subprocess.DEVNULL)} for address in addresses]
    for result in ping_result:
        result['reachability'] = 'Host unreachable' if result['reachability'] else 'Host reachable'
    print(tabulate(ping_result, headers='keys', tablefmt='pipe'))


if __name__ == '__main__':
    HOSTS = ['ya.ru', 'google.com', '192.168.5.1']

    try:
        ip_addresses = get_adresses(HOSTS)
        host_ping(ip_addresses, 2)
    except ValueError as error:
        print(error)
