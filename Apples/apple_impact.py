import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


import pdb


G = 9.81#m/s2

timestep = 0.00001#one tenth of a millisecond
timesteps = np.arange(0, 0.1, timestep)

foam_thickness = 8#mm
useful_percentage = 0.25
useful_foam_thickness = foam_thickness*useful_percentage
foam_pressure = 4#psi
foam_pressure_Pa = foam_pressure*6894#Pa/psi
foam_kmm3 = foam_pressure_Pa/(1000*1000)/useful_foam_thickness




apple_diameter = 80#mm
apple_rad = apple_diameter/2.0
apple_mass = 0.238#kg

fall_height = 0.050#meters

#now for each timestep take energy remaining in the apple from
#the previous timestep, calc speed, calc forces etc

# energy = np.zeros(len(timesteps))
# velocity = np.zeros(len(timesteps))
# sphere_area_mm2 = np.zeros(len(timesteps))
# dists = np.zeros(len(timesteps))
# inc_sphere_force = np.zeros(len(timesteps))


energy = []
velocity = []
sphere_area_mm2 = []
dists = []
inc_sphere_area_mm2 = []
cum_dists = []

energy.append(apple_mass*G*fall_height)
k = 0

half_sphere_mm2 = 2*np.pi*(apple_diameter/2)**2

for t in timesteps:
	velocity.append(np.sqrt(2*energy[-1]/apple_mass))
	dists.append(1000*velocity[-1] * timestep)#units of mm
	cum_dists.append(np.sum(dists))
	theta = np.arccos((apple_rad-cum_dists[-1])/apple_rad)
	cyl_r = apple_rad*np.sin(theta)
	sphere_area_mm2.append(np.pi * cyl_r**2)
	if len(sphere_area_mm2) < 2:
		inc_sphere_area_mm2.append(sphere_area_mm2[-1])
	else:
		inc_sphere_area_mm2.append(sphere_area_mm2[-1] - sphere_area_mm2[-2])

	#calculate the energy absorbed during this time step. It is the 
	#1/2 k*x**2 for each contact patch. The first contact patch has x
	#equal to the total distance and the second contact patch has x equal
	#to the sum excluding the first and so on.
	E_absorbed = 0
	cum_dists.reverse()
	for dd in zip(cum_dists, inc_sphere_area_mm2):
		E_absorbed += 0.5 * dd[1]*foam_kmm3 * dd[0]**2/1000
	cum_dists.reverse()
	if (energy[-1]<=0): break
	energy.append(energy[-1] - E_absorbed)
	# velocity.append(np.sqrt(2*energy[-1]/apple_mass


#calculate DV/DT = acceleration
accel = []
for v in zip(velocity[1:], velocity[0:-1]):
	accel.append((v[0]-v[1])/timestep)







##Now for some plots
fig = make_subplots(rows=2, cols=2)

dist_trace = go.Scatter(
	x=timesteps,
	y=cum_dists,
	mode="markers",
	marker=dict(size=3, color="blue"),
	name="Dist [mm]",
	)
fig.add_trace(dist_trace, row=1, col=1)

accel_trace = go.Scatter(
	x=timesteps,
	y=accel,
	mode="markers",
	marker=dict(size=3, color="red"),
	name="Accel [m/s2]",
	)
fig.add_trace(accel_trace, row=2, col=1)

energy_trace = go.Scatter(
	x=timesteps,
	y=energy,
	mode="markers",
	marker=dict(size=3,color="green"),
	name="Energy [J]",
	)
fig.add_trace(energy_trace, row=1,col=2)


fig.show()



# pdb.set_trace()

















