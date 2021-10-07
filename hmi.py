#!/usr/bin/env python

import pprint
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk
from pyModbusTCP.client import ModbusClient
from time import sleep
from pymodbus.exceptions import ConnectionException

MODBUS_SLEEP=1

class HMIWindow(Gtk.Window):

    connected = False

    def initModbus(self):

        self.modbusClient = ModbusClient(host='192.168.1.63', port=12345)
        if self.modbusClient.open():
            self.connected = True
            self.modbusClient.write_single_register(0, 1)
        else:
            self.connected = False
            self.modbusClient.write_single_register(0, 0)

    def resetLabels(self):
        self.connectionStatusValue.set_markup("<span weight='bold' foreground='red'>OFFLINE</span>")
        self.motorStatusValue.set_markup("<span weight='bold' foreground='gray33'>N/A</span>")
        self.weavingLoomValue.set_markup("<span weight='bold' foreground='gray33'>N/A</span>")
        self.conveyorBeltValue.set_markup("<span weight='bold' foreground='gray33'>N/A</span>")
        self.hydraulicPressValue.set_markup("<span weight='bold' foreground='gray33'>N/A</span>")
        self.woolReadyValue.set_markup("<span weight='bold' foreground='gray33'>N/A</span>")
        self.woolenHatsCompletedValue.set_markup("<span weight='bold' foreground='gray33'>N/A</span>")


    def __init__(self):
        Gtk.Window.__init__(self, title="Woolen hats for cats factory - HMI")

        self.set_border_width(15)
        
        self.initModbus()

        elementIndex = 0

        # Grid
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        self.add(grid)

        # Main title label
        label = Gtk.Label()
        label.set_markup("<span  weight='bold' font='35'>Woolen hats for cats process status</span>")
        grid.attach(label, 0, elementIndex, 2, 1)
        elementIndex += 1

        # Motor status label
        motorStatusLabel = Gtk.Label()
        motorStatusLabel.set_markup("<span weight='bold' font='24'>Motor status</span>")
        motorStatusValue = Gtk.Label()
        grid.attach(motorStatusLabel, 0, elementIndex, 1, 1)
        grid.attach(motorStatusValue, 1, elementIndex, 1, 1)
        elementIndex += 1

        # Conveyor belt status label
        conveyorBeltLabel = Gtk.Label()
        conveyorBeltLabel.set_markup("<span weight='bold' font='24'>Conveyor belt status</span>")
        conveyorBeltValue = Gtk.Label()
        grid.attach(conveyorBeltLabel, 0, elementIndex, 1, 1)
        grid.attach(conveyorBeltValue, 1, elementIndex, 1, 1)
        elementIndex += 1

        # Weaving loom status label
        weavingLoomLabel = Gtk.Label()
        weavingLoomLabel.set_markup("<span weight='bold' font='24'>Weaving loom status</span>")
        weavingLoomValue = Gtk.Label()
        grid.attach(weavingLoomLabel, 0, elementIndex, 1, 1)
        grid.attach(weavingLoomValue, 1, elementIndex, 1, 1)
        elementIndex += 1

        # Hydraulic press status
        hydraulicPressLabel = Gtk.Label()
        hydraulicPressLabel.set_markup("<span weight='bold' font='24'>Hydraulic press status</span>")
        hydraulicPressValue = Gtk.Label()
        grid.attach(hydraulicPressLabel, 0, elementIndex, 1, 1)
        grid.attach(hydraulicPressValue, 1, elementIndex, 1, 1)
        elementIndex += 1

        # Wool ready label
        woolReadyLabel = Gtk.Label()
        woolReadyLabel.set_markup("<span weight='bold' font='24'>Wool pieces ready for processing</span>")
        woolReadyValue = Gtk.Label()
        grid.attach(woolReadyLabel, 0, elementIndex, 1, 1)
        grid.attach(woolReadyValue, 1, elementIndex, 1, 1)
        elementIndex += 1

        # Woolen hats completed
        woolenHatsCompletedLabel = Gtk.Label()
        woolenHatsCompletedLabel.set_markup("<span weight='bold' font='24'>Woolen hats completed</span>")
        woolenHatsCompletedValue = Gtk.Label()
        grid.attach(woolenHatsCompletedLabel, 0, elementIndex, 1, 1)
        grid.attach(woolenHatsCompletedValue, 1, elementIndex, 1, 1)
        elementIndex += 1

        # Connection status
        connectionStatusLabel = Gtk.Label()
        connectionStatusLabel.set_markup("<span weight='bold' font='24'>Connection status</span>")
        connectionStatusValue = Gtk.Label()
        grid.attach(connectionStatusLabel, 0, elementIndex, 1, 1)
        grid.attach(connectionStatusValue, 1, elementIndex, 1, 1)
        elementIndex += 1


        # Run and Stop buttons
        runButton = Gtk.Button(label="Run")
        stopButton = Gtk.Button(label="Stop")
        resetButton = Gtk.Button(label="Reset")
		
        runButton.connect("clicked", self.setProcess, 1)
        stopButton.connect("clicked", self.setProcess, 0)
        resetButton.connect("clicked", self.resetProcess, 1)
		
        grid.attach(runButton, 0, elementIndex, 1, 1)
        grid.attach(stopButton, 1, elementIndex, 1, 1)
        grid.attach(resetButton, 2, elementIndex, 1, 1)
        elementIndex += 2

        
        # Attach Value Labels
        self.woolenHatsCompletedValue = woolenHatsCompletedValue
        self.connectionStatusValue = connectionStatusValue
        self.weavingLoomValue = weavingLoomValue
        self.motorStatusValue = motorStatusValue
        self.woolReadyValue = woolReadyValue
        self.conveyorBeltValue = conveyorBeltValue
        self.hydraulicPressValue = hydraulicPressValue

        self.resetLabels()

        GLib.timeout_add_seconds(MODBUS_SLEEP, self.update_status)

    def setProcess(self, widget, data=None):
        try:

            #If we have not connection when starting the process we try again the connection
            if not self.connected:
                print("Not connected: trying again...")
                self.initModbus()
            else:
                self.modbusClient.write_single_register(1, data)
        except:
            pass

    def resetProcess(self, widget, data=None):
        try:
            self.modbusClient.write_single_register(2, data)
        except:
            pass

    def update_status(self):

        try:
            connectionReg = self.modbusClient.read_holding_registers(0)

            if connectionReg != [1] or not self.connected:
                self.connected = False
                self.connectionStatusValue.set_markup("<span weight='bold' font='24'  foreground='red'>Offline</span>")
            else:
                self.connectionStatusValue.set_markup("<span weight='bold' font='24'  foreground='green'>Online</span>")
            
                regs = list(self.modbusClient.read_holding_registers(10,6))
                    
                if regs[0] == 1:
                    self.conveyorBeltValue.set_markup("<span weight='bold' font='24'  foreground='green'>On</span>")
                else:
                    self.conveyorBeltValue.set_markup("<span weight='bold' font='24'  foreground='red'>Off</span>")

                if regs[1] == 1:
                    self.motorStatusValue.set_markup("<span weight='bold' font='24' foreground='green'>On</span>")
                else:
                    self.motorStatusValue.set_markup("<span weight='bold' font='24' foreground='red'>Off</span>")

                if regs[2] == 1:
                    self.weavingLoomValue.set_markup("<span weight='bold' font='24' foreground='green'>On</span>")
                else:
                    self.weavingLoomValue.set_markup("<span weight='bold' font='24'foreground='red'>Off</span>")

                if regs[3] == 1:
                    self.hydraulicPressValue.set_markup("<span weight='bold' font='24'  foreground='green'>On</span>")
                else:
                    self.hydraulicPressValue.set_markup("<span weight='bold' font='24'  foreground='red'>Off</span>")
                
                stringWoolPiecesValue = "<span weight='bold' font='24' foreground='grey33'>" + str(regs[4]) + "</span>"
                self.woolReadyValue.set_markup(stringWoolPiecesValue)

                stringWoolenHatsValue = "<span weight='bold' font='24' foreground='grey33'>" + str(regs[5]) + "</span>"
                self.woolenHatsCompletedValue.set_markup(stringWoolenHatsValue)
            
    
        except:
            raise
        finally:
            return True

def app_main():
    win = HMIWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

if __name__ == "__main__":
    app_main()
    Gtk.main()

