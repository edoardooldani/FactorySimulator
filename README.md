# FactorySimulator
This is a simulation of a factory made with Python as an internship for GRUPPO SIGLA SRL.

The project contains two Python files, client and server. The server file contains the factory (PLC) and the client file contains the supervisor (HMI).

The communication between client and server uses the protocol ModbusTCP, developed using the Python library pyModbusTCP. 
The GUI of the factory is made with pygame. 

This project runs on two different Ubuntu machines and to make it work you have to change server's IP address in the client file. This can work in localhost
but is made to work in two different machines.
