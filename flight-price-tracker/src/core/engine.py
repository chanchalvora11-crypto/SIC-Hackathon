from src.core.tracker import FlightTracker


class Engine:
    def __init__(self, simulator, storage, notifier, filters=None):
        self.tracker = FlightTracker(simulator, storage, notifier)
        self.simulator = simulator
        self.filters = filters if filters else []

    def apply_filters(self, flights):
        for f in self.filters:
            flights = f.apply(flights)
        return flights

    def run(self, source, destination):
        flights = self.simulator.get_flights(source, destination)

        if self.filters:
            flights = self.apply_filters(flights)

        if not flights:
            print("No flights found after applying filters.")
            return

        best_flight = min(flights, key=lambda x: x.price)

        print("\nBest Flight Selected:")
        print(best_flight)   # this now works correctly

        self.tracker.track(source, destination)