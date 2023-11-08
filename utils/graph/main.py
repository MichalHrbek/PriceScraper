from bokeh.plotting import curdoc
from create_graph import create_graph
import data

print()
db = data.get()
items = []
print(curdoc().session_context.request.arguments)
for i in curdoc().session_context.request.arguments["ids[]"]:
    try:
        items.append(db[i.decode()])
    except KeyError:
        print(i, "not found")

curdoc().add_root(create_graph(items))