import numpy as np
import shapely as sg
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pdb



def make_axes_equal(fig):
    for i in range(1, 4):  # For rows 1 to 3
        for j in range(1, 3):  # For columns 1 to 2
            fig.update_xaxes(scaleanchor=f"y{i}", scaleratio=1, range=[0,2000], row=i, col=j)
            fig.update_yaxes(scaleanchor=f"x{i}", scaleratio=1, range=[-1500,1500],row=i, col=j)




a1_length = 600
a2_length = 600



num_pts = 151

xpos = np.linspace(0,1500, num_pts)
zpos = np.linspace(-1500, 1500, num_pts)

a1 = a1_length * np.ones([num_pts, num_pts])
a2 = a2_length * np.ones([num_pts, num_pts])


mesh = np.meshgrid(xpos, zpos)

xmesh = mesh[0]
zmesh = mesh[1]


# pdb.set_trace()
np.errstate(all='ignore')
# pdb.set_trace()
q2_up = np.arccos((np.square(xmesh) + np.square(zmesh) - np.square(a1) - np.square(a2))/(2*a1*a2))
q1_up = np.arctan(zmesh/xmesh) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))

xposForward = a1*np.cos(q1_up) + a2*np.cos(q1_up+q2_up)
zposForward = a1*np.sin(q1_up) + a2*np.sin(q1_up+q2_up)

# pdb.set_trace()

fig = make_subplots(rows=3, cols=2, subplot_titles=(
	'Thetas of Achievable Cartesian Points',
		'Achievable Cartesian Points',
		'dtheta1/dx',
		'dtheta2/dx',
		'dtheta1/dz',
		'dtheta2/dz',
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
	x = xmesh.flatten(),
	y = zmesh.flatten(),
	mode = "markers",
	marker=dict(size=2, color="red"),
	name="Cartesian Points Attempted",
	)
fig.add_trace(cart_pts, row=1, col=2)


fig.update_xaxes(title_text = 'blah', row=1, col=2)

cart_pts_forward = go.Scatter(
	x = xposForward.flatten(),
	y = zposForward.flatten(),
	mode = "markers",
	marker=dict(size=3, color="green"),
	name="Cartesian Points Achieved",
	)

fig.add_trace(cart_pts_forward, row=1, col=2)



# now I need to play with the jacobian matrix to see where the RPM is high
# and where the accelerations are high.
# to do this I'll take each of the points and move them by 1mm in X and Z
# and see the delta in the theta. This will give me the dx/dtheta
# and the dz/dtheta for each of the axes.

delta = 1
mesh_add = delta * np.ones([num_pts, num_pts])
new_mesh = mesh + mesh_add
new_xmesh = new_mesh[0]
new_zmesh = new_mesh[1]



#dtheta/dx

new_q2_up = np.arccos((np.square(new_xmesh) + np.square(new_zmesh) - np.square(a1) - np.square(a2))/(2*a1*a2))
new_q1_up = np.arctan(new_zmesh/new_xmesh) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))


# cart_vel = 3000#mm/s

def get_ratio(dthetadcart):
	ratio = np.nanmax(np.abs(dthetadcart)) / np.nanmin(np.abs(dthetadcart))
	return the_ratio






dtheta1dx = (new_q1_up - q1_up)/delta#*cart_vel
dtheta2dx = (new_q2_up - q2_up)/delta#*cart_vel

# condition for bit-masking the stuff that is out of the ROM.
# only need to check dtheta1 because it is based on dtheta 2 anyhow
condition  = np.isnan(dtheta1dx)



dtheta1dx_plot = go.Scatter(
    x=xmesh[~condition].flatten(),
    y=zmesh[~condition].flatten(),
    name='dtheta1/dx',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dtheta1dx[~condition].flatten()),
        colorscale='plasma',
        colorbar=dict(title="dtheta1/dx"),
        coloraxis="coloraxis1"  # Link to the first color axis
    ),
    hovertemplate='%{marker.color:.4f}<extra></extra>'
)

dtheta2dx_plot = go.Scatter(
    x=xmesh[~condition].flatten(),
    y=zmesh[~condition].flatten(),
    name='dtheta2/dx',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dtheta2dx[~condition].flatten()),
        colorscale='plasma',
        colorbar=dict(title="dtheta2/dx"),
        coloraxis="coloraxis2"  # Link to the second color axis
    ),
    hovertemplate='%{marker.color:.4f}<extra></extra>'
)

# Add traces to the figure
fig.add_trace(dtheta1dx_plot, row=2, col=1,)
fig.add_trace(dtheta2dx_plot, row=2, col=2,)
# fig.update_layout(title_text='dtheta2/dx')

# Update the layout to include separate color axes
fig.update_layout(
    coloraxis1=dict(colorscale='plasma', colorbar=dict(title="dtheta1dx", x=0.45, y=0.5, len=0.3)),
    coloraxis2=dict(colorscale='plasma', colorbar=dict(title="dtheta2dx", x=1.0, y=0.5, len=0.3))
)



#dtheta/dy
new_q2_up = np.arccos((np.square(xmesh) + np.square(new_zmesh) - np.square(a1) - np.square(a2))/(2*a1*a2))
new_q1_up = np.arctan(new_zmesh/xmesh) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))

dtheta1dz = (new_q1_up - q1_up)/1
dtheta2dz = (new_q2_up - q2_up)/1

condition  = np.isnan(dtheta1dz)#only need to check dtheta1 because it's calculated from dtheta2 anyways
condition2 = np.logical_and(np.abs(dtheta1dz)>0.0005, np.abs(dtheta1dz)<0.01)
all_conditions = np.logical_and(~condition, condition2)


# Create the scatter plots for dtheta/dy
dtheta1dz_plot = go.Scatter(
    x=xmesh[all_conditions].flatten(),
    y=zmesh[all_conditions].flatten(),
    name='dthe1dz',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dtheta1dz[all_conditions].flatten()),
        colorscale='plasma',
        colorbar=dict(title="dtheta1/dz"),
        coloraxis="coloraxis3"  # Link to the first color axis
    ),
    hovertemplate='%{marker.color:.4f}<extra></extra>',
)

condition2 = np.logical_and(np.abs(dtheta2dz)>0.001, np.abs(dtheta2dz)<0.01)
all_conditions = np.logical_and(~condition, condition2)


# Create the second scatter plot
dtheta2dz_plot = go.Scatter(
    x=xmesh[all_conditions].flatten(),
    y=zmesh[all_conditions].flatten(),
    name='dtheta2dz',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dtheta2dz[all_conditions].flatten()),
        colorscale='plasma',
        colorbar=dict(title="dtheta2/dz"),
        coloraxis="coloraxis4" # Link to the second color axis
    ),
    hovertemplate='%{marker.color:.4f}<extra></extra>',
)

# Add traces to the figure
fig.add_trace(dtheta1dz_plot, row=3, col=1,)
fig.add_trace(dtheta2dz_plot, row=3, col=2,)

# Update the layout to include separate color axes
fig.update_layout(
    coloraxis3=dict(colorscale='plasma', colorbar=dict(title="dtheta1dz", x=0.45, y=0.15, len=0.3)),
    coloraxis4=dict(colorscale='plasma', colorbar=dict(title="dtheta2dz", x=1.0, y=0.15, len=0.3))
)



fig.update_layout(
	width = 1800,
	height = 2700,
	)
make_axes_equal(fig)




# Show the plot
fig.show()

pdb.set_trace()


def getLinearPoints(xs, zs, duration, max_speed, max_accel, num_pts):
	dx = xs[1] - xs[0]
	dz = zs[1] - zs[0]

	path_length = np.sqrt(dx**2 + dy**2)
	max_accel_duration = max_speed/max_accel
	if duration > 2*max_accel_duration:
		#the path is long enough that we're going to get a trapezoidal path
		pass


	return 0













