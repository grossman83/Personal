import numpy as np
import shapely as sg
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pdb



# pdb.set_trace()



#create a certain number of apples at positions in X and Y where X is direction
#of travel and Y is up.

def get_apples():
	num_apples = 3600
	minx = 0
	maxx = 60
	miny = 0
	maxy = 3.5

	apple_ys = np.random.rand(num_apples) * maxy
	# apple_ys = np.random.normal(1.5, 1, num_apples)
	apple_xs = np.random.rand(num_apples) * maxx

	apple_pts  = sg.points(np.column_stack((apple_xs,apple_ys)))

	return apple_pts



def get_window(window_width, window_height, corner):
	window = sg.box(corner[0], corner[1], corner[0]+window_width, corner[1]+window_height)
	return window


#move the window forward
def move_windows(windows, x_trans):
	new_windows = []
	for w in windows:
		new_windows.append(sg.affinity.translate(w, x_trans, 0, 0))
	return new_windows

def calc_window_time(windows, apples):
	window_time = []
	for window in windows:
		num_apples = sum(window.contains(apples))
		window_time.append(num_apples)
	return window_time




window_width = 4.0
window_height = 1.0
r1_corner = [0, 0]
r2_corner = [0, 1.0]
r3_corner = [0, 2.0]

apples = get_apples()
r1_window = get_window(window_width, window_height, r1_corner)
r2_window = get_window(window_width, window_height, r2_corner)
r3_window = get_window(window_width, window_height, r3_corner)

windows = [r1_window, r2_window, r3_window]

apples_in_window = r1_window.contains(apples)



#now move the windows across the scene and count the number of
#apples in each window at each incremental step.

x_increment = 0.1#meters
num_increments = 60.0/x_increment


counts = []
for k in range(int(num_increments)):
	counts.append(calc_window_time(windows, apples))
	#move the window forward some increment
	windows = move_windows(windows, 0.1)





#make the points and polygon (window) into plotly compatible objects
apple_pts = [[sg.get_x(k), sg.get_y(k)] for k in apples]



fig = make_subplots(rows=2, cols=1)

#plot the apples
point_trace = go.Scatter(
	x = [k[0] for k in apple_pts],
	y = [k[1] for k in apple_pts],
	mode="markers",
	marker = dict(size=3, color="red"),
	name="Point",
)

fig.add_trace(point_trace, row=1, col=1)

#plot the polygons
polygons = []
colors = ['red', 'green', 'blue']
fill_colors = ['rgba(255,0,0,0.25)', 'rgba(0,255,0,0.25)', 'rgba(0,0,255,0.25)']
for w in zip(windows, colors, fill_colors):
	polygon = go.Scatter(
		x=[k[0] for k in sg.get_coordinates(w[0])],
		y=[k[1] for k in sg.get_coordinates(w[0])],
		mode="lines",
		fill="toself",
		fillcolor=w[2],
		line=dict(color=w[1]),
		name="Polygon",
	)
	# polygons.append(polygon)
	fig.add_trace(polygon, row=1, col=1)



# for poly_trace in polygons:
	# fig.add_trace(poly_trace, row=1, col=1)




xs = np.arange(0,60, 0.1)

fig.add_trace(go.Scatter(x=xs, y=[k[0] for k in counts], mode='lines', name='Apple_Count1', marker_color='lightcoral'), row=2, col=1)
fig.add_trace(go.Scatter(x=xs, y=[k[1] for k in counts], mode='lines', name='Apple_Count2', marker_color ='lightgreen'), row=2, col=1)
fig.add_trace(go.Scatter(x=xs, y=[k[2] for k in counts], mode='lines', name='Apple_Count3', marker_color='lightblue'), row=2, col=1)


#now calculate utilization at each "timestop"
u1 = [100*k[0]/max(k) for k in counts]
u2 = [100*k[1]/max(k) for k in counts]
u3 = [100*k[2]/max(k) for k in counts]
#average utilization
avg_util = np.average([u1, u2, u3])
print(avg_util)

fig.add_trace(go.Scatter(x=xs, y=u1, mode='lines', name='Util1', marker_color='red'), row=2, col=1)
fig.add_trace(go.Scatter(x=xs, y=u2, mode='lines', name='Util2', marker_color='green'), row=2, col=1)
fig.add_trace(go.Scatter(x=xs, y=u3, mode='lines', name='Util3', marker_color='blue'), row=2, col=1)



# fig = go.Figure(data=polygons)

fig.update_layout(xaxis=dict(range=[0, 65]), yaxis=dict(range=[0, 4]))
fig.update_layout(title=f'Window Width: {window_width}  Window Height: {window_height} Average Utilization: {avg_util:.1f}%')

fig.show()















# pdb.set_trace()
