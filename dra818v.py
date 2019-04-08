#!/usr/bin/env python
import serial
import time


#############################################################################
# Parameters configulation, Change any to match your requirement
#############################################################################
# Default Transmitter / Squelch Settings
PORT = '/dev/ttyAMA0'
FREQUENCY1 = 144.390
FREQUENCY2 = 145.825
MODE = 0 # 1 = FM (supposedly 5kHz deviation), 0 = NFM (2.5 kHz Deviation)
SQUELCH = 0 # Squelch Value, 0-8
CTCSS = '0000'
VOLUMN = 7



#############################################################################
# Module Initial Command
#############################################################################

# Open serial port
_s = serial.Serial(
	port=PORT,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
		timeout=0.5)

# We need to issue this command to be able to send further commands.
_s.write("AT+DMOCONNECT\r\n")
_response = _s.readline()
print("Setup: %s" % _response)

# Set volumn
_s.write("AT+DMOSETVOLUME=%d\r\n" % (VOLUMN))
_response = _s.readline()
print("Setup: %s" % _response)

# Set Filter 
_s.write("AT+SETFILTER=0,0,0\r\n")
_response = _s.readline()
print("Setup: %s" % _response.strip())

# Send the programming command..
_s.write("AT+DMOSETGROUP=%d,%3.4f,%3.4f,%s,%d,%s\r\n" % (MODE, FREQUENCY1, FREQUENCY1, CTCSS, SQUELCH, CTCSS))
_response = _s.readline()
print("Setup: %s" % _response.strip())


#############################################################################
# Main Loop Running
#############################################################################
print("Continue working ...")
# SCANNING FREQUENCY
while True:
	_s.write("AT+DMOSETGROUP=%d,%3.4f,%3.4f,%s,%d,%s\r\n" % (MODE, FREQUENCY1, FREQUENCY1, CTCSS, SQUELCH, CTCSS))
	_response = _s.readline()
	while True: 
		_s.write("RSSI?\r\n")
		_response = _s.readline().strip()
		if "RSSI" in _response:
			rssi = int(_response.split('=')[1])
			if rssi > 50:
				print("FOUND 144.390")
			else:
				break
	
	_s.write("AT+DMOSETGROUP=%d,%3.4f,%3.4f,%s,%d,%s\r\n" % (MODE, FREQUENCY2, FREQUENCY2, CTCSS, SQUELCH, CTCSS))
	_response = _s.readline()
	while True: 
		_s.write("RSSI?\r\n")
		_response = _s.readline().strip()
		if "RSSI" in _response:
			rssi = int(_response.split('=')[1])
			if rssi > 50:
				print("FOUND 145.825")
			else:
				break


_s.close() # May not used because never close serialport during program running
