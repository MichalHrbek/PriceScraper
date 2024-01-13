from bokeh.plotting import curdoc
from create_graph import create_graph
from app_hooks import on_server_loaded
from DataManager import get_timeline

if "reload" in curdoc().session_context.request.arguments:
	on_server_loaded(None)
else:	
	if "ids[]" in curdoc().session_context.request.arguments:
		items = []

		for i in curdoc().session_context.request.arguments["ids[]"]:
			try:
				store,id = i.decode().split(";",1)
				id = int(id)
				items.append(sorted(get_timeline(store, id), key=lambda i: i["timestamp"]))
			except KeyError:
				print(i, "Not found")
			except ValueError:
				print(i, "Invalid")

		curdoc().add_root(create_graph(items))