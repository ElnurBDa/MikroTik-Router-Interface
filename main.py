from netmiko import ConnectHandler
from time import sleep
import sys

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
    
    # Basic
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
    
    # Terminal Handle
    def clean_terminal(self):
        self.wait_line()
        sys.stdout.write("\033[H\033[J")
    
    def wait_line(self):
        input("\n+-----------------+\n| Press Enter key |\n+-----------------+\n")

    def limit_line(self):
        print('█'*50)

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
        interface = input('Enter interface(default ether2): ') or "ether2"
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
        while True:
            self.clean_terminal()
            print('1. Show IP address')
            print('2. Add IP address')
            print('3. Remove IP address')
            print('4. Change IP address')
            print('5. Back')
            choice = input('Enter choice: ')
            self.limit_line()
            if choice == '1':
                self.show_ip_address()
            elif choice == '2':
                self.add_ip()
            elif choice == '3':
                self.remove_ip()
            elif choice == '4':
                self.change_ip()
            elif choice == '5':
                break
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
        while True:
            self.clean_terminal()
            print('1. Show port')
            print('2. Change port')
            print('3. Back')
            choice = input('Enter choice: ')
            self.limit_line()
            if choice == '1':
                self.show_port()
            elif choice == '2':
                self.change_port()
            elif choice == '3':
                break
            else:
                print('Invalid choice')

    # Firewall
    def show_firewall_rule(self):
        print('Showing firewall rule!')
        command = '/ip firewall filter print'
        res = self.send_command(command)
        print(res)
        return res

    def add_firewall_rule(self):
        print('Adding firewall rule!')
        rule = input('Enter rule (default: chain=forward): ') or 'chain=forward'
        command = f'/ip firewall filter add {rule}'
        self.send_command(command)
    
    def remove_firewall_rule(self):
        print('Removing firewall rule!')
        number = input('Enter number: ')
        command = f'/ip firewall filter remove numbers={number}'
        self.send_command(command)
    
    def disable_firewall_rule(self):
        print('Disabling firewall rule!')
        number = input('Enter number: ')
        command = f'/ip firewall filter disable numbers={number}'
        self.send_command(command)

    def enable_firewall_rule(self):
        print('Enabling firewall rule!')
        number = input('Enter number: ')
        command = f'/ip firewall filter enable numbers={number}'
        self.send_command(command)
    
    def handle_firewall_rule(self):
        while True:
            self.clean_terminal()
            print('1. Show firewall rule')
            print('2. Add firewall rule')
            print('3. Remove firewall rule')
            print('4. Disable firewall rule')
            print('5. Enable firewall rule')
            print('6. Back')
            choice = input('Enter choice: ')
            self.limit_line()
            if choice == '1':
                self.show_firewall_rule()
            elif choice == '2':
                self.add_firewall_rule()
            elif choice == '3':
                self.remove_firewall_rule()
            elif choice == '4':
                self.disable_firewall_rule()
            elif choice == '5':
                self.enable_firewall_rule()
            elif choice == '6':
                break
            else:
                print('Invalid choice')
    
    # Showing some other info about router
    def show_system_resource(self):
        print('Showing info!')
        command = '/system resource print'
        res = self.send_command(command)
        print(res)
        return res
    
    def show_interface(self):
        print('Showing interface!')
        command = '/interface print'
        res = self.send_command(command)
        print(res)
        return res

    def show_route(self):
        print('Showing route!')
        command = '/ip route print'
        res = self.send_command(command)
        print(res)
        return res
    
    def show_arp(self):
        print('Showing arp!')
        command = '/ip arp print'
        res = self.send_command(command)
        print(res)
        return res
    
    def show_dns(self):
        print('Showing dns!')
        command = '/ip dns print'
        res = self.send_command(command)
        print(res)
        return res
    
    def show_dhcp(self):
        print('Showing dhcp!')
        command = '/ip dhcp-server print'
        res = self.send_command(command)
        print(res)
        return res
    
    def show_user(self):
        print('Showing user!')
        command = '/user print'
        res = self.send_command(command)
        print(res)
        return res
    
    def show_log(self):
        print('Showing log!')
        command = '/log print'
        res = self.send_command(command)
        print(res)
        return res
    
    def handle_info(self):
        while True:
            self.clean_terminal()
            print('1. Show system resource')
            print('2. Show interface')
            print('3. Show route')
            print('4. Show arp')
            print('5. Show dns')
            print('6. Show dhcp')
            print('7. Show user')
            print('8. Show log')
            print('9. Back')
            choice = input('Enter choice: ')
            self.limit_line()
            if choice == '1':
                self.show_system_resource()
            elif choice == '2':
                self.show_interface()
            elif choice == '3':
                self.show_route()
            elif choice == '4':
                self.show_arp()
            elif choice == '5':
                self.show_dns()
            elif choice == '6':
                self.show_dhcp()
            elif choice == '7':
                self.show_user()
            elif choice == '8':
                self.show_log()
            elif choice == '9':
                break
            else:
                print('Invalid choice')
    
    # Main menu
    def main_menu(self):
        while True:
            self.clean_terminal()
            print('1. Handle IP address')
            print('2. Handle port')
            print('3. Handle firewall rule')
            print('4. Handle info')
            print('5. Exit')
            choice = input('Enter choice: ')
            self.limit_line()
            if choice == '1':
                dev.handle_ip_change()
            elif choice == '2':
                dev.handle_port_change()
            elif choice == '3':
                dev.handle_firewall_rule()
            elif choice == '4':
                dev.handle_info()
            elif choice == '5':
                break
            else:
                print('Invalid choice')


host = input('Enter host: ') or '192.168.56.179'
port = input('Enter port(default 22): ') or 22
username = input('Enter username(default admin): ') or 'admin'
password = input('Enter password(default admin): ') or 'admin'
dev = MikrotikRouter(host=host, port=port, username=username, password=password)
dev.main_menu()