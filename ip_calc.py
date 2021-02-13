"""
GitHub repository: https://github.com/Andrusyshyn-Orest/ip_calculator.git

This module performs various calculations with ip addresses.
"""


def get_ip_from_raw_address(raw_address: str) -> str:
    """
    Return ip address from raw ip address.

    >>> get_ip_from_raw_address("192.168.1.15/24")
    '192.168.1.15'
    >>> get_ip_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    """

    slash_ind = raw_address.index('/')
    return raw_address[:slash_ind]


def get_binary_mask_from_raw_address(raw_address: str) -> str:
    """
    Return binary mask from raw address.

    >>> get_binary_mask_from_raw_address("192.168.1.15/24")
    '11111111.11111111.11111111.00000000'
    >>> get_binary_mask_from_raw_address("91.124.230.205/30")
    '11111111.11111111.11111111.11111100'
    """

    slash_ind = raw_address.index('/')
    prefix = int(raw_address[slash_ind + 1:])
    mask = ['0']*32
    mask[:prefix] = ['1']*prefix
    for ind in range(1, 4):
        mask.insert(8*ind + (ind -1), ".")
    return "".join(mask)


def turn_from_binary_to_decimal(bin_adress: str) -> str:
    """
    Return decimal address from binary address.

    >>> turn_from_binary_to_decimal('11111111.11111111.11111111.00000000')
    '255.255.255.0'
    """

    bin_numbers = bin_adress.split('.')
    decimal_adress = ''
    for number in bin_numbers:
        decimal_adress += str(int( ('0b' + number), 2 ) )
        decimal_adress += '.'
    return decimal_adress[:-1]


def turn_from_decimal_to_binary(decimal_adress: str) -> str:
    """
    Return binary address from decimal address.

    >>> turn_from_decimal_to_binary("192.168.1.15")
    '11000000.10101000.00000001.00001111'
    """

    numbers = decimal_adress.split('.')
    bin_adress = ''
    for number in numbers:
        bin_num = bin(int(number))
        bin_num = bin_num[2:]
        bin_num = bin_num.zfill(8)
        bin_adress += bin_num
        bin_adress += '.'
    return bin_adress[:-1]


def get_network_address_from_raw_address(raw_address: str) -> str:
    """
    Return network address from raw_address.

    >>> get_network_address_from_raw_address("192.168.1.15/24")
    '192.168.1.0'
    >>> get_network_address_from_raw_address("91.124.230.205/30")
    '91.124.230.204'
    """

    ip_address = get_ip_from_raw_address(raw_address)
    mask = get_binary_mask_from_raw_address(raw_address)
    mask = turn_from_binary_to_decimal(mask)

    mask_numbers = mask.split('.')
    ip_numbers = ip_address.split('.')
    network = ''
    for ind in range(len(mask_numbers)):
        network += str( int(mask_numbers[ind]) & int(ip_numbers[ind]) )
        network += '.'
    return network[:-1]


def invert_mask(bin_mask: str) -> str:
    """
    Return inverted binary mask from binary mask (bin_mask).

    >>> invert_mask('11111111.11111111.11111111.00000000')
    '00000000.00000000.00000000.11111111'
    """

    inverted_mask = ''
    for char in bin_mask:
        if char == "1":
            inverted_mask += '0'
        elif char == '0':
            inverted_mask += '1'
        else:
            inverted_mask += '.'
    return inverted_mask


def get_broadcast_address_from_raw_address(raw_address: str) -> str:
    """
    Return broadcast address from raw address.

    >>> get_broadcast_address_from_raw_address("192.168.1.15/24")
    '192.168.1.255'
    >>> get_broadcast_address_from_raw_address("91.124.230.205/30")
    '91.124.230.207'
    """

    mask = get_binary_mask_from_raw_address(raw_address)
    inverted_mask = invert_mask(mask)
    inverted_mask = turn_from_binary_to_decimal(inverted_mask)
    ip_address = get_ip_from_raw_address(raw_address)

    inverted_mask_numbers = inverted_mask.split('.')
    ip_numbers = ip_address.split('.')
    broadcast = ''
    for ind in range(len(ip_numbers)):
        broadcast += str( int(inverted_mask_numbers[ind]) | int(ip_numbers[ind]) )
        broadcast += '.'
    return broadcast[:-1]


def get_first_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    Return first usable host ip address from raw_address.

    >>> get_first_usable_ip_address_from_raw_address("192.168.1.15/24")
    '192.168.1.1'
    >>> get_first_usable_ip_address_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    """

    network = get_network_address_from_raw_address(raw_address)
    network_numbers = network.split('.')
    network_numbers[3] = str( int(network_numbers[3]) + 1 )
    return ".".join(network_numbers)


def get_penultimate_usable_ip_address_from_raw_address(raw_address: str) -> str:
    """
    Return penultimate usable host ip address from raw_address.

    >>> get_penultimate_usable_ip_address_from_raw_address("192.168.1.15/24")
    '192.168.1.253'
    >>> get_penultimate_usable_ip_address_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    """

    broadcast = get_broadcast_address_from_raw_address(raw_address)
    broadcast_numbers = broadcast.split('.')
    broadcast_numbers[3] = str( int(broadcast_numbers[3]) - 2 )
    return ".".join(broadcast_numbers)


def get_number_of_usable_hosts_from_raw_address(raw_address: str) -> int:
    """
    Return number of usable host ip addresses.

    >>> get_number_of_usable_hosts_from_raw_address("192.168.1.15/24")
    254
    >>> get_number_of_usable_hosts_from_raw_address("91.124.230.205/30")
    2
    """

    slash_ind = raw_address.index('/')
    prefix = int(raw_address[slash_ind + 1:])
    return pow(2, 32-prefix) - 2


def get_ip_class_from_raw_address(raw_address: str) -> str:
    """
    Return ip address class from raw_address.

    class A: 1.0.0.0—126.0.0.0, mask 255.0.0.0
    class B: 128.0.0.0—191.255.0.0, mask 255.255.0.0
    class C: 192.0.0.0—223.255.255.0, mask 255.255.255.0
    class D: 224.0.0.0—239.255.255.255, mask 255.255.255.255
    class E: 240.0.0.0—247.255.255.255, mask 255.255.255.255

    >>> get_ip_class_from_raw_address("192.168.1.15/24")
    'C'
    >>> get_ip_class_from_raw_address("91.124.230.205/30")
    'A'
    """

    ip_address = get_ip_from_raw_address(raw_address)
    ip_address = turn_from_decimal_to_binary(ip_address)
    if turn_from_decimal_to_binary('1.0.0.0') <= ip_address <= \
                              turn_from_decimal_to_binary('126.0.0.0'):
        return 'A'
    elif turn_from_decimal_to_binary('128.0.0.0') <= ip_address <= \
                              turn_from_decimal_to_binary('191.255.0.0'):
        return 'B'
    elif turn_from_decimal_to_binary('192.0.0.0') <= ip_address <= \
                              turn_from_decimal_to_binary('223.255.255.0'):
        return 'C'
    elif turn_from_decimal_to_binary('224.0.0.0') <= ip_address <= \
                              turn_from_decimal_to_binary('239.255.255.255'):
        return 'D'
    elif turn_from_decimal_to_binary('240.0.0.0') <= ip_address <= \
                              turn_from_decimal_to_binary('247.255.255.255'):
        return 'E'


def check_private_ip_address_from_raw_address(raw_address: str) -> bool:
    """
    Return True if raw_address is private type, return False otherwise.

    >>> check_private_ip_address_from_raw_address("192.168.1.15/24")
    True
    >>> check_private_ip_address_from_raw_address("91.124.230.205/30")
    False
    """

    ip_address = get_ip_from_raw_address(raw_address)
    ip_address = turn_from_decimal_to_binary(ip_address)
    if turn_from_decimal_to_binary('10.0.0.0') <= ip_address <= \
                turn_from_decimal_to_binary('10.255.255.255'):
        return True
    if turn_from_decimal_to_binary('172.16.0.0') <= ip_address <= \
                turn_from_decimal_to_binary('172.31.255.255'):
        return True
    if turn_from_decimal_to_binary('192.168.0.0') <= ip_address <= \
                turn_from_decimal_to_binary('192.168.255.255'):
        return True

    return False


def input_raw_address() -> str:
    """
    Return raw address from user input:
    ###.###.###.###/##
    """

    return input("Input raw address in th ###.###.###.###/## format: ")


def main():
    """
    Run a program
    """

    raw_address = input_raw_address()
    if raw_address.count('.') != 3:
        print('Error')
        return

    if raw_address.find('/') == -1:
        numbers = raw_address.split('.')
        if not all(map(str.isdecimal, numbers)):
            print("Error")
            return
        print("Missing prefix")
        return
    else:
        slash_ind = raw_address.index('/')
        prefix = raw_address[slash_ind + 1:]
        ip_address = raw_address[:slash_ind]
        if (not (prefix.isdecimal()) or (not 0 <= int(prefix) <= 32)):
            print('Error')
            return
        numbers = ip_address.split('.')
        if (not all(map(str.isdecimal, numbers))) or\
           (not all([0 <= int(number) <= 255 for number in numbers])):
            print('Error')
            return

    ip_address = get_ip_from_raw_address(raw_address)
    print(f'IP address: {ip_address}')
    network = get_network_address_from_raw_address(raw_address)
    print(f'Network Address: {network}')
    broadcast = get_broadcast_address_from_raw_address(raw_address)
    print(f'Broadcast Address: {broadcast}')
    binary_mask = get_binary_mask_from_raw_address(raw_address)
    print(f'Binary Subnet Mask: {binary_mask}')
    first_host = get_first_usable_ip_address_from_raw_address(raw_address)
    print(f'First usable host IP: {first_host}')
    penultimate_host = get_penultimate_usable_ip_address_from_raw_address(raw_address)
    print(f'Penultimate usable host IP: {penultimate_host}')
    number_usable_hosts = get_number_of_usable_hosts_from_raw_address(raw_address)
    print(f'Number of usable Hosts: {number_usable_hosts}')
    ip_class = get_ip_class_from_raw_address(raw_address)
    print(f'IP class: {ip_class}')
    ip_type = check_private_ip_address_from_raw_address(raw_address)
    print(f'IP type private: {ip_type}')


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
    main()
