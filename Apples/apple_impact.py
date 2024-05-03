import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


import pdb


G = 9.81#m/s2

timestep = 0.00001#one tenth of a millisecond
timesteps = np.arange(0, 0.1, timestep)

foam_thickness = 25#mm
useful_percentage = 0.25
useful_foam_thickness = foam_thickness*useful_percentage
foam_pressure = 4#psi
foam_pressure_Pa = foam_pressure*6894#Pa/psi
foam_kmm3 = foam_pressure_Pa/(1000*1000)/useful_foam_thickness




apple_diameter = 80#mm
apple_rad = apple_diameter/2.0
half_sphere_mm2 = 2*np.pi*(apple_diameter/2)**2
apple_mass = 0.238#kg

fall_height = 0.050#meters

energy = []
velocity = []
dists = []
patch_area_mm2 = []
inc_patch_area_mm2 = []
cum_dists = []

#calculate the initial energy
energy.append(apple_mass*G*fall_height)


for t in timesteps:
	velocity.append(np.sqrt(2*energy[-1]/apple_mass))
	dists.append(1000*velocity[-1] * timestep)#1000mm/m
	cum_dists.append(np.sum(dists))
	theta = np.arccos((apple_rad-cum_dists[-1])/apple_rad)
	circle_r = apple_rad*np.sin(theta)
	patch_area_mm2.append(np.pi * circle_r**2)
	if len(patch_area_mm2) < 2:
		inc_patch_area_mm2.append(patch_area_mm2[-1])
	else:
		inc_patch_area_mm2.append(patch_area_mm2[-1] - patch_area_mm2[-2])

	#calculate the energy absorbed during this time step.
	#this is done with E = 1/2 * K *x^2 (spring equation).
	#the trick here is that the center patch which made contact first
	#will have a higher x (distance) into the foam than each subsequent
	#new ring of apple that makes contact with the foam.
	E_absorbed = 0
	cum_dists.reverse()
	for dd in zip(cum_dists, inc_patch_area_mm2):
		K = dd[1]*foam_kmm3*dd[0]
		E_absorbed += 0.5 * K * dd[0]**2/(1000*1000)
	cum_dists.reverse()
	if (energy[-1]<=0): break
	energy.append(energy[-1] - E_absorbed)
	# velocity.append(np.sqrt(2*energy[-1]/apple_mass



#calculate DV/DT = acceleration
accel = []
for v in zip(velocity[1:], velocity[0:-1]):
	accel.append((v[0]-v[1])/timestep)

patch_diameter=[]
for a in patch_area_mm2:
	patch_diameter.append(2*np.sqrt(a/np.pi))







##Now for some plots
fig = make_subplots(
	rows=2,
	cols=3,
	subplot_titles=(
		"Position [mm]",
		"Velocity [m/s]",
		"Acceleration [Gs]",

		"Apple Energy [J]",
		"Patch Area [mm2]",
		"Patch Diameter [mm]",),
	)


dist_trace = go.Scatter(
	x=timesteps,
	y=cum_dists,
	mode="markers",
	marker=dict(size=3, color="blue"),
	name="Dist [mm]",
	)
fig.add_trace(dist_trace, row=1, col=1)



vel_trace = go.Scatter(
	x=timesteps,
	y=velocity,
	mode="markers",
	marker=dict(size=3, color="red"),
	name="Velocity [m/s]",
	)
fig.add_trace(vel_trace, row=1, col=2)


accel_trace = go.Scatter(
	x=timesteps,
	y=[k/9.81 for k in accel],
	mode="markers",
	marker=dict(size=3, color="red"),
	name="Accel [Gs]",
	)
fig.add_trace(accel_trace, row=1, col=3)



energy_trace = go.Scatter(
	x=timesteps,
	y=energy,
	mode="markers",
	marker=dict(size=3,color="green"),
	name="Energy [J]",
	)
fig.add_trace(energy_trace, row=2,col=1)



area_trace = go.Scatter(
	x=timesteps,
	y=patch_area_mm2,
	mode="markers",
	marker=dict(size=3,color="green"),
	name="Contact Area [mm2]",
	)

patch_trace = go.Scatter(
	x=timesteps,
	y=patch_diameter,
	mode="markers",
	marker=dict(size=3, color="blue",),
	name="Patch Diameter [mm]",
	)


fig.add_trace(area_trace, row=2,col=2)
fig.add_trace(patch_trace, row=2, col=3)


fig.show()



pdb.set_trace()

















