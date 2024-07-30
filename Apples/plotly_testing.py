import plotly.graph_objs as go
import plotly.io as pio

# Sample data
x = [1, 2, 3, 4, 5]
y = [10, 11, 12, 13, 14]

# Create scatter plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='markers',
    marker=dict(size=10, color='blue'),
    name='Points'
))

# Add invisible lines to be revealed on click
line_indices = {}  # To store which lines correspond to each point
for i in range(len(x)):
    line_indices[i] = []
    if i > 0:  # Line from the previous point to the current point
        line_idx = len(fig.data)
        line_indices[i].append(line_idx)
        fig.add_trace(go.Scatter(
            x=[x[i-1], x[i]],
            y=[y[i-1], y[i]],
            mode='lines',
            line=dict(color='red', width=2),
            showlegend=False,
            hoverinfo='none',  # Make lines non-hoverable
            visible=False  # Make lines invisible initially
        ))
    if i < len(x) - 1:  # Line from the current point to the next point
        line_idx = len(fig.data)
        line_indices[i].append(line_idx)
        fig.add_trace(go.Scatter(
            x=[x[i], x[i+1]],
            y=[y[i], y[i+1]],
            mode='lines',
            line=dict(color='red', width=2),
            showlegend=False,
            hoverinfo='none',  # Make lines non-hoverable
            visible=False  # Make lines invisible initially
        ))

# Configure layout
fig.update_layout(
    title='Click to Reveal Lines',
    hovermode='closest'
)

# Add click events using Plotly.js
fig.show(config={'displayModeBar': False})

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
pio.write_html(fig, file='click_reveal_lines.html', auto_open=True, include_plotlyjs='cdn', config={'displayModeBar': False}, post_script=js_code)








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












