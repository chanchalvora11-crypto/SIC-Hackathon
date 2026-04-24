from src.core.engine import Engine


# ===== Dummy Simulator =====
class DummySimulator:
    def get_price(self, source, destination):
        import random
        return random.randint(4000, 8000)

    def get_flights(self, source, destination):
        class Flight:
            def __init__(self, price):
                self.price = price

            def __str__(self):
                return f"✈ Flight | Price: ₹{self.price}"

        return [Flight(6000), Flight(5000), Flight(7000)]


# ===== Dummy Storage =====
class DummyStorage:
    def __init__(self):
        self.data = {}

    def get_price(self, key):
        return self.data.get(key)

    def save_price(self, key, price):
        self.data[key] = price


# ===== Dummy Notifier =====
class DummyNotifier:
    def notify(self, message, new, old):
        print(f"{message}: ₹{old} → ₹{new}")


# Initialize system
simulator = DummySimulator()
storage = DummyStorage()
notifier = DummyNotifier()
engine = Engine(simulator, storage, notifier)


# ===== MENU =====
def menu():
    while True:
        print("\n===== Flight Price Tracker =====")
        print("1. Track a flight")
        print("2. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            source = input("Enter source city: ").strip()
            destination = input("Enter destination city: ").strip()

            if not source.isalpha() or not destination.isalpha():
                print("Invalid input. Please enter valid city names.")
                continue

            engine.run(source, destination)

        elif choice == "2":
            print("Thank you for using Flight Price Tracker.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()