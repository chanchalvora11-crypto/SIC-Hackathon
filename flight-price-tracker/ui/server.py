import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

from src.services.predictor import PricePredictor
from src.services.price_simulator import PriceSimulator
from src.services.storage import get_last_price, get_price_history, update_price


class FlightUiServer(SimpleHTTPRequestHandler):
    simulator = PriceSimulator()
    predictor = PricePredictor()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT / "ui"), **kwargs)

    def do_GET(self):
        if self.path == "/api/cities":
            self.send_json(
                {
                    "sources": [city.title() for city in self.simulator.sources],
                    "destinations": [
                        city.title() for city in self.simulator.destinations
                    ],
                }
            )
            return

        if self.path == "/api/history":
            self.send_json(self.read_all_history())
            return

        super().do_GET()

    def do_POST(self):
        if self.path != "/api/track":
            self.send_error(404, "Not found")
            return

        payload = self.read_json()
        source = payload.get("source", "").strip()
        destination = payload.get("destination", "").strip()

        if not source or not destination:
            self.send_json({"error": "Source and destination are required."}, 400)
            return

        flights = self.simulator.get_flights(source, destination)
        if not flights:
            self.send_json({"error": "No flights found for this route."}, 404)
            return

        flights.sort(key=lambda flight: flight.price)
        top_flights = self.unique_by_price(flights)[:5]
        best = top_flights[0]

        normalized_source = best.source.strip().lower()
        normalized_destination = best.destination.strip().lower()
        route_key = f"{normalized_source}->{normalized_destination}"
        route_display = (
            f"{normalized_source.title()} to {normalized_destination.title()}"
        )

        old_price = get_last_price(route_key)
        new_price = best.price
        update_price(route_key, new_price)

        history = get_price_history(route_key)
        predicted_price, trend = self.predictor.predict(history)

        self.send_json(
            {
                "route": route_display,
                "oldPrice": old_price,
                "newPrice": new_price,
                "change": self.price_change(old_price, new_price),
                "flights": [self.serialize_flight(flight) for flight in top_flights],
                "prediction": {
                    "price": predicted_price,
                    "trend": trend,
                },
                "history": history[-8:],
            }
        )

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}

        body = self.rfile.read(length).decode("utf-8")
        return json.loads(body or "{}")

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_all_history(self):
        data_path = PROJECT_ROOT / "data" / "data.json"
        if not data_path.exists():
            return {}

        try:
            return json.loads(data_path.read_text())
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def unique_by_price(flights):
        seen = set()
        unique = []

        for flight in flights:
            if flight.price in seen:
                continue

            seen.add(flight.price)
            unique.append(flight)

        return unique

    @staticmethod
    def serialize_flight(flight):
        return {
            "airline": flight.airline,
            "source": flight.source.title(),
            "destination": flight.destination.title(),
            "price": flight.price,
            "stops": flight.stops,
            "time": flight.time,
        }

    @staticmethod
    def price_change(old_price, new_price):
        if old_price is None:
            return {
                "type": "new",
                "label": "New tracking started",
                "amount": 0,
            }

        if new_price < old_price:
            return {
                "type": "drop",
                "label": "Price dropped",
                "amount": old_price - new_price,
            }

        if new_price > old_price:
            return {
                "type": "increase",
                "label": "Price increased",
                "amount": new_price - old_price,
            }

        return {
            "type": "same",
            "label": "No price change",
            "amount": 0,
        }


def main():
    port = int(os.environ.get("PORT", 8000))
    server = ThreadingHTTPServer(("127.0.0.1", port), FlightUiServer)
    print(f"Flight Price Tracker UI running at http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
