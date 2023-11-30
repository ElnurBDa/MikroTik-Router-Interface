from netmiko import ConnectHandler
from time import sleep

class MikrotikRouter:
    def __init__(self, host, username='admin', password='admin',port=22):
        self.device_type = 'mikrotik_routeros'
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.config_set = None
        self.connenction = None
        self.retry(self.connect)
    
    def connect(self):
        self.config_set = {
            'device_type': self.device_type,
            'host': self.host,
            'username': self.username,
            'password': self.password,
            'port': self.port
        }
        self.connenction = ConnectHandler(**self.config_set)

    def retry(self, method, times=3):
        for i in range(times):
            try:
                method()
                break
            except Exception as e:
                print(e)
                sleep(30)
                print('Retrying...')

    def send_command(self, command):
        return self.connenction.send_command(command, cmd_verify=False)
    
    # IP address
    def show_ip_address(self):
        print('Showing IP address!')
        command = '/ip address print'
        res = self.send_command(command)
        print(res)
        return res

    def add_ip(self):
        print('Adding IP address!')
        ip_address = input('Enter IP address (N.N.N.N/M): ')
        interface = input('Enter interface: ')
        command = f'/ip address add address={ip_address} interface={interface}'
        print(self.send_command(command))
    
    def remove_ip(self):
        print('Removing IP address!')
        number = input('Enter number: ')
        command = f'/ip address remove numbers={number}'
        print(self.send_command(command))
    
    def change_ip(self):
        print('Changing IP address!')
        ip_address = input('Enter IP address (N.N.N.N): ')
        self.host = ip_address
        self.retry(self.connect)

    def handle_ip_change(self):
        print('1. Show IP address')
        print('2. Add IP address')
        print('3. Remove IP address')
        print('4. Change IP address')
        choice = input('Enter choice: ')
        if choice == '1':
            self.show_ip_address()
        elif choice == '2':
            self.add_ip()
        elif choice == '3':
            self.remove_ip()
        elif choice == '4':
            self.change_ip()
        else:
            print('Invalid choice')

    # Port
    def show_port(self):
        print('Showing port!')
        command = 'ip service print'
        res = self.send_command(command)
        print(res)
        return res
    
    def change_port(self):
        print('Changing port!')
        port = input('Enter port you want to redact(ssh): ')
        port_number = input('Enter new port number: ')
        command = f'/ip service set {port} port={port_number}'
        print(self.send_command(command))
        if port == 'ssh':
            self.port = port_number
            self.retry(self.connect)

    def handle_port_change(self):
        print('1. Show port')
        print('2. Change port')
        choice = input('Enter choice: ')
        if choice == '1':
            self.show_port()
        elif choice == '2':
            self.change_port()
        else:
            print('Invalid choice')

    


dev = MikrotikRouter(host='192.168.56.120')

dev.handle_port_change()
dev.handle_port_change()
dev.handle_port_change()
dev.handle_port_change()
