export function defaultTransform(value, field) {
	if (field === 'timestamp') return value * 1000;
	return value;
}

export function genRoundTransform(seconds) {
	return (value, field) => {
		if (field === 'timestamp') return (value-value%seconds)*1000;
		return value;
	}
}

export const roundToHour = genRoundTransform(3600)
export const roundToMinute = genRoundTransform(60)

export async function getItemTimeline(path, _transform=defaultTransform) {
	// This doesn't seem safe
	const csvData = await fetch("data/" + path).then(response => response.text());

	var parsed = Papa.parse(csvData, {
		header: true,
		skipEmptyLines: true,
		dynamicTyping: {"timestamp": true, "price": true, "unit_price": true},
		transform: _transform,
	});
	
	let o = Object.assign({}, parsed.data[0]);

	for (let i = 0; i < parsed.data.length; i++) {
		parsed.meta.fields.forEach(j => {
			if (!parsed.data[i][j]) parsed.data[i][j] = o[j];
			else o[j] = parsed.data[i][j];
		});
	}

	return parsed.data;
}

export async function getItemUnparsed(path, keys=undefined) {
	const timeline = await getItemTimeline(path,undefined);
	return Papa.unparse(timeline, {
		header: true,
		columns: keys,
	});
}

// Filters the timeline in place
export function filterDate(timeline, startTime=Number.MIN_SAFE_INTEGER, endTime=Number.MAX_SAFE_INTEGER) {
	let start = timeline.length;
	for (let i = 0; i < timeline.length; i++) {
		if (timeline[i].timestamp >= startTime && timeline[i].timestamp <= endTime) {
			start = i;
			break;
		}
	}
	timeline.splice(0,start);
	
	let end = timeline.length;
	for (let i = 0; i < timeline.length; i++) {
		if (timeline[i].timestamp > endTime) {
			end = i;
			break;
		}
	}
	timeline.splice(end,timeline.length-end);
}

export async function getIndex(_transform=defaultTransform) {
	const csvData = await fetch("data/index.csv").then(response => response.text());
	
	var parsed = Papa.parse(csvData, {
		header: true,
		skipEmptyLines: true,
		dynamicTyping: {"timestamp": true, "price": true, "unit_price": true},
		transform: _transform,
	});

	let o = {};

	o.items = parsed.data.reduce((acc, i) => {
		acc[`${i.store}/${i.id}.csv`] = i;
		return acc;
	}, {});

	o.stores = new Set(parsed.data.map(item => item.store))
	
	return o;
}