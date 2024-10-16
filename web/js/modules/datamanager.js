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

export async function getItemTimeline(path, _transform=defaultTransform, startTime=Number.MIN_SAFE_INTEGER, endTime=Number.MAX_SAFE_INTEGER) {
	// This doesn't seem safe
	let csvData = await fetch("data/" + path).then(response => response.text());

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

	let start = 0;
	for (let i = 0; i < parsed.data.length; i++) {
		if (parsed.data[i].timestamp >= startTime) {
			start = i;
			break;
		}
	}
	// FIX: If whole array is befora start date
	parsed.data.splice(0,start);
	
	let end = parsed.data.length;
	for (let i = 0; i < parsed.data.length; i++) {
		if (parsed.data[i].timestamp > endTime) {
			end = i;
			break;
		}
	}
	parsed.data.splice(end,parsed.data.length-end);

	return parsed.data;
}