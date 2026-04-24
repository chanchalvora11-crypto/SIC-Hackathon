import pandas as pd
import random
from difflib import get_close_matches
from src.models.flight import Flight


class PriceSimulator:
    def __init__(self, file_path="data/flights_processed.csv"):
        self.df = pd.read_csv(file_path)

        self.df["Source"] = self.df["Source"].str.strip().str.lower()
        self.df["Destination"] = self.df["Destination"].str.strip().str.lower()

        self.sources = sorted(self.df["Source"].unique())
        self.destinations = sorted(self.df["Destination"].unique())

    def normalize_input(self, city, valid_list):
        city = city.strip().lower()

        if city in valid_list:
            return city

        match = get_close_matches(city, valid_list, n=1, cutoff=0.6)
        return match[0] if match else None

    def get_flights(self, source, destination):
        source = self.normalize_input(source, self.sources)
        destination = self.normalize_input(destination, self.destinations)

        if not source or not destination:
            return []

        filtered = self.df[
            (self.df["Source"] == source) &
            (self.df["Destination"] == destination)
        ]

        if filtered.empty:
            return []

        flights = []

        for _, row in filtered.iterrows():
            price = int(row["Price"]) + random.randint(-300, 300)

            flight = Flight(
                source=row["Source"],
                destination=row["Destination"],
                price=max(1000, price),
                stops=row.get("Total_Stops", 0),
                time=row.get("Dep_Time", "Unknown"),
                airline=row.get("Airline", "Unknown")
            )

            flights.append(flight)

        flights = sorted(flights, key=lambda x: x.price)

        # remove duplicate prices
        seen = set()
        unique_flights = []

        for f in flights:
            if f.price not in seen:
                seen.add(f.price)
                unique_flights.append(f)

        return unique_flights[:5]

    def get_price(self, source, destination):
        flights = self.get_flights(source, destination)

        if not flights:
            return None

        return min(f.price for f in flights)