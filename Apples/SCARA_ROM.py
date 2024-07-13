import numpy as np
import shapely as sg
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pdb


a1_length = 800
a2_length = 600



num_pts = 151

ypos = np.linspace(0,1500, num_pts)
zpos = np.linspace(-1500, 1500, num_pts)

a1 = a1_length * np.ones([num_pts, num_pts])
a2 = a2_length * np.ones([num_pts, num_pts])

mesh = np.meshgrid(ypos, zpos)


q2_up = np.arccos((np.square(mesh[0]) + np.square(mesh[1]) - np.square(a1) - np.square(a2))/(2*a1*a2))
q1_up = np.arctan(mesh[1]/mesh[0]) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))



yposForward = a1*np.cos(q1_up) + a2*np.cos(q1_up+q2_up)
zposForward = a1*np.sin(q1_up) + a2*np.sin(q1_up+q2_up)



fig = make_subplots(rows=2, cols=2)


angle_pts = go.Scatter(
	x = q1_up.flatten(),
	y = q2_up.flatten(),
	mode="markers",
	marker=dict(size=3, color="blue"),
	name="Joint Angles",
	)
fig.add_trace(angle_pts, row=1, col=1)


cart_pts = go.Scatter(
	x = mesh[0].flatten(),
	y = mesh[1].flatten(),
	mode = "markers",
	marker=dict(size=2, color="red"),
	name="Cartesian Points Attempted",
	)
fig.add_trace(cart_pts, row=1, col=2)
fig.update_layout(
	xaxis = dict(
		scaleanchor='y',
		scaleratio=1,
		),
	yaxis = dict(
		scaleanchor='x',
		scaleratio=1,
		)
	)

cart_pts_forward = go.Scatter(
	x = yposForward.flatten(),
	y = zposForward.flatten(),
	mode = "markers",
	marker=dict(size=3, color="green"),
	name="Cartesian Points Achieved",

	)
fig.add_trace(cart_pts_forward, row=1, col=2)
fig.update_layout(
	xaxis = dict(
		scaleanchor='y',
		scaleratio=1,
		),
	yaxis = dict(
		scaleanchor='x',
		scaleratio=1,
		)
	)


fig.show()



pdb.set_trace()








