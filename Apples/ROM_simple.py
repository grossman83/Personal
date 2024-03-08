import numpy as np
import shapely as sg
import plotly.graph_objects as go
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
	apple_xs = np.random.rand(num_apples) * maxx

	apple_pts  = sg.points(np.column_stack((apple_xs,apple_ys)))

	return apple_pts



def get_window(window_width, window_height, corner):
	window = sg.box(corner[0], corner[1], corner[0]+window_width, corner[1]+window_height)
	return window


#move the window forward
def move_window(window, x_trans):
	sg.affinity.translate(window, x_trans, 0, 0)
	return window

def calc_window_time(windows, apples):
	window_time = []
	for window in windows:
		num_apples = len(window.contains(apples))
		window_time.append(num_apples)
	return window_time




window_width = 1.5
window_height = 1.0
r1_corner = [0, 0.75]
r2_corner = [0, 1.75]
r3_corner = [0, 2.75]

apples = get_apples()
r1_window = get_window(window_width, window_height, r1_corner)
r2_window = get_window(window_width, window_height, r2_corner)
r3_window = get_window(window_width, window_height, r3_corner)

windows = [r1_window, r2_window, r3_window]

apples_in_window = r1_window.contains(apples)



#make the points and polygon (window) into plotly compatible objects
apple_pts = [[sg.get_x(k), sg.get_y(k)] for k in apples]



#plot the apples
point_trace = go.Scatter(
	x = [k[0] for k in apple_pts],
	y = [k[1] for k in apple_pts],
	mode="markers",
	marker = dict(size=10, color="red"),
	name="Point",
)

#plot the polygons
polygons = []
for w in windows:
	polygon = go.Scatter(
		x=[k[0] for k in sg.get_coordinates(w)],
		y=[k[1] for k in sg.get_coordinates(w)],
		mode="lines",
		fill="toself",
		fillcolor='rgba(173, 216, 230, 0.5)',
		line=dict(color="blue"),
		name="Polygon",
	)
	polygons.append(polygon)

polygons.append(point_trace)

fig = go.Figure(data= polygons)

fig.update_layout(xaxis=dict(range=[0, 60]), yaxis=dict(range=[0, 4]))

fig.show()













pdb.set_trace()
