const form = document.querySelector('#train-form');
const from = document.querySelector('#from');
const to = document.querySelector('#to');
const date = document.querySelector('#date');
const dialog = document.querySelector('#results-dialog');
const results = document.querySelector('#results');

date.min = new Date().toISOString().slice(0, 10);
date.value = new Date(Date.now() + 86400000).toISOString().slice(0, 10);

document.querySelector('#swap').addEventListener('click', () => {
  [from.value, to.value] = [to.value, from.value];
  from.focus();
});

document.querySelector('.close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const origin = from.value.trim();
  const destination = to.value.trim();
  const journeyDate = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(`${date.value}T00:00:00`));
  const trains = [
    ['12952', 'Mumbai Rajdhani', '16:55', '08:35', '6h 40m', 'AVAILABLE 42'],
    ['12260', 'Sealdah Duronto', '19:35', '12:10', '16h 35m', 'RAC 18'],
    ['12310', 'Rajendra Nagar Rajdhani', '17:10', '10:05', '16h 55m', 'AVAILABLE 12']
  ];
  results.innerHTML = `<p class="eyebrow">SEARCH RESULTS</p><h2 class="result-title">Trains for your journey</h2><p class="result-route">${origin} <b>→</b> ${destination} &nbsp;·&nbsp; ${journeyDate}</p>${trains.map(([number, name, depart, arrive, duration, seat]) => `<article class="train-result"><div><h3>${number} · ${name}</h3><p>${depart} <b>→</b> ${arrive} &nbsp; <span>(${duration})</span></p></div><div class="availability">${seat}<span>View classes & fares</span></div></article>`).join('')}`;
  dialog.showModal();
});
