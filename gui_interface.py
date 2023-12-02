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

theme1 = 'DarkAmber'
theme2 = 'DarkRed'
sg.theme(theme1)
size1=(20,1)
size2=(7,1)
size3=(50,10)
size4=(30,1)
title='MikrotikRouter Configuration Interface'
retry_times = 3
sleep_time = 1
is_safe = False

def click_safe_mode():
    global is_safe
    if not is_safe: 
        sg.popup('Entering safe mode...')
        sg.theme(theme2)
    else: 
        sg.popup('Exiting safe mode...')
        sg.theme(theme1)
    is_safe = not is_safe
    router.send_str(ascii.ctrl('x'))

def click_undo_changes_in_safe_mode():
    global is_safe
    sg.popup('Undoing changes...')
    router.send_str(ascii.ctrl('d'))
    is_safe = False
    router.disconnect()
    retry(router.connect)
    sg.theme(theme1)

def retry(method):
    for i in range(retry_times):
        try:
            method()
            break
        except Exception as e:
            sg.popup('Connection failed:  '+str(e)+'\nRetrying...')
            sleep(sleep_time)
            continue
    if retry_times == i+1:
        sg.popup('Connection failed\nPlease check your network and try again')
        return False
    return True

def show_anything(window, command):
    try:
        result = router.send_command(command)
        window['-Result-'].update(result)
    except Exception as e:
        sg.popup('Failed:  '+str(e))

def number_page(what_page,show_command, execute_command):
    result = router.send_command(show_command)
    new_window = sg.Window(title, [[sg.Text(what_page)],
        [sg.Text('Enter number',s=size4), sg.InputText(s=size1)],
        [sg.Button('Execute',s=size1)],
        [sg.Button('Back',s=size1)],
        [sg.Text('Result:',s=size2)], 
        [sg.Multiline(default_text=result, s=size3, key='-Result-')]] )
    while True:
        event, values = new_window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break
        if event == 'Execute':
            try:
                number = values[0]
                result = router.send_command(execute_command+number) or 'Success'
                new_window['-Result-'].update(result)
            except Exception as e:
                sg.popup('Failed:  '+str(e))
            continue
    new_window.close()

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
            show_anything(window, '/ip address print')
            continue
        if event == 'Add IP address':
            window.hide()
            hidden = True
            result = router.send_command('/ip address print')
            new_window = sg.Window(title, [[sg.Text('Add IP address Page')],
                [sg.Text('Enter IP address (N.N.N.N/M)',s=size4), sg.InputText(s=size1)],
                [sg.Text('Enter interface(default ether2)',s=size4), sg.InputText(s=size1)],
                [sg.Button('Execute',s=size1)],
                [sg.Button('Back',s=size1)],
                [sg.Text('Result:',s=size2)], 
                [sg.Multiline(default_text=result, s=size3, key='-Result-')]] )
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
        if event == 'Remove IP address':
            window.hide()
            hidden = True
            number_page('Remove IP address Page', '/ip address print', '/ip address remove numbers=')
            continue
        if event == 'Change IP address':
            result = router.send_command('/ip address print')
            window.hide()
            hidden = True
            new_window = sg.Window(title, [[sg.Text('Change IP address Page')],
                [sg.Text('Current IP address: '+router.host, key='-CURRENT-IP-')],
                [sg.Text('Enter IP address (N.N.N.N)',s=size4), sg.InputText(s=size1)],
                [sg.Button('Execute',s=size1)],
                [sg.Button('Back',s=size1)],
                [sg.Text('Result:',s=size2)], 
                [sg.Multiline(default_text=result, s=size3, key='-Result-')]] )
            while True:
                event, values = new_window.read()
                if event in (sg.WIN_CLOSED, 'Back'):
                    break
                if event == 'Execute':
                    try:
                        ip_address = values[0]
                        router.host = ip_address
                        if not retry(router.connect): continue
                        new_window['-Result-'].update('Success')
                        new_window['-CURRENT-IP-'].update('Current IP address: '+router.host)

                    except Exception as e:
                        sg.popup('Failed:  '+str(e))
                    continue
            new_window.close()
            continue
    window.close()

def open_port_page():
    window = sg.Window(title, [  [sg.Text('Port Page')],
        [sg.Button('Show port',s=size1)],
        [sg.Button('Change port',s=size1)],
        [sg.Button('Back',s=size1)],
        [sg.Text('Result:',s=size2)], 
        [sg.Multiline(s=size3, key='-Result-')] ])
    hidden = False
    while True:
        if hidden: window.un_hide()
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break
        if event == 'Show port':
            show_anything(window, '/ip service print')
            continue
        if event == 'Change port':
            result = router.send_command('/ip service print')
            window.hide()
            hidden = True
            new_window = sg.Window(title, [[sg.Text('Change port Page')],
                [sg.Text('Current port: '+str(router.port), key='-CURRENT-PORT-')],
                [sg.Text('Enter port you want to redact(default: ssh)',s=size4), sg.InputText(s=size1)],
                [sg.Text('Enter new port number',s=size4), sg.InputText(s=size1)],
                [sg.Button('Execute',s=size1)],
                [sg.Button('Back',s=size1)],
                [sg.Text('Result:',s=size2)], 
                [sg.Multiline(default_text=result, s=size3, key='-Result-')]] )
            while True:
                event, values = new_window.read()
                if event in (sg.WIN_CLOSED, 'Back'):
                    break
                if event == 'Execute':
                    try:
                        port = values[0] or 'ssh'
                        port_number = values[1]
                        router.send_command(f'/ip service set {port} port={port_number}')
                        if port == 'ssh':
                            router.port = port_number
                            if not retry(router.connect): continue
                        
                        new_window['-Result-'].update('Success')
                        new_window['-CURRENT-PORT-'].update('Current IP address: '+router.port)
                    except Exception as e:
                        sg.popup('Failed:  '+str(e))
                    continue
            new_window.close()
            continue
    window.close()

def open_firewall_page():
    window = sg.Window(title, [[sg.Text('Firewall Page')],
        [sg.Button('Show firewall rule',s=size1)],
        [sg.Button('Add firewall rule',s=size1)],
        [sg.Button('Remove firewall rule',s=size1)],
        [sg.Button('Disable firewall rule',s=size1)],
        [sg.Button('Enable firewall rule',s=size1)],
        [sg.Button('Back',s=size1)],
        [sg.Text('Result:',s=size2)], 
        [sg.Multiline(s=size3, key='-Result-')] ])
    hidden = False
    while True:
        if hidden: window.un_hide()
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break
        if event == 'Show firewall rule':
            show_anything(window, '/ip firewall filter print')
            continue
        if event == 'Add firewall rule':
            result = router.send_command('/ip firewall filter print')
            window.hide()
            hidden = True
            new_window = sg.Window(title, [[sg.Text('Add firewall rule Page')],
                [sg.Text('Enter rule (default: chain=forward)',s=size4), sg.InputText(s=size1)],
                [sg.Button('Execute',s=size1)],
                [sg.Button('Back',s=size1)],
                [sg.Text('Result:',s=size2)], 
                [sg.Multiline(default_text=result, s=size3, key='-Result-')]] )
            while True:
                event, values = new_window.read()
                if event in (sg.WIN_CLOSED, 'Back'):
                    break
                if event == 'Execute':
                    try:
                        rule = values[0] or 'chain=forward'
                        result = router.send_command('/ip firewall filter add '+rule) or 'Success'
                        new_window['-Result-'].update(result)
                    except Exception as e:
                        sg.popup('Failed:  '+str(e))
                    continue
            new_window.close()
            continue
        if event == 'Remove firewall rule':
            window.hide()
            hidden = True
            number_page('Remove firewall rule Page', '/ip firewall filter print', '/ip firewall filter remove numbers=')
            continue
        if event == 'Disable firewall rule':
            window.hide()
            hidden = True
            number_page('Disable firewall rule Page', '/ip firewall filter print', '/ip firewall filter disable numbers=')
            continue
        if event == 'Enable firewall rule':
            window.hide()
            hidden = True
            number_page('Enable firewall rule Page', '/ip firewall filter print', '/ip firewall filter enable numbers=')
            continue
    window.close()

def open_info_page():
    window = sg.Window(title, [  [sg.Text('Info Page')],
        [sg.Button('Show system resource',s=size1)],
        [sg.Button('Show interface',s=size1)],
        [sg.Button('Show route',s=size1)],
        [sg.Button('Show arp',s=size1)],
        [sg.Button('Show dns',s=size1)],
        [sg.Button('Show dhcp',s=size1)],
        [sg.Button('Show user',s=size1)],
        [sg.Button('Show log',s=size1)],
        [sg.Button('Back',s=size1)],
        [sg.Text('Result:',s=size2)], 
        [sg.Multiline(s=size3, key='-Result-')] ])
    hidden = False
    while True:
        if hidden: window.un_hide()
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break
        if event == 'Show system resource':
            show_anything(window, '/system resource print')
            continue
        if event == 'Show interface':
            show_anything(window, '/interface print')
            continue
        if event == 'Show route':
            show_anything(window, '/ip route print')
            continue
        if event == 'Show arp':
            show_anything(window, '/ip arp print')
            continue
        if event == 'Show dns':
            show_anything(window, '/ip dns print')
            continue
        if event == 'Show dhcp':
            show_anything(window, '/ip dhcp-server print')
            continue
        if event == 'Show user':
            show_anything(window, '/user print')
            continue
        if event == 'Show log':
            show_anything(window, '/log print')
            continue
    window.close()

def open_safe_page():
    window = sg.Window(title, [  [sg.Text('Safe Page')],
        [sg.Button('Click safe mode',s=size1)],
        [sg.Button('Undo changes in safe mode',s=size1)],
        [sg.Button('Back',s=size1)] ])
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Back'):
            break
        if event == 'Click safe mode':
            click_safe_mode()
            window.close()
            window = sg.Window(title, [  [sg.Text('Safe Page')],
        [sg.Button('Click safe mode',s=size1)],
        [sg.Button('Undo changes in safe mode',s=size1)],
        [sg.Button('Back',s=size1)] ])
            continue
        if event == 'Undo changes in safe mode':
            click_undo_changes_in_safe_mode()
            window.close()
            window = sg.Window(title, [  [sg.Text('Safe Page')],
        [sg.Button('Click safe mode',s=size1)],
        [sg.Button('Undo changes in safe mode',s=size1)],
        [sg.Button('Back',s=size1)] ])
            continue
    window.close()

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

def init_main_page():
    return sg.Window(title, [  [sg.Text('Main Page')],
        [sg.Button('Handle IP address',s=size1)],
        [sg.Button('Handle port',s=size1)],
        [sg.Button('Handle firewall rule',s=size1)],
        [sg.Button('Handle info',s=size1)],
        [sg.Button('Handle safe mode',s=size1)],
        [sg.Button('Handle any command',s=size1)],
        [sg.Button('Exit',s=size1)] ])


def open_main_page():
    window = init_main_page()
    hidden = False
    while True:
        if hidden: 
            window = init_main_page()
            # window.un_hide()
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Handle IP address':
            # window.hide()
            window.close()
            hidden = True
            open_ip_page()
            continue
        if event == 'Handle port':
            # window.hide()
            window.close()
            hidden = True
            open_port_page()
            continue
        if event == 'Handle firewall rule':
            # window.hide()
            window.close()
            hidden = True
            open_firewall_page()
            continue
        if event == 'Handle info':
            # window.hide()
            window.close()
            hidden = True
            open_info_page()
            continue
        if event == 'Handle safe mode':
            # window.hide()
            window.close()
            hidden = True
            open_safe_page()
            continue
        if event == 'Handle any command':
            # window.hide()
            window.close()
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

        sg.popup('Successfully connnected!')
        window.close()
        open_main_page()
        continue
window.close()
