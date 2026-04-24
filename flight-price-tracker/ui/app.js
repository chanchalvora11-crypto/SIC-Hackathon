const form = document.querySelector("#tracker-form");
const sourceInput = document.querySelector("#source");
const destinationInput = document.querySelector("#destination");
const routeTitle = document.querySelector("#route-title");
const statusPill = document.querySelector("#status-pill");
const currentPrice = document.querySelector("#current-price");
const priceNote = document.querySelector("#price-note");
const flightList = document.querySelector("#flight-list");
const flightCount = document.querySelector("#flight-count");
const predictionPrice = document.querySelector("#prediction-price");
const predictionTrend = document.querySelector("#prediction-trend");
const historyCount = document.querySelector("#history-count");
const historyBars = document.querySelector("#history-bars");
const routeCount = document.querySelector("#route-count");
const checkCount = document.querySelector("#check-count");

function formatPrice(value) {
  if (value === null || value === undefined) {
    return "Rs. --";
  }

  return `Rs. ${Number(value).toLocaleString("en-IN")}`;
}

function setOptions(listId, values) {
  const list = document.querySelector(listId);
  list.innerHTML = values.map((value) => `<option value="${value}"></option>`).join("");
}

async function loadCities() {
  const response = await fetch("/api/cities");
  const data = await response.json();

  setOptions("#source-list", data.sources);
  setOptions("#destination-list", data.destinations);
}

async function loadHistorySummary() {
  const response = await fetch("/api/history");
  const data = await response.json();
  const routes = Object.values(data);
  const checks = routes.reduce((total, route) => total + (route.history || []).length, 0);

  routeCount.textContent = routes.length;
  checkCount.textContent = checks;
}

function renderFlights(flights) {
  flightCount.textContent = `${flights.length} found`;
  flightList.classList.remove("empty-state");

  flightList.innerHTML = flights
    .map(
      (flight, index) => `
        <article class="flight-row">
          <div class="flight-main">
            <strong>${index + 1}. ${flight.airline}</strong>
            <span>${flight.source} to ${flight.destination}</span>
            <span class="flight-meta">${flight.stops} stops | ${flight.time}</span>
          </div>
          <div class="flight-price">${formatPrice(flight.price)}</div>
        </article>
      `,
    )
    .join("");
}

function renderHistory(history) {
  historyCount.textContent = `${history.length} points`;
  historyBars.innerHTML = "";

  if (!history.length) {
    return;
  }

  const min = Math.min(...history);
  const max = Math.max(...history);
  const spread = Math.max(max - min, 1);

  history.forEach((price) => {
    const bar = document.createElement("div");
    const height = 28 + ((price - min) / spread) * 72;
    bar.className = "history-bar";
    bar.style.height = `${height}px`;
    bar.title = formatPrice(price);
    historyBars.appendChild(bar);
  });
}

function renderResult(data) {
  routeTitle.textContent = data.route;
  currentPrice.textContent = formatPrice(data.newPrice);

  statusPill.className = `status-pill ${data.change.type}`;
  statusPill.textContent = data.change.label;

  if (data.oldPrice === null) {
    priceNote.textContent = "First saved price for this route.";
  } else if (data.change.amount > 0) {
    priceNote.textContent = `${data.change.label} by ${formatPrice(data.change.amount)} from ${formatPrice(data.oldPrice)}.`;
  } else {
    priceNote.textContent = `Previous price was ${formatPrice(data.oldPrice)}.`;
  }

  renderFlights(data.flights);
  predictionPrice.textContent = formatPrice(data.prediction.price);
  predictionTrend.textContent = data.prediction.trend || "Waiting for enough history.";
  renderHistory(data.history || []);
}

function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  window.setTimeout(() => toast.remove(), 3200);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = form.querySelector("button");
  submitButton.disabled = true;
  submitButton.textContent = "Tracking...";

  try {
    const response = await fetch("/api/track", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source: sourceInput.value,
        destination: destinationInput.value,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      showToast(data.error || "Unable to track this route.");
      return;
    }

    renderResult(data);
    await loadHistorySummary();
  } catch (error) {
    showToast("Could not reach the tracker server.");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Track flight";
  }
});

loadCities().catch(() => showToast("City suggestions are unavailable."));
loadHistorySummary().catch(() => {});
