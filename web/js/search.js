var items;
async function main() {
	items = await fetch("data/index.json").then(response => response.json());
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
	
	tr.insertCell().appendChild(document.createTextNode(items[id]));
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
	for (const [id, name] of Object.entries(items)) {
		if (name.toLowerCase().includes(search.value.toLowerCase())) {
			if (isPicked(id)) continue;

			const tr = window.filtered.insertRow();
			tr.setAttribute("data-id", id);
			
			const add_btn = document.createElement('button');
			add_btn.onclick = () => {
				pickItem(id);
				tr.remove();
				// filter();
			}
			add_btn.innerText = "➕";

			tr.insertCell().appendChild(document.createTextNode(name));
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