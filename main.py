from netmiko import ConnectHandler

mikrotik = {
    'device_type': 'mikrotik_routeros',
    'host':   '192.168.56.150',
    'username': 'admin',
    'password': 'admin',
    'port': 22,
}

class MikrotikRouter:
    def __init__(self, host='192.168.56.150', username='admin', password='admin', port=22):
        self.device_type = 'mikrotik_routeros'
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.config_set = {
            'device_type': self.device_type,
            'host': self.host,
            'username': self.username,
            'password': self.password,
            'port': self.port,
        }
    
    def send_command(self, command):
        with ConnectHandler(**self.config_set) as mikrotik_connection:
            return mikrotik_connection.send_command(command, cmd_verify=False)


dev = MikrotikRouter()
dev.send_command('ip address print')