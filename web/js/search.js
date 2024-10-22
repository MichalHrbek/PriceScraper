var items;
var stores;

async function main() {
	index = await fetch("data/index.json").then(response => response.json());
	items = index.items;
	stores = {};
	index.stores.forEach(i => {
		stores[i] = true;
	});

	index.stores.forEach(i => {
		var label = document.createElement("label");
		label.htmlFor = i;
		label.appendChild(document.createTextNode(i));
		window.storefilter.appendChild(label);
		var checkbox = document.createElement("input");
		checkbox.type = "checkbox";
		checkbox.name = i;
		checkbox.id = i;
		checkbox.checked = true;
		checkbox.onchange = (event) => {
			stores[i] = event.currentTarget.checked;
			filter();
		}
		window.storefilter.appendChild(checkbox);
	});
}

function pickItem(id) {
	if (isPicked(id)) {
		return;
	}

	const tr = window.picked.insertRow();
	tr.setAttribute("data-id", id);
	
	const rm_btn = document.createElement('button');
	rm_btn.onclick = () => {
		tr.remove();
		filter();
	}
	rm_btn.innerText = "❌"
	
	tr.insertCell().appendChild(document.createTextNode(items[id].name));
	tr.insertCell().appendChild(rm_btn)
}

function isPicked(id) {
	for (let i = 0; i < window.picked.rows.length; i++) {
		if (window.picked.rows[i].getAttribute("data-id") == id) {
			return true;
		}
	}
	return false;
}

function filter() {
	window.filtered.replaceChildren();
	if (search.value.trim() === "") return;
	for (const [id, item] of Object.entries(items)) {
		if (item.name.toLowerCase().includes(search.value.toLowerCase())) {
			if (isPicked(id)) continue;
			if(!stores[item.store]) continue;

			const tr = window.filtered.insertRow();
			tr.setAttribute("data-id", id);
			
			const add_btn = document.createElement('button');
			add_btn.onclick = () => {
				pickItem(id);
				tr.remove();
				// filter();
			}
			add_btn.innerText = "➕";

			tr.insertCell().appendChild(document.createTextNode(item.name));
			tr.insertCell().appendChild(add_btn);
		}
	}
}

function downloadItem(path) {
	getItemTimeline(path)
}

function pickAll() {
	for (let i = 0; i < window.filtered.rows.length; i++) {
		pickItem(window.filtered.rows[i].getAttribute("data-id"));
	}
	window.filtered.replaceChildren()
	// filter();
}

function removeAll() {
	window.picked.replaceChildren();
	filter();
}

function plot() {
	let params = new URLSearchParams();
	if (window.start.value) {
		params.append("start", new Date(window.start.value + 'T00:00:00').getTime());
	}
	if (window.end.value) {
		params.append("end", new Date(window.end.value + 'T00:00:00').getTime());
	}
	for (let i = 0; i < window.picked.rows.length; i++) {
		params.append("ids[]", window.picked.rows[i].getAttribute("data-id"))
	}
	window.location = '/?' + params.toString();
}
main();