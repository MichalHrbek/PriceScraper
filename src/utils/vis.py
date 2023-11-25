from tkinter import *
from graph.create_graph import create_graph
from bokeh.plotting import show
from graph.data import *
import datetime

start()
all_items = getAllItems()

def item_to_str(item) -> str:
	return f'{item["Name"]}, {item["Price"]} CZK, {item["Shop"]}'

class SelectWindow:
	def __init__(self) -> None:
		self.root = Tk()
		self.root.title('PriceVis')
		self.root.geometry("1280x720")
		self.itemlist = []

		self.entry_box = Entry(self.root, font=("Helvetica", 20))
		self.entry_box.pack(pady=5)

		self.listbox = Listbox(self.root, selectmode=EXTENDED)
		self.listbox.pack(pady=10, fill=BOTH, expand=YES)

		self.update(all_items)

		self.entry_box.bind("<KeyRelease>", self.check)

		self.graph_button = Button(self.root, text="Graph", command=self.make_graph)
		self.graph_button.pack(pady=5, side=LEFT, expand=TRUE)

		self.info_button = Button(self.root, text="Info", command=self.make_info)
		self.info_button.pack(pady=5, side=RIGHT, expand=TRUE)

		self.root.mainloop()

	def make_graph(self):
		GraphWindow([self.itemlist[i]["Id"] for i in self.listbox.curselection()])
	
	def make_info(self):
		InfoWindow([self.itemlist[i]["Id"] for i in self.listbox.curselection()])

	def update(self, data):
		self.itemlist = []
		self.listbox.delete(0, END)
		
		for item in data:
			self.itemlist.append(item)
			self.listbox.insert(END, item_to_str(item))

	def check(self, e):
		typed = self.entry_box.get()

		if typed == '':
			data = all_items
		else:
			data = []
			for items in all_items:
				if typed.lower() in items["Name"].lower():
					data.append(items)
		self.update(data)

class GraphWindow:
	def __init__(self, ids) -> None:
		items = [getItemList(i) for i in ids]
		p = create_graph(items)
		
		show(p)

class InfoWindow:
	def __init__(self, ids) -> None:
		self.items = [getItemList(i) for i in ids]
		for i in self.items:
			for j in i:
				j["RecordTimeStamp"] = datetime.datetime.fromtimestamp(j["RecordTimeStamp"])
		self.clipboard = ""

		self.root = Tk()
		self.root.title('PriceInfo')
		self.root.geometry("1280x720")
		self.root.bind("<Control-c>", lambda event: self.copy_to_clipboard())

		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_columnconfigure(1, weight=1)
		self.root.grid_columnconfigure(2, weight=1)

		self.overview = Listbox(self.root, selectmode=BROWSE, exportselection=False)
		self.overview.grid(row=0, column=0, sticky=NSEW)
		self.overview.bind("<<ListboxSelect>>", self.on_select_overview)

		self.item_box = Listbox(self.root, selectmode=BROWSE, exportselection=False)
		self.item_box.grid(row=0, column=1, sticky=NSEW)
		self.item_box.bind("<<ListboxSelect>>", self.on_select_item)

		self.iteminfo = Listbox(self.root, selectmode=EXTENDED, exportselection=False)
		self.iteminfo.grid(row=0, column=2, sticky=NSEW)
		self.iteminfo.bind("<<ListboxSelect>>", self.on_select_info)

		self.overview.delete(0, END)
		for i in self.items:
			self.overview.insert(END, item_to_str(i[0]))

		self.root.mainloop()

	def on_select_overview(self, event):
		self.clipboard = self.overview.get(self.overview.curselection()[0])
		self.item_box.delete(0, END)
		for item in self.items[self.overview.curselection()[0]]:
			self.item_box.insert(END, item["RecordTimeStamp"])
	
	def on_select_item(self, event):
		self.clipboard = self.item_box.get(self.item_box.curselection()[0])
		self.iteminfo.delete(0, END)
		item = self.items[self.overview.curselection()[0]][self.item_box.curselection()[0]]
		for i in item:
			self.iteminfo.insert(END, f'{i}: {item[i]}')
	
	def on_select_info(self, event):
		self.clipboard = ""
		for i in self.iteminfo.curselection():
			self.clipboard += self.iteminfo.get(i) + "\n"

	def copy_to_clipboard(self):
		self.root.clipboard_clear()
		self.root.clipboard_append(self.clipboard)
		self.root.update()

sw = SelectWindow()