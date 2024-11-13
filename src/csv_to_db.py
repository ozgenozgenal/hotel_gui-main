import csv
from database import Database

class CSVToDB:
    def __init__(self, db_file):
        self.database = Database(db_file)
        self.sql_create_hotels_table = """
        CREATE TABLE IF NOT EXISTS hotels (
            id integer PRIMARY KEY,
            city text NOT NULL,
            name text NOT NULL,
            cleanliness real,
            room real,
            service real,
            location real,
            value real,
            safety real,
            comfort real,
            transportation real,
            noise real
        );
        """

    def process_hotel_name(self, hotel_name):
        parts = hotel_name.split('_')[2:]  # Skip the first two parts
        capitalized_parts = [part.capitalize() for part in parts]
        return ' '.join(capitalized_parts)

    def create_table(self):
        with self.database.conn:
            self.database.conn.execute("DROP TABLE IF EXISTS hotels")
            self.database.create_table(self.sql_create_hotels_table)

    def load_data(self, city):
        with open(f'csv/{city}.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip the header
            for row in reader:
                hotel_name = self.process_hotel_name(row[0])
                hotel = (
                    city,
                    hotel_name,
                    float(row[2]),  # cleanliness_score
                    float(row[3]),  # room_score
                    float(row[4]),  # service_score
                    float(row[5]),  # location_score
                    float(row[6]),  # value_score
                    float(row[7]),  # safety_score
                    float(row[8]),  # comfort_score
                    float(row[9]),  # transportation_score
                    float(row[10])  # noise_score
                )
                self.database.insert_hotel(hotel)

    def main(self):
        self.create_table()
        cities = ["Beijing", "Dubai", "Chicago", "Las Vegas", "London", "Montreal", "New Delhi", "San Francisco",
                  "Shanghai"]
        for city in cities:
            self.load_data(city)
        self.database.close_connection()


if __name__ == '__main__':
    csv_to_db = CSVToDB("hotels.db")
    csv_to_db.main()
