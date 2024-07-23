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





################################ INPUTS ######################################
a1_length = 600
a2_length = 600

a1_mass = 3.6#kg
a2_mass = 3.85#kg

a1_arm = 0.213#m
a2_arm = 0.257#m

q1_max_torque = 8#N*m
q2_max_torque = 8#N*m


a1_reduction = 16
a2_reduction = 10

max_omega_rpm = 1200
max_torque = 100#N*m (omega**2 * inertia)

max_cart_vel = 3000#mm/s
accel_multiple = 10

num_pts = 151
################################ INPUTS ######################################






################################ DERIVED ######################################
a1_inertia = a1_mass * a1_arm**2
a2_inertia = a2_mass * a2_arm**2
max_omega1 = max_omega_rpm * 2 * np.pi / 60 / a1_reduction
max_omega2 = max_omega_rpm * 2 * np.pi / 60 / a2_reduction
max_cart_accel = max_cart_vel * accel_multiple

gearbox1_max_torque = q1_max_torque * a1_reduction
gearbox2_max_torque = q2_max_torque * a2_reduction
################################ DERIVED ######################################



xpos = np.linspace(0,1500, num_pts)
zpos = np.linspace(-1500, 1500, num_pts)

a1 = a1_length * np.ones([num_pts, num_pts])
a2 = a2_length * np.ones([num_pts, num_pts])


mesh = np.meshgrid(xpos, zpos)

xmesh = mesh[0]
zmesh = mesh[1]


#trying to get it to stop telling me about divide by zero and stuff.
np.errstate(all='ignore')


#named qn_up because this is the up solve for the x,z position. There
#is another way to get to the same position and that is the down solve.
q2_up = np.arccos((np.square(xmesh) + np.square(zmesh) - np.square(a1) - np.square(a2))/(2*a1*a2))
q1_up = np.arctan(zmesh/xmesh) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))

xposForward = a1*np.cos(q1_up) + a2*np.cos(q1_up+q2_up)
zposForward = a1*np.sin(q1_up) + a2*np.sin(q1_up+q2_up)


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

#calculate dtheta/dx
xmesh = mesh[0] + mesh_add
zmesh = mesh[1]
q2dx = np.arccos((np.square(xmesh) + np.square(zmesh) - np.square(a1) - np.square(a2))/(2*a1*a2))
q1dx = np.arctan(zmesh/xmesh) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))
dq2dx = (q2dx - q2_up)/delta
dq1dx = (q1dx - q1_up)/delta


#calculate dtheta/dz
xmesh = mesh[0]
zmesh = mesh[1] + mesh_add
q2dz = np.arccos((np.square(xmesh) + np.square(zmesh) - np.square(a1) - np.square(a2))/(2*a1*a2))
q1dz = np.arctan(zmesh/xmesh) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))
dq2dz = (q2dz - q2_up)/delta
dq1dz = (q1dz - q1_up)/delta


#dtheta/dt = dtheta/dx * dx/dt (where dx/dt is max_cart_vel) [rad/s]
#dtheta/dt^2 = dtheta/dx * dx/dt * dx/dt [rad/s2]

# renamed these to dqndx and dqndz
# dtheta1dx = (new_q1_up - q1_up)/delta#*cart_vel
# dtheta2dx = (new_q2_up - q2_up)/delta#*cart_vel


dq1xdt = dq1dx * max_cart_vel
dq2xdt = dq2dx * max_cart_vel

dq1xdtdt = dq1xdt * max_cart_accel
dq2xdtdt = dq2xdt * max_cart_accel



# condition for bit-masking the stuff that is out of the ROM.
# only need to check dtheta1 because it is based on dtheta 2 anyhow
nancondition  = np.isnan(dq1dx)
# now various maskings to make sure that we're below the max motor speed
speed_condition = np.logical_and(
	np.abs(dq1xdt)<max_omega1,
	np.abs(dq2xdt)<max_omega2
	)

#calculate torques due to rotational accelerations of the joints.
t2 = dq2xdtdt * a2_inertia

#torque due to gravity.
tg2 = -1 * a2_mass * a2_arm * np.cos(q2_up+q1_up)#gravity results in - torque
t2 = t2 + tg2

#@todo
#need torques due to velocity.

t1 = dq1xdtdt*a1_inertia - np.cos(q1_up)*a1_mass*a1_arm + t2

torque_condition = np.logical_and(
	np.abs(t1<gearbox1_max_torque), np.abs(t2<gearbox2_max_torque))

condition = np.logical_and(speed_condition, torque_condition)


#combine all conditions
condition = np.logical_and(~nancondition, condition)


#Trying a way to combine many logical arrays into one with and
# condition_test = np.logical_and.reduce((
# 	nancondition,
# 	np.abs(dtheta1dt)<max_omega1,
# 	np.abs(dtheta2dt)<max_omega2
# 	 ))




dq1xdt_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    name='dtheta1/dx',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dq1xdt[condition].flatten()),
        colorscale='plasma',
        colorbar=dict(title="dtheta1/dx"),
        coloraxis="coloraxis1"  # Link to the first color axis
    ),
    hovertemplate='%{marker.color:.4f}<extra></extra>'
)
fig.add_trace(dq1xdt_plot, row=2, col=1,)
fig.update_layout(
	width = 1800,
	height = 2700,
	)
make_axes_equal(fig)
fig.show()
pdb.set_trace()

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


# this was meant to work on the motion and timing. I'll come back to it later.
# def getLinearPoints(x_if, z_if, duration, max_speed, max_accel, num_pts):
# 	dx = x_if[1] - x_if[0]
# 	dz = z_if[1] - z_if[0]
# 	dt = 

# 	path_length = np.sqrt(dx**2 + dy**2)
# 	max_accel_duration = max_speed/max_accel
# 	if duration > 2*max_accel_duration:
# 		#the path is long enough that we're going to get a trapezoidal path
# 		xs = np.zeros(num_pts)
# 		zs = np.zeros(num_pts)

# 		xs[0] = x_if[0]
# 		xs[-1] = x_if[1]

# 		#determine if max accel is needed to reach max speed not overshoot
# 		if (dx < 0.5*max_accel*dt**2):
# 			#accel at max velosity for timestep





# 	if duration <= 2*max_accel_duration:
# 		pass


# 	return 0













