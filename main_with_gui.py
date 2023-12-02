import PySimpleGUI as sg
from netmiko import ConnectHandler
from time import sleep
from curses import ascii 

class MikrotikRouter:
    def __init__(self, host, username='admin', password='admin',port=22):
        self.device_type = 'mikrotik_routeros'
        self.host = host 
        self.username = username
        self.password = password
        self.port = port
        self.config_set = None
        self.connenction = None
        self.insafe = False
        
    def connect(self):
        self.config_set = {
            'device_type': self.device_type,
            'host': self.host,
            'username': self.username,
            'password': self.password,
            'port': self.port
        }
        self.connenction = ConnectHandler(**self.config_set)
        
    def disconnect(self):
        self.connenction.disconnect()

    def send_command(self, command):
        return self.connenction.send_command(command, cmd_verify=False)
    
    def send_str(self,string):
        self.connenction.write_channel(string)

sg.theme('DarkAmber')
size1=(20,1)
size2=(7,1)
size3=(50,10)
size4=(50,1)
title='MikrotikRouter Configuration Interface'
retry_times = 3
sleep_time = 1

pages ={
    "port_page" : [  [sg.Text('Port Page')],
        [sg.Button('Show port',s=size1)],
        [sg.Button('Change port',s=size1)],
        [sg.Button('Back',s=size1)] ],
    "firewall_page" : [  [sg.Text('Firewall Page')],
        [sg.Button('Show firewall rule',s=size1)],
        [sg.Button('Add firewall rule',s=size1)],
        [sg.Button('Remove firewall rule',s=size1)],
        [sg.Button('Disable firewall rule',s=size1)],
        [sg.Button('Enable firewall rule',s=size1)],
        [sg.Button('Back',s=size1)] ],
    "info_page" : [  [sg.Text('Info Page')],
        [sg.Button('Show system resource',s=size1)],
        [sg.Button('Show interface',s=size1)],
        [sg.Button('Show route',s=size1)],
        [sg.Button('Show arp',s=size1)],
        [sg.Button('Show dns',s=size1)],
        [sg.Button('Show dhcp',s=size1)],
        [sg.Button('Show user',s=size1)],
        [sg.Button('Show log',s=size1)],
        [sg.Button('Back',s=size1)] ],
    "safe_page" : [  [sg.Text('Safe Page')],
        [sg.Button('Click safe mode',s=size1)],
        [sg.Button('Undo changes in safe mode',s=size1)],
        [sg.Button('Back',s=size1)] ],
}


def open_ip_page():
    window = sg.Window(title, [  [sg.Text('IP Page')],
        [sg.Button('Show IP address',s=size1)],
        [sg.Button('Add IP address',s=size1)],
        [sg.Button('Remove IP address',s=size1)],
        [sg.Button('Change IP address',s=size1)],
        [sg.Button('Back',s=size1)],
        [sg.Text('Result:',s=size2)], 
        [sg.Multiline(s=size3, key='-Result-')] ])
    hidden = False
    while True:
        if hidden: window.un_hide()
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break
        if event == 'Show IP address':
            try:
                result = router.send_command('/ip address print')
                window['-Result-'].update(result)
            except Exception as e:
                sg.popup('Failed:  '+str(e))
            continue
        if event == 'Add IP address':
            window.hide()
            hidden = True
            new_window = sg.Window(title, [[sg.Text('Add IP address Page')],
                [sg.Text('Enter IP address (N.N.N.N/M)',s=size4), sg.InputText(s=size1)],
                [sg.Text('Enter interface(default ether2)',s=size4), sg.InputText(s=size1)],
                [sg.Button('Execute',s=size1)],
                [sg.Button('Back',s=size1)],
                [sg.Text('Result:',s=size2)], 
                [sg.Multiline(s=size3, key='-Result-')]] )
            while True:
                event, values = new_window.read()
                if event in (sg.WIN_CLOSED, 'Back'):
                    break
                if event == 'Execute':
                    try:
                        ip_address = values[0]
                        interface = values[1] or 'ether2'
                        result = router.send_command('/ip address add address='+ip_address+' interface='+interface) or 'Success'
                        new_window['-Result-'].update(result)
                    except Exception as e:
                        sg.popup('Failed:  '+str(e))
                    continue
            new_window.close()
            continue
            
    window.close()

def open_port_page():
    pass

def open_firewall_page():
    pass

def open_info_page():
    pass

def open_safe_page():
    pass

def open_any_command_page():
    window = sg.Window(title, [[sg.Text('Any command Page')],
        [sg.Text('Command',s=size2), sg.InputText(s=size1)],
        [sg.Button('Execute',s=size1)],
        [sg.Button('Back',s=size1)],
        [sg.Text('Result:',s=size2)], 
        [sg.Multiline(s=size3, key='-Result-')]])
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break
        if event == 'Execute':
            try:
                result = router.send_command(values[0])
                window['-Result-'].update(result)
            except Exception as e:
                sg.popup('Failed:  '+str(e))
    window.close()
    del window

def open_main_page():
    window = sg.Window(title, [  [sg.Text('Main Page')],
        [sg.Button('Handle IP address',s=size1)],
        [sg.Button('Handle port',s=size1)],
        [sg.Button('Handle firewall rule',s=size1)],
        [sg.Button('Handle info',s=size1)],
        [sg.Button('Handle safe mode',s=size1)],
        [sg.Button('Handle any command',s=size1)],
        [sg.Button('Exit',s=size1)] ])
    hidden = False
    while True:
        if hidden: window.un_hide()
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Handle IP address':
            window.hide()
            hidden = True
            open_ip_page()
            continue
        if event == 'Handle port':
            window.hide()
            hidden = True
            open_port_page()
            continue
        if event == 'Handle firewall rule':
            window.hide()
            hidden = True
            open_firewall_page()
            continue
        if event == 'Handle info':
            window.hide()
            hidden = True
            open_info_page()
            continue
        if event == 'Handle safe mode':
            window.hide()
            hidden = True
            open_safe_page()
            continue
        if event == 'Handle any command':
            window.hide()
            hidden = True
            open_any_command_page()
            continue
    window.close()


window = sg.Window(title, [  [sg.Text('Login Page')],
    [sg.Text('host:',s=size2), sg.InputText(s=size1)],
    [sg.Text('port:',s=size2), sg.InputText(s=size1)],
    [sg.Text('username:',s=size2), sg.InputText(s=size1)],
    [sg.Text('password:',s=size2), sg.InputText(s=size1)],
    [sg.Button('Login')] ])
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Login':
        host=values[0] or '192.168.56.199'
        port=values[1] or 22
        username=values[2] or 'admin'
        password=values[3] or 'admin'
        router = MikrotikRouter(host,username,password,port)

        for i in range(retry_times):
            try:
                router.connect()
                break
            except Exception as e:
                sg.popup('Login failed:  '+str(e)+'\nRetrying...')
                sleep(sleep_time)
                continue

        if retry_times == i+1:
            sg.popup('Login failed\nPlease check your network and try again')
            continue

        sg.popup('Login successful')
        window.close()
        open_main_page()
        continue
window.close()
