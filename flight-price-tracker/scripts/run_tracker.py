from src.core.engine import Engine
from src.services.price_simulator import PriceSimulator


# ===== Storage =====
class Storage:
    def __init__(self):
        self.data = {}

    def get_price(self, key):
        return self.data.get(key)

    def save_price(self, key, price):
        self.data[key] = price


# ===== Notifier =====
class Notifier:
    def notify(self, message, new, old):
        print(f"{message}: ₹{old} → ₹{new}")


simulator = PriceSimulator()
storage = Storage()
notifier = Notifier()
engine = Engine(simulator, storage, notifier)


def menu():
    while True:
        print("\n===== Flight Price Tracker =====")
        print("1. Track a flight")
        print("2. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            source = input("Enter source city: ")
            destination = input("Enter destination city: ")

            flights = simulator.get_flights(source, destination)

            if not flights:
                print("\nNo flights found.")
                print("\nAvailable cities:")
                print("Sources:", simulator.sources)
                print("Destinations:", simulator.destinations)
                continue

            print("\nTop 5 Cheapest Flights:\n")

            for i, f in enumerate(flights, 1):
                print(f"{i}. {f}")

            best = flights[0]

            print("\nBest Flight Selected:")
            print(best)

            print("\nTip: Showing cheapest available options based on latest data.\n")

            engine.run(source, destination, best)

        elif choice == "2":
            print("Thank you for using Flight Price Tracker.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()