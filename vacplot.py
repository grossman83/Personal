import argparse
import json
import pprint as pp
import sys
import traceback
import time

import matplotlib.pyplot as plt
import numpy as np
import serial
from serial.tools import list_ports
from scipy.optimize import minimize


import pdb

TEST_VOLUME = 0.75  # Liter

ATM_PRESS = 100.0  #kPa
IDEAL_GAS = 22.4  #L/mol
TEST_TEMPERATURE = 293.0  #Kelvin
STD_TEMPERATURE = 273.15  #Kelvin


def model_pressure(flow_coeff, volume, time, max_delta_P):
	mols = volume / (IDEAL_GAS * TEST_TEMPERATURE / STD_TEMPERATURE)
	press = max_delta_P * (1 - np.exp(-time / (flow_coeff * mols)))
	return press


def process_flowrate_data(volume, time, delta_P):
	""" expects timeseries data
		time is an iterable of time data in seconds
		delta_P is an iterable same size as time in kPa
		from a vacuum test (evacuating a known volume)
		The evacuation of a fixed volume chamber using a pump closely
		resembles the charge/discharge of a capacitor

		V = V(1-e^(-t/RC))
		I = (V/R)*e^(-t/RC)

		Potential (V) is analogous to Pressure (kPa)
		Resistance (R) is now in units of seconds/mol
		Capacitance (C) is in units of mols

		Current (I) is analogous to rate of change of pressure (kPa/s)

		Gas law: PV=nrT

		We can determine Max flow in Liters/second by converting s/mol,
		using the gas law and 22.4L/mol ideal gas at STP.

		Using pressure samples over time from the evacuation of a known
		volume we can determine the Resistance (R) or flow coefficient
		of the pump, and from the asymptote of the pressure we can
		determine the total potential of the pump (V)
	"""

	#a simple least squares residual objective function
	def obj_fcn(args, volume, max_delta_P, time, delta_P):

		flow_coeff, time_offset = args
		modeled_press = np.array([
			model_pressure(flow_coeff, volume, t+time_offset, max_delta_P) for t in time
		])
		modeled_press = modeled_press.flatten()
		delta_P = np.array(delta_P)

		res = np.sqrt(np.sum((delta_P - modeled_press)**2))

		return res

	#maximum delta P (just use the last few data points)
	max_delta_P = np.median(delta_P[-10:])

	result = minimize(
		obj_fcn,
		(5.0, 0.0),
		args=(volume, max_delta_P, time, delta_P),
		method='Nelder-Mead',
		options={'maxiter':1000, 'disp':True}
	)

	flow_coeff = result['x'][0]
	time_offset = result['x'][1]

	max_flow = (IDEAL_GAS * TEST_TEMPERATURE / STD_TEMPERATURE) / flow_coeff

	return {
		'flow_coeff': flow_coeff,
		'max_delta_P': max_delta_P,
		'max_flow': max_flow,
		'time_offset': time_offset,
	}


def plot_vac_data(ts, delta_P, modeled_press=None):
	""" Generate a plot of the
	"""

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	handles = ax.plot(ts, delta_P, '.b', label="experimental")

	if modeled_press is not None:
		h2 = ax.plot(ts, modeled_press, '-r', label="model")
		handles.extend(h2)

	ax.set_title("Vacuum Data Plot")
	ax.set_xlabel("Time (S)")
	ax.set_ylabel("Differential Pressure (kPa)")
	ax.legend(handles=handles)
	return fig


# def plot_pump_curve(max_delta_P, flow_coeff)


def setup_opts():
	parser = argparse.ArgumentParser(description="Vacuum Plot")

	parser.add_argument(
		"-l",
		"--list",
		action='store_true',
		required=False,
		help="List available ports"
	)

	parser.add_argument(
		"-p",
		"--port",
		type=str,
		required=False,
		help="COM port for pressure sensor data eg: /dev/ttyACM0"
	)

	opts = parser.parse_args()

	return opts


if __name__ == "__main__":

	opts = setup_opts()

	ports = list_ports.comports()

	if opts.list:
		print("Available COM ports:")
		pp.pprint([x.device for x in ports])
		sys.exit(0)

	if opts.port is None:
		if len(ports) == 0:
			print("No COM port detected")
			sys.exit(1)
		elif len(ports) == 1:
			# try to use the only available port
			opts.port = ports[0].device
		else:
			print("Please select a port using --port option:")
			pp.pprint([x.name for x in ports])
			sys.exit(1)

	print("Connecting to: {}".format(opts.port))

	#connect to the comport to collect data
	ser = serial.Serial(opts.port, 115200)
	data = ser.readline(2000) # check that we get something from the port
	if data is None:
		print("No data rxed...")
		sys.exit(1)

	data = []
	start_ts = None
	TIMEOUT = 1000000 #seconds after start detected
	MIN_TRESH = 3.0 #kPa of vacuum (100 - 2 = 98 kPa abs at sea level)
	while True:
		# pdb.set_trace()
		thestr = ser.readline(2000).decode('utf-8')
		micros = int(thestr[0:thestr.find(',')])
		press = float(thestr[thestr.find(',')+2:-1])


		# press = float(ser.readline(1000).decode('utf-8'))
		# ts = time.time()

		# check start condition
		if start_ts is None and press > MIN_TRESH:
			print("Start condition")
			start_ts = micros

		# check timeout condition
		if start_ts is not None:
			if micros - start_ts > TIMEOUT:
				break

		#record and print data
		if start_ts is not None:
			dt = (micros - start_ts)/1000000.0
			data.append((dt, press))
			print("{}, {}".format(dt, press))


	# pdb.set_trace()
	print("Processing Results...")
	ts, delta_P = zip(*data)
	result = process_flowrate_data(TEST_VOLUME, ts, delta_P)
	pp.pprint(result)

	#generate the model fit points
	flow_coeff = result['flow_coeff']
	max_delta_P = result['max_delta_P']
	time_offset = result['time_offset']
	modeled_press = np.array([model_pressure(flow_coeff, TEST_VOLUME, t+time_offset, max_delta_P) for t in ts])

	fig = plot_vac_data(ts, delta_P, modeled_press)

	plt.show(block=True)