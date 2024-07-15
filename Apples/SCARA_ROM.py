import numpy as np
import shapely as sg
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pdb


a1_length = 600
a2_length = 600



num_pts = 151

xpos = np.linspace(0,1500, num_pts)
zpos = np.linspace(-1500, 1500, num_pts)

a1 = a1_length * np.ones([num_pts, num_pts])
a2 = a2_length * np.ones([num_pts, num_pts])


mesh = np.meshgrid(xpos, zpos)

# pdb.set_trace()
np.errstate(all='ignore')
# pdb.set_trace()
q2_up = np.arccos((np.square(mesh[0]) + np.square(mesh[1]) - np.square(a1) - np.square(a2))/(2*a1*a2))
q1_up = np.arctan(mesh[1]/mesh[0]) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))

xposForward = a1*np.cos(q1_up) + a2*np.cos(q1_up+q2_up)
zposForward = a1*np.sin(q1_up) + a2*np.sin(q1_up+q2_up)

# pdb.set_trace()

fig = make_subplots(rows=3, cols=2, subplot_titles=(
	'Thetas of Achievable Cartesian Points',
		'Achievable Cartesian Points',
		'dtheta1/dx',
		'dtheta2/dx',
		'dtheta1/dy',
		'dtheta2/dy',
		)
)


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
		),
	width = 1800,
	height = 1800,
	)

cart_pts_forward = go.Scatter(
	x = xposForward.flatten(),
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






# pdb.set_trace()

# now I need to play with the jacobian matrix to see where the RPM is high
# and where the accelerations are high.
# to do this I'll take each of the points and move them by 1mm in X and Z
# and see the delta in the theta. This will give me the dx/dtheta
# and the dz/dtheta for each of the axes.

mesh_add = 1 * np.ones([num_pts, num_pts])
new_mesh = mesh + mesh_add



#dtheta/dx

new_q2_up = np.arccos((np.square(new_mesh[0]) + np.square(mesh[1]) - np.square(a1) - np.square(a2))/(2*a1*a2))
new_q1_up = np.arctan(mesh[1]/new_mesh[0]) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))

dtheta1dx = (new_q1_up - q1_up)/1
dtheta2dx = (new_q2_up - q2_up)/1


# condition for bit-masking the stuff that is out of the ROM.
# only need to check dtheta1 because it is based on dtheta 2 anyhow
condition  = np.isnan(dtheta1dx)



dtheta1dx_plot = go.Scatter(
    x=mesh[0][~condition].flatten(),
    y=mesh[1][~condition].flatten(),
    name='dtheta1/dx',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dtheta1dx[~condition].flatten()),
        colorscale='magma',
        colorbar=dict(title="dtheta1/dx"),
        coloraxis="coloraxis1"  # Link to the first color axis
    )
)

dtheta2dx_plot = go.Scatter(
    x=mesh[0][~condition].flatten(),
    y=mesh[1][~condition].flatten(),
    name='dtheta2/dx',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dtheta2dx[~condition].flatten()),
        colorscale='magma',
        colorbar=dict(title="dtheta2/dx"),
        coloraxis="coloraxis2"  # Link to the second color axis
    )
)

# Add traces to the figure
fig.add_trace(dtheta1dx_plot, row=2, col=1,)
fig.add_trace(dtheta2dx_plot, row=2, col=2,)
# fig.update_layout(title_text='dtheta2/dx')

# Update the layout to include separate color axes
fig.update_layout(
    coloraxis1=dict(colorscale='magma', colorbar=dict(title="dtheta1dx", x=0.45, y=0.5, len=0.3)),
    coloraxis2=dict(colorscale='magma', colorbar=dict(title="dtheta2dx", x=1.0, y=0.5, len=0.3))
)



#dtheta/dy
new_q2_up = np.arccos((np.square(mesh[0]) + np.square(new_mesh[1]) - np.square(a1) - np.square(a2))/(2*a1*a2))
new_q1_up = np.arctan(new_mesh[1]/mesh[0]) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))

dtheta1dy = (new_q1_up - q1_up)/1
dtheta2dy = (new_q2_up - q2_up)/1

condition  = np.isnan(dtheta1dy)


# Create the scatter plots for dtheta/dy
dtheta1dz_plot = go.Scatter(
    x=mesh[0][~condition].flatten(),
    y=mesh[1][~condition].flatten(),
    name='dthe1dz',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dtheta1dy[~condition].flatten()),
        colorscale='magma',
        colorbar=dict(title="dtheta1/dz"),
        coloraxis="coloraxis3"  # Link to the first color axis
    )
)

# Create the second scatter plot
dtheta2dz_plot = go.Scatter(
    x=mesh[0][~condition].flatten(),
    y=mesh[1][~condition].flatten(),
    name='dtheta2dz',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dtheta2dy[~condition].flatten()),
        colorscale='magma',
        colorbar=dict(title="dtheta2/dz"),
        coloraxis="coloraxis4" # Link to the second color axis
    )
)

# Add traces to the figure
fig.add_trace(dtheta1dz_plot, row=3, col=1,)
fig.add_trace(dtheta2dz_plot, row=3, col=2,)

# Update the layout to include separate color axes
fig.update_layout(
    coloraxis3=dict(colorscale='magma', colorbar=dict(title="dtheta1dz", x=0.45, y=0.15, len=0.3)),
    coloraxis4=dict(colorscale='magma', colorbar=dict(title="dtheta2dz", x=1.0, y=0.15, len=0.3))
)







# Show the plot
fig.show()











