class Engine:
    def __init__(self, simulator, storage, notifier):
        self.simulator = simulator
        self.storage = storage
        self.notifier = notifier

    def run(self, source, destination, best_flight):
        key = f"{source.lower()}-{destination.lower()}"
        route = f"{source.title()} → {destination.title()}"

        current_price = best_flight.price
        old_price = self.storage.get_price(key)

        print(f"\n✈ Route: {route}")
        print(f"💰 Current Price: ₹{current_price}")

        # 🔥 ONLY notifier handles messaging
        self.notifier.notify(route, old_price, current_price)

        # save for next comparison
        self.storage.save_price(key, current_price)