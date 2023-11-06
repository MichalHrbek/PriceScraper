from tkinter import *
import json, glob, sys, datetime, random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

JITTER = 0

def item_to_str(item: list[dict]) -> str:
	return f'{item[-1]["name"]}, {item[-1]["price"]} CZK, {item[-1]["store"]}, {len(item)}' + ('' if all([i["price"] == item[0]["price"] for i in item]) else ', X')

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

		self.update(db.values())

		self.entry_box.bind("<KeyRelease>", self.check)

		self.graph_button = Button(self.root, text="Graph", command=self.make_graph)
		self.graph_button.pack(pady=5, side=LEFT, expand=TRUE)

		self.info_button = Button(self.root, text="Info", command=self.make_info)
		self.info_button.pack(pady=5, side=RIGHT, expand=TRUE)

		self.root.mainloop()

	def make_graph(self):
		GraphWindow([self.itemlist[i] for i in self.listbox.curselection()])
	
	def make_info(self):
		InfoWindow([self.itemlist[i] for i in self.listbox.curselection()])

	def update(self, data):
		self.itemlist = []
		self.listbox.delete(0, END)
		
		for item in data:
			self.itemlist.append(item)
			self.listbox.insert(END, item_to_str(item))

	def check(self, e):
		typed = self.entry_box.get()

		if typed == '':
			data = db.values()
		else:
			data = []
			for items in db.values():
				if typed.lower() in items[0]["name"].lower():
					data.append(items)
		self.update(data)

class GraphWindow:
	def __init__(self, items) -> None:
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m')) # '%d.%m.%Y'
		plt.gca().xaxis.set_major_locator(mdates.DayLocator())
		
		for i in items:
			offset = random.uniform(-JITTER, JITTER)
			plt.plot([j["timestamp"] for j in i],[j["price"]+offset for j in i], marker='o')
		
		plt.gcf().autofmt_xdate()
		plt.legend([i[-1]["name"] for i in items])
		plt.show()

class InfoWindow:
	def __init__(self, items) -> None:
		self.items = items
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

		self.itemlist = Listbox(self.root, selectmode=BROWSE, exportselection=False)
		self.itemlist.grid(row=0, column=1, sticky=NSEW)
		self.itemlist.bind("<<ListboxSelect>>", self.on_select_item)

		self.iteminfo = Listbox(self.root, selectmode=EXTENDED, exportselection=False)
		self.iteminfo.grid(row=0, column=2, sticky=NSEW)
		self.iteminfo.bind("<<ListboxSelect>>", self.on_select_info)

		self.overview.delete(0, END)
		for item in self.items:
			self.overview.insert(END, item_to_str(item))

		self.root.mainloop()


	def on_select_overview(self, event):
		self.clipboard = self.overview.get(self.overview.curselection()[0])
		self.itemlist.delete(0, END)
		for item in self.items[self.overview.curselection()[0]]:
			self.itemlist.insert(END, item["timestamp"])
	
	def on_select_item(self, event):
		self.clipboard = self.itemlist.get(self.itemlist.curselection()[0])
		self.iteminfo.delete(0, END)
		item = self.items[self.overview.curselection()[0]][self.itemlist.curselection()[0]]
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
		

if __name__== "__main__":
	filepaths = []
	for i in sys.argv[1:]:
		for j in glob.glob(i):
			filepaths.append(j)
	
	# print(filepaths)

	db: dict[str,list[dict]] = {}
	for i in filepaths:
		for j in json.loads(open(i).read()):
			j["timestamp"] = datetime.datetime.fromtimestamp(j["timestamp"])
			if j["id"] in db:
				db[j["id"]].append(j)
			else:
				db[j["id"]] = [j]

	sw = SelectWindow()