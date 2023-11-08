from bokeh.plotting import figure, show
from bokeh.models import HoverTool, TapTool, WheelZoomTool, PanTool
from bokeh.palettes import Viridis6
from collections import defaultdict

def create_graph(items):
	spec = defaultdict(list)
	spec["color"] = (Viridis6 * (len(items)//len(Viridis6)+1))[:len(items)]
	
	for i in items:
		spec["timestamp"].append([[j["timestamp"]] for j in i])
		spec["price"].append([[j["price"]] for j in i])
		spec["name"].append(i[-1]["name"])
	
	hover_opts = dict(
		tooltips=[
			("Name", "@name"),
			("Date", "$snap_x{%F}"),
			("Prize", "$snap_y")
			],
		formatters={
			"$snap_x": "datetime"
		},
		show_arrow=False,
		line_policy="nearest",
	)

	line_opts = dict(
		line_width=7, line_alpha=0.6, line_color="color",
		hover_line_alpha=1.0,
		source=spec,
		legend_field="name",
	)

	tools = [
		HoverTool(**hover_opts),
		TapTool(),
		WheelZoomTool(),
		PanTool()
		]

	p = figure(x_axis_label='x', y_axis_label='y', tools=tools, x_axis_type="datetime")
	p.multi_line(xs="timestamp", ys="price", **line_opts)
	p.sizing_mode = "scale_width"
	p.legend.location = "center"

	p.add_layout(p.legend[0], 'right')
	
	return p