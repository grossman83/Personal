
import plotly.graph_objs as go
import numpy as np

# Generate two datasets
x1 = np.linspace(0, 10, 100)
y1 = np.sin(x1)

x2 = np.linspace(0, 10, 100)
y2 = np.cos(x2)

# Create the initial plot with the first dataset
fig = go.Figure()

# First dataset (sine wave)
fig.add_trace(go.Scatter(
    x=x1,
    y=y1,
    mode='lines',
    name='Sine Wave',
    line=dict(color='blue')
))

# Second dataset (cosine wave) - Initially hidden
fig.add_trace(go.Scatter(
    x=x2,
    y=y2,
    mode='lines',
    name='Cosine Wave',
    line=dict(color='red'),
    visible=False  # This trace is initially hidden
))

# Define the layout with buttons to switch datasets
fig.update_layout(
    title='Select Dataset to Display',
    xaxis=dict(title='X-axis'),
    yaxis=dict(title='Y-axis'),
    updatemenus=[
        {
            'buttons': [
                {
                    'args': [{'visible': [True, False]}, {'title': 'Sine Wave'}],
                    'label': 'Sine Wave',
                    'method': 'update'
                },
                {
                    'args': [{'visible': [False, True]}, {'title': 'Cosine Wave'}],
                    'label': 'Cosine Wave',
                    'method': 'update'
                }
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'y': 1.15,
            'pad': {'r': 10, 't': 10},
            'xanchor': 'left',
            'yanchor': 'top'
        }
    ]
)

# Show the plot
fig.show()








############################################################################## 



# import plotly.graph_objs as go
# import plotly.io as pio

# # Sample data
# x = [1, 2, 3, 4, 5]
# y = [10, 11, 12, 13, 14]

# # Create scatter plot
# fig = go.Figure()

# fig.add_trace(go.Scatter(
#     x=x,
#     y=y,
#     mode='markers',
#     marker=dict(size=10, color='blue'),
#     name='Points'
# ))

# # Add invisible lines to be revealed on click
# line_indices = {}  # To store which lines correspond to each point
# for i in range(len(x)):
#     line_indices[i] = []
#     if i > 0:  # Line from the previous point to the current point
#         line_idx = len(fig.data)
#         line_indices[i].append(line_idx)
#         fig.add_trace(go.Scatter(
#             x=[x[i-1], x[i]],
#             y=[y[i-1], y[i]],
#             mode='lines',
#             line=dict(color='red', width=2),
#             showlegend=False,
#             hoverinfo='none',  # Make lines non-hoverable
#             visible=False  # Make lines invisible initially
#         ))
#     if i < len(x) - 1:  # Line from the current point to the next point
#         line_idx = len(fig.data)
#         line_indices[i].append(line_idx)
#         fig.add_trace(go.Scatter(
#             x=[x[i], x[i+1]],
#             y=[y[i], y[i+1]],
#             mode='lines',
#             line=dict(color='red', width=2),
#             showlegend=False,
#             hoverinfo='none',  # Make lines non-hoverable
#             visible=False  # Make lines invisible initially
#         ))

# # Configure layout
# fig.update_layout(
#     title='Click to Reveal Lines',
#     hovermode='closest'
# )

# # Add click events using Plotly.js
# fig.show(config={'displayModeBar': False})

# # JavaScript code to add click events (to be used with Plotly's HTML export)
# js_code = """
# document.querySelectorAll('.plotly-graph-div').forEach(function (div) {
#     div.on('plotly_click', function (data) {
#         var pointIndex = data.points[0].pointIndex;
#         var lines = %s[pointIndex];
#         var visibility = div.data[lines[0]].visible === true ? false : true;
#         var update = {'visible': visibility};
#         for (var i = 0; i < lines.length; i++) {
#             Plotly.restyle(div, update, [lines[i]]);
#         }
#     });
# });
# """ % (line_indices,)

# # Export to HTML with embedded JavaScript
# pio.write_html(fig, file='click_reveal_lines.html', auto_open=True, include_plotlyjs='cdn', config={'displayModeBar': False}, post_script=js_code)


##############################################################################





# import plotly.graph_objs as go
# import plotly.io as pio

# # Sample data
# x = [1, 2, 3, 4, 5]
# y = [10, 11, 12, 13, 14]

# # Create scatter plot
# fig = go.Figure()

# fig.add_trace(go.Scatter(
#     x=x,
#     y=y,
#     mode='markers',
#     marker=dict(size=10, color='blue'),
#     name='Points'
# ))

# # Add invisible lines to be revealed on hover
# for i in range(len(x)):
#     for j in range(i+1, len(x)):
#         fig.add_trace(go.Scatter(
#             x=[x[i], x[j]],
#             y=[y[i], y[j]],
#             mode='lines',
#             line=dict(color='red', width=2),
#             showlegend=False,
#             hoverinfo='none',  # Make lines non-hoverable
#             visible='legendonly'  # Make lines invisible initially
#         ))

# # Configure layout
# fig.update_layout(
#     title='Hover to Reveal Lines',
#     hovermode='closest'
# )

# # Add hover events using Plotly.js
# fig.show(config={'displayModeBar': False})

# # JavaScript code to add hover events (to be used with Plotly's HTML export)
# js_code = """
# document.querySelectorAll('.plotly-graph-div').forEach(function (div) {
#     div.on('plotly_hover', function (data) {
#         var update = {'visible': true};
#         Plotly.restyle(div, update, data.points[0].curveNumber + 1);
#     });

#     div.on('plotly_unhover', function (data) {
#         var update = {'visible': 'legendonly'};
#         Plotly.restyle(div, update, data.points[0].curveNumber + 1);
#     });
# });
# """

# # Export to HTML with embedded JavaScript
# pio.write_html(fig, file='hover_reveal_lines.html', auto_open=True, include_plotlyjs='cdn', config={'displayModeBar': False}, post_script=js_code)












