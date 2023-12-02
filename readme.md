# Description
This codes aim to work with MikroTik RouterOS.

And anyone who desired to work via more user-friencdly interface now may use this project.

MikroTik-RouterOS-7.3.1.ova - user kernel version other 64x

winbox64.exe - https://mikrotik.com/download

# Pre-Configure 
https://wiki.mikrotik.com/wiki/Manual:First_time_startup

give ip address in winbox

# Install required modules
Netmiko - https://pynet.twb-tech.com/blog/netmiko-python-library.html

```cmd
pip install netmiko
```

# Note
If you get some error related to pattern then check problemsolved.jpg

# To-Do
- [x] System should retry to connect every 30 seconds
- [x] Ports and ip address should be able to change
- [x] Disconnect and connect internet(via firewall rule)
- [x] Add some other commands like print ip adresses, interface information and so on
- [x] Enable/ Disable firewall rules 
- [x] Activate safe mode - https://help.mikrotik.com/docs/display/ROS/Configuration+Management#ConfigurationManagement-SafeMode
- [ ] GUI - PySimpleGUI