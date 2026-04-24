class Engine:
    def __init__(self, simulator, storage, notifier):
        self.simulator = simulator
        self.storage = storage
        self.notifier = notifier

    def run(self, source, destination, best_flight):
        key = f"{source.lower()}-{destination.lower()}"

        current_price = best_flight.price
        old_price = self.storage.get_price(key)

        print(f"\n✈ Route: {source.title()} → {destination.title()}")
        print(f"💰 Current Price: ₹{current_price}")

        if old_price:
            if current_price < old_price:
                self.notifier.notify("Price dropped", current_price, old_price)
            else:
                print(f"Previous Price: ₹{old_price}")
        else:
            print("No previous data found.")

        self.storage.save_price(key, current_price)