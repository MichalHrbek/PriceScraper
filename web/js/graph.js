import { getItemTimeline, roundToHour, filterDate } from "./modules/datamanager.js"

const CURRENCY = "CZK";
const ctx = document.getElementById('chart');
// ?ids[]=tesco%2F2001019141652.csv&ids[]=tesco%2F2001130909583.csv&ids[]=tesco%2F2001000151875.csv&ids[]=tesco%2F2001130898559.csv&ids[]=tesco%2F2001130294293.csv&ids[]=tesco%2F2001130907487.csv&ids[]=tesco%2F2001130294254.csv&ids[]=tesco%2F2001130905057.csv&ids[]=tesco%2F2001130905063.csv&ids[]=tesco%2F2001130905073.csv&ids[]=albert%2F20480905.csv&ids[]=albert%2F22459466.csv&ids[]=albert%2F27344064.csv&ids[]=albert%2F26109718.csv&ids[]=albert%2F21976056.csv&ids[]=billa%2F82322229.csv&ids[]=billa%2F82316363.csv&ids[]=billa%2F82315094.csv
const params = new URLSearchParams(window.location.search);
var startTime = Number.MIN_SAFE_INTEGER;
var endTime = Number.MAX_SAFE_INTEGER;

if (params.get("start")) startTime = parseInt(params.get("start"));
if (params.get("end")) endTime = parseInt(params.get("end"));

async function getDataset(path) {
	let i = await getItemTimeline(path,roundToHour);
	
	let label;
	if(i.length > 0) label = `${i[0].store} – ${i[i.length-1].name}`;
	else label = "No data: " + path;
	
	filterDate(i,startTime,endTime);
	
	return {
		label: label,
		data: i,
	};
}

async function main() {
	var d = await Promise.all(params.getAll("ids[]").map((path) => {
		return getDataset(path);
	}));

	const priceChart = new Chart(ctx, {
		type: 'line',
		data: {
			datasets: d,
		},
		options: {
			// Performance
			animation: false,
			parsing: false,

			responsive: true,
			maintainAspectRatio: false,
			plugins: {
				tooltip: {
					enabled: true,
					// position: 'nearest',
					external: externalTooltipHandler,
					callbacks: {
						label: function(context) {
							let i = context.element.$context.raw;
							return [`${i.store} – ${i.name}`,`${i.price} ${CURRENCY}`];
						}
					}
				}
			},
			parsing: {
				xAxisKey: 'timestamp',
				yAxisKey: 'price',
			},
			scales: {
				x: {
					type: 'time',
					time: {
						unit: "day",
					},
				},
				y: {
					beginAtZero: true,
				}
			}
		}
	});


}

main();

const externalTooltipHandler = (context) => {
	const infoEl = window.hoverinfo;
	infoEl.replaceChildren();

	context.tooltip.dataPoints.forEach(i => {
		const tbl = document.createElement('table');
		tbl.classList.add("infotable")
		for (let key in i.raw) {
			const tr = tbl.insertRow();
			tr.insertCell().appendChild(document.createTextNode(key));
			tr.insertCell().appendChild(document.createTextNode(i.raw[key]));
		}
		infoEl.appendChild(tbl)
	})
};