# Description
This codes aim to work with MikroTik RouterOS.

And anyone who desired to work via more user-friencdly interface now may use this application.

MikroTik-RouterOS-7.3.1.ova - use kernel version other 64x

winbox64.exe - https://mikrotik.com/download

# Pre-Configure 
https://wiki.mikrotik.com/wiki/Manual:First_time_startup

give ip address in winbox

# Install required modules
Netmiko - https://pynet.twb-tech.com/blog/netmiko-python-library.html

PySimpleGUI - https://www.pysimplegui.org/en/latest/ 

```cmd
pip install netmiko
pip install PySimpleGUI
```

# Running it
```cmd
# CLI Interface
python cli_interface.py
# GUI Interface
python gui_interface.py
```

# Features
- IP Address handling: adding, removing, changing connection IP
- Port handling: changing port of services, changing connection PORT(ssh's)
- Firewall rules handling: adding, removing, enabling, disabling
- Getting info about IP Address, Ports, Interfaces, DNS, DHCP and many other things
- Safe Mode
- Sending Any Custom Command

# Note
If you get some error related to patterns then check the problem_solutions folder.

# To-Do
- [x] System should retry to connect every 30 seconds
- [x] Ports and ip address should be able to change
- [x] Disconnect and connect internet(via firewall rule)
- [x] Add some other commands like print ip adresses, interface information and so on
- [x] Enable/ Disable firewall rules 
- [x] Activate safe mode - https://help.mikrotik.com/docs/display/ROS/Configuration+Management#ConfigurationManagement-SafeMode
- [x] GUI - PySimpleGUI
