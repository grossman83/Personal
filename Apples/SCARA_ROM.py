import numpy as np
import shapely as sg
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
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

q1_max_torque = 4#N*m
q2_max_torque = 4#N*m


a1_reduction = 16
a2_reduction = 7

a1_efficiency = 0.9
a2_efficiency = 0.9

max_omega_rpm = 900

max_cart_vel = 3000#mm/s
accel_mult = 10#unitless

num_pts = 151
################################ INPUTS ######################################






################################ DERIVED ######################################
a1_inertia = a1_mass * a1_arm**2
a2_inertia = a2_mass * a2_arm**2
max_omega1 = max_omega_rpm * 2 * np.pi / 60 / a1_reduction
max_omega2 = max_omega_rpm * 2 * np.pi / 60 / a2_reduction
max_cart_accel = max_cart_vel * accel_mult

gearbox1_max_torque = q1_max_torque * a1_reduction * a1_efficiency
gearbox2_max_torque = q2_max_torque * a2_reduction * a2_efficiency
################################ DERIVED ######################################


#linspace of points in x and z
xpos = np.linspace(0,1500, num_pts)
zpos = np.linspace(-1500, 1500, num_pts)

#same shape grid of the arm lengths
a1 = a1_length * np.ones([num_pts, num_pts])
a2 = a2_length * np.ones([num_pts, num_pts])

#make linspace into a mesh of points to try
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
		't1(x,z) dx',
		't2(x,z) dx',
		't1(x,z) dz',
		't2(x,z) dz',
		)
)


fig2 = go.Figure()

#create lines that can be revealed upon clicking on the end-point
#this will show the arms when a point is clicked. All I really need
#is the intermediate point because we know that the first point is the
#origin, and the last point is the point clicked. This point is simply
#the position of the second joint.



cart_pts_forward = go.Scatter(
	x = xposForward.flatten(),
	y = zposForward.flatten(),
	mode = "markers",
	marker=dict(size=3, color="green"),
	name="Points",
	)

fig2.add_trace(cart_pts_forward)

j2pos_x = a1*np.cos(q1_up)
j2pos_z = a1*np.sin(q1_up)


xposForward_flat = xposForward.flatten()
zposForward_flat = zposForward.flatten()
j2pos_x_flat = j2pos_x.flatten()
j2pos_z_flat = j2pos_z.flatten()



#################vectorize this#########################
#########this is really slow####################
line_indices = {}
for i in range(len(j2pos_x_flat)):
	line_indices[i] = []
	line_idx = len(fig2.data)
	line_indices[i].append(line_idx)
	thescatter = go.Scatter(
		x = [0, j2pos_x_flat[i], xposForward_flat[i]],
		y = [0, j2pos_z_flat[i], zposForward_flat[i]],
		mode = 'lines',
		line=dict(color='red', width=4),
		showlegend=False,
		hoverinfo='none',
		visible=False,
		)
	fig2.add_trace(thescatter)
#################vectorize this#########################

fig2.update_layout(title='Click To Reveal',
	hovermode='closest'
	)

i=1
fig2.update_xaxes(scaleanchor=f"y{i}",
	scaleratio=1,
	range=[-1000,2000])
fig2.update_yaxes(scaleanchor=f"x{i}",
	scaleratio=1,
	range=[-1500,1500])







angle_pts = go.Scatter(
	x = q1_up.flatten(),
	y = q2_up.flatten(),
	mode="markers",
	marker=dict(size=3, color="blue"),
	name="Joint Angles",
	)
fig.add_trace(angle_pts, row=1, col=1)


# two plots to get an overlay of points achievable and not achievable
cart_pts = go.Scatter(
	x = xmesh.flatten(),
	y = zmesh.flatten(),
	mode = "markers",
	marker=dict(size=2, color="red"),
	name="Cartesian Points Attempted",
	)
fig.add_trace(cart_pts, row=1, col=2)

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
dq2dx = (q2dx - q2_up)/delta #rad/mm
dq1dx = (q1dx - q1_up)/delta


#calculate dtheta/dz
xmesh = mesh[0]
zmesh = mesh[1] + mesh_add
q2dz = np.arccos((np.square(xmesh) + np.square(zmesh) - np.square(a1) - np.square(a2))/(2*a1*a2))
q1dz = np.arctan(zmesh/xmesh) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))
dq2dz = (q2dz - q2_up)/delta #rad/mm
dq1dz = (q1dz - q1_up)/delta



#rotational velocity dtheta/dt for dx/dt
#assumes that we're moving at maximum cartesian velocity parallel to x-axis
dq1xdt = dq1dx * max_cart_vel #rad/mm * mm/s = rad/s
dq2xdt = dq2dx * max_cart_vel
dq1zdt = dq1dz * max_cart_vel
dq2zdt = dq2dz * max_cart_vel

#rotational acceleration for a path parallel to x-axis
dq1xdtdt = dq1dx * max_cart_accel #rad/mm * mm/s2 = rad/s2
dq2xdtdt = dq2dx * max_cart_accel
dq1zdtdt = dq1dz * max_cart_accel
dq2zdtdt = dq2dz * max_cart_accel



# condition for bit-masking the stuff that is out of the ROM.
# only need to check dtheta1 because it is based on dtheta 2 anyhow
nancondition  = np.isnan(dq1dx)

# check that we're below the max motor/geaerbox speed
speed_condition = np.logical_and(
	np.abs(dq1xdt)<max_omega1,
	np.abs(dq2xdt)<max_omega2
	)

#calculate torques due to rotational accelerations of the joints.
t2 = dq2xdtdt * a2_inertia

#torque due to gravity.
tg2 = -1 * a2_mass * a2_arm * np.cos(q2_up+q1_up)#gravity results in - torque
t2 = t2 + tg2
t1 = dq1xdtdt*a1_inertia - np.cos(q1_up)*a1_mass*a1_arm + t2

#@todo
#need torques due to velocity. (dynamics)


torque_condition = np.logical_and(
	np.abs(t1)<gearbox1_max_torque,
	np.abs(t2)<gearbox2_max_torque)

condition = np.logical_and(speed_condition, torque_condition)


#combine all conditions. If I don't remove the points that fail due
#to torque or speed it screws up the scale on the plots.
condition = np.logical_and(condition, ~nancondition)

# pdb.set_trace()


dq1xdt_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    name='t1(x,z) dx',
    mode='markers',
    hoverinfo='none',
    marker=dict(
        size=3,
        color=np.abs(t1[condition].flatten()),
        colorscale='plasma',
        colorbar=dict(title="t1(x,z) dx"),
        coloraxis="coloraxis1",  # Link to the first color axis
    ),
    hovertemplate='%{marker.color:.1f}<extra></extra>'
)

dq2xdt_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    name='t2(x,z) dx',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(t2[condition].flatten()),
        colorscale='plasma',
        colorbar=dict(title="t2(x,z) dx"),
        coloraxis="coloraxis2"  # Link to the second color axis
    ),
    hovertemplate='%{marker.color:.1f}<extra></extra>'
)


#adjust conditions to only show unachievable points due to torque
torque_condition = np.abs(t1)>gearbox1_max_torque
condition = np.logical_and(~nancondition, torque_condition)


dq1dxdt_torque_fail_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    # name='dtheta1/dx',
    mode='markers',
    marker=dict(
        size=3,
        color='red',
    ),
)


speed_condition = np.abs(dq1xdt)>max_omega1
condition = np.logical_and(~nancondition, speed_condition)

dq1dxdt_speed_fail_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    # name='dtheta1/dx',
    mode='markers',
    marker=dict(
        size=3,
        color='black',
    ),
)


fig.add_trace(dq1xdt_plot, row=2, col=1,)
fig.add_trace(dq1dxdt_torque_fail_plot, row=2, col=1,)
fig.add_trace(dq1dxdt_speed_fail_plot, row=2, col=1,)

#############################################

torque_condition = np.abs(t2) > gearbox2_max_torque
condition = np.logical_and(~nancondition, speed_condition)

dq2dxdt_torque_fail_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    # name='dtheta2/dx',
    mode='markers',
    marker=dict(
        size=3,
        color='red',
    ),
)

speed_condition = np.abs(dq2xdt)>max_omega2
condition = np.logical_and(~nancondition, speed_condition)

dq2dxdt_speed_fail_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    # name='dtheta2/dx',
    mode='markers',
    marker=dict(
        size=3,
        color='black',
    ),
)

fig.add_trace(dq2xdt_plot, row=2, col=2,)
fig.add_trace(dq2dxdt_torque_fail_plot, row=2, col=2,)
fig.add_trace(dq2dxdt_speed_fail_plot, row=2, col=2,)

# fig.update_xaxes(nticks=)
fig.update_xaxes(minor=dict(ticklen=6, tickcolor="black", showgrid=True))
fig.update_xaxes(minor_ticks="inside")

fig.update_yaxes(minor=dict(ticklen=6, tickcolor="black", showgrid=True))
fig.update_yaxes(minor_ticks="inside")


# Update the layout to include separate color axes and locate them on the page
fig.update_layout(
    coloraxis1=dict(colorscale='plasma', colorbar=dict(title="t1(x,z) dx", x=0.45, y=0.5, len=0.3)),
    coloraxis2=dict(colorscale='plasma', colorbar=dict(title="t2(x,z) dx", x=1.0, y=0.5, len=0.3))
)



#calculate dtheta/dz
xmesh = mesh[0] 
zmesh = mesh[1] + mesh_add
q2dz = np.arccos((np.square(xmesh) + np.square(zmesh) - np.square(a1) - np.square(a2))/(2*a1*a2))
q1dz = np.arctan(zmesh/xmesh) - np.arctan((a2*np.sin(q2_up))/(a1+a2*np.cos(q2_up)))
dq2dz = (q2dz - q2_up)/delta
dq1dz = (q1dz - q1_up)/delta


#conditions
# condition for bit-masking the stuff that is out of the ROM.
# only need to check dtheta1 because it is based on dtheta 2 anyhow
nancondition  = np.isnan(dq1dz)

# check that we're below the max motor/geaerbox speed
speed_condition = np.logical_and(
	np.abs(dq1zdt)<max_omega1,
	np.abs(dq2zdt)<max_omega2
	)

#calculate torques due to rotational accelerations of the joints.
t2 = dq2zdtdt * a2_inertia

#torque due to gravity.
tg2 = -1 * a2_mass * a2_arm * np.cos(q2_up+q1_up)#gravity results in - torque

t2 = t2 + tg2
t1 = dq1zdtdt*a1_inertia - np.cos(q1_up)*a1_mass*a1_arm + t2

#@todo
#need torques due to velocity. (dynamics)


torque_condition = np.logical_and(
	np.abs(t1)<gearbox1_max_torque, np.abs(t2)<gearbox2_max_torque)

condition = np.logical_and(speed_condition, torque_condition)


#combine all conditions. If I don't remove the points that fail due
#to torque or speed it screws up the scale on the plots.
condition = np.logical_and(condition, ~nancondition)


dq1dz_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    name='t1(x,z) dz',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(t1[condition].flatten()),
        colorscale='plasma',
        colorbar=dict(title="t1(x,z) dz"),
        coloraxis="coloraxis3"  # Link to the proper color axis
    ),
    hovertemplate='%{marker.color:.1f}<extra></extra>',
)


dq2dz_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    name='t2(x,z) dz',
    mode='markers',
    marker=dict(
        size=3,
        color=np.abs(dq2zdt[condition].flatten()),
        colorscale='plasma',
        colorbar=dict(title="t2(x,z) dz"),
        coloraxis="coloraxis4" # Link to the proper color axis
    ),
    hovertemplate='%{marker.color:.1f}<extra></extra>',
)

#add both plots to the figure
fig.add_trace(dq1dz_plot, row=3, col=1,)
fig.add_trace(dq2dz_plot, row=3, col=2,)




#######################################
#adjust conditions to only show unachievable points due to torque
torque_condition = np.abs(t1)>gearbox1_max_torque
condition = np.logical_and(~nancondition, torque_condition)


dq1dzdt_torque_fail_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    # name='dq1/dz',
    mode='markers',
    marker=dict(
        size=3,
        color='red',
    ),
)


speed_condition = np.abs(dq1zdt)>max_omega1
condition = np.logical_and(~nancondition, speed_condition)

dq1dzdt_speed_fail_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    # name='dq1/dz',
    mode='markers',
    marker=dict(
        size=3,
        color='black',
    ),
)

fig.add_trace(dq1dzdt_torque_fail_plot, row=3, col=1)
fig.add_trace(dq1dzdt_speed_fail_plot, row=3, col=1)



torque_condition = np.abs(t2)>gearbox2_max_torque
condition = np.logical_and(~nancondition, torque_condition)


dq2dzdt_torque_fail_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    # name='dq1/dz',
    mode='markers',
    marker=dict(
        size=3,
        color='red',
    ),
)

speed_condition = np.abs(dq1zdt)>max_omega2
condition = np.logical_and(~nancondition, speed_condition)

dq2dzdt_speed_fail_plot = go.Scatter(
    x=xmesh[condition].flatten(),
    y=zmesh[condition].flatten(),
    # name='dq1/dz',
    mode='markers',
    marker=dict(
        size=3,
        color='black',
    ),
)

fig.add_trace(dq2dzdt_torque_fail_plot, row=3, col=2)
fig.add_trace(dq2dzdt_speed_fail_plot, row=3, col=2)
# Update the layout to include separate color axes
fig.update_layout(
    coloraxis3=dict(colorscale='plasma', colorbar=dict(title="dq1dz", x=0.45, y=0.1, len=0.3)),
    coloraxis4=dict(colorscale='plasma', colorbar=dict(title="dq2dz", x=1.0, y=0.1, len=0.3))
)



fig.update_layout(
	width = 1800,
	height = 2700,
	)
make_axes_equal(fig)



# JavaScript code to add click events (to be used with Plotly's HTML export)
js_code = """
document.querySelectorAll('.plotly-graph-div').forEach(function (div) {
    div.on('plotly_click', function (data) {
        var pointIndex = data.points[0].pointIndex;
        var lines = %s[pointIndex];
        var visibility = div.data[lines[0]].visible === true ? false : true;
        var update = {'visible': visibility};
        for (var i = 0; i < lines.length; i++) {
            Plotly.restyle(div, update, [lines[i]]);
        }
    });
});
""" % (line_indices,)

# Export to HTML with embedded JavaScript
pio.write_html(fig2,
	file='click_reveal_lines.html',
	auto_open=True,
	include_plotlyjs='cdn',
	config={'displayModeBar': False},
	post_script=js_code)





# fig2.show(config={'displayModeBar': False})
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













