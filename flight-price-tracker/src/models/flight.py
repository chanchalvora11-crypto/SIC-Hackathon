class Flight:
    def __init__(self, source, destination, price, stops, time, airline):
        self.source = source
        self.destination = destination
        self.price = price
        self.stops = stops
        self.time = time
        self.airline = airline

    def __str__(self):
        return f"{self.airline} | {self.source.title()}->{self.destination.title()} | ₹{self.price} | Stops: {self.stops} | Time: {self.time}"