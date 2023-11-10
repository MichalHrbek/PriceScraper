from bokeh.plotting import curdoc
from create_graph import create_graph
from app_hooks import on_server_loaded
import data

if "reload" in curdoc().session_context.request.arguments:
	on_server_loaded(None)
else:
	db = data.get()
	items = []
	
	if "ids[]" in curdoc().session_context.request.arguments:
		for i in curdoc().session_context.request.arguments["ids[]"]:
			try:
				items.append(sorted(db[i.decode()], key=lambda i: i["timestamp"]))
			except KeyError:
				print(i, "not found")

		curdoc().add_root(create_graph(items))