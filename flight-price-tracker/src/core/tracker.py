class FlightTracker:
    def __init__(self, simulator, storage, notifier):
        self.simulator = simulator
        self.storage = storage
        self.notifier = notifier

    def track(self, source, destination):
        route_key = f"{source}-{destination}"

        old_price = self.storage.get_price(route_key)
        new_price = self.simulator.get_price(source, destination)

        print(f"\n✈ Route: {source} → {destination}")
        print(f"💰 Current Price: ₹{new_price}")

        if old_price is not None:
            print(f"📊 Previous Price: ₹{old_price}")

            if new_price < old_price:
                self.notifier.notify("📉 PRICE DROPPED", new_price, old_price)
            elif new_price > old_price:
                self.notifier.notify("📈 PRICE INCREASED", new_price, old_price)
            else:
                self.notifier.notify("⚖ NO CHANGE", new_price, old_price)
        else:
            print("No previous data found.")

        self.storage.save_price(route_key, new_price)