from src.services.price_simulator import PriceSimulator
from src.services.notifier import Notifier
from src.services.storage import (
    get_last_price,
    update_price,
    get_price_history,
)
from src.services.predictor import PricePredictor


class Flight:
    def __init__(self, airline, source, destination, price, stops=0, time="Unknown"):
        self.airline = airline
        self.source = source
        self.destination = destination
        self.price = price
        self.stops = stops
        self.time = time

    def __str__(self):
        return f"{self.airline} | {self.source}->{self.destination} | ₹{self.price} | Stops: {self.stops} | Time: {self.time}"


class FlightEngine:
    def __init__(self):
        self.simulator = PriceSimulator()
        self.notifier = Notifier()
        self.predictor = PricePredictor()

    def normalize(self, text):
        return text.strip().lower()

    def run(self, source, destination):
        # Normalize input
        source = self.normalize(source)
        destination = self.normalize(destination)

        # Route keys
        route_key = f"{source}->{destination}"
        route_display = f"{source.title()} → {destination.title()}"

        # Get flights from simulator
        flights = self.simulator.get_flights(source, destination)

        if not flights:
            print("No flights found for this route.")
            return

        # Sort flights by price
        flights.sort(key=lambda x: x.price)

        # Remove duplicate prices
        seen = set()
        unique_flights = []
        for f in flights:
            if f.price not in seen:
                seen.add(f.price)
                unique_flights.append(f)

        top_flights = unique_flights[:5]

        print("\nTop 5 Cheapest Flights:\n")
        for i, f in enumerate(top_flights, 1):
            print(f"{i}. {f}")

        # Best flight
        best = top_flights[0]

        print("\nBest Flight Selected:")
        print(best)

        print("\nTip: Showing cheapest available options based on latest data.\n")

        print(f"\n✈ Route: {route_display}")
        print(f"💰 Current Price: ₹{best.price}")

        # STORAGE + NOTIFIER
        old_price = get_last_price(route_key)
        new_price = best.price

        self.notifier.notify(route_display, old_price, new_price)
        update_price(route_key, new_price)

        # PREDICTION
        history = get_price_history(route_key)
        predicted_price, trend = self.predictor.predict(history)

        print("\n" + "=" * 40)
        print("🤖 PRICE PREDICTION")
        print("=" * 40)

        if predicted_price:
            print(f"📊 Next Expected Price: ₹{predicted_price}")
            print(f"📉 Trend: {trend}")
        else:
            print("Not enough data for prediction.")

        print("=" * 40 + "\n")


def main():
    engine = FlightEngine()

    while True:
        print("\n===== Flight Price Tracker =====")
        print("1. Track a flight")
        print("2. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            source = input("Enter source city: ")
            destination = input("Enter destination city: ")
            engine.run(source, destination)

        elif choice == "2":
            print("Thank you for using Flight Price Tracker.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()