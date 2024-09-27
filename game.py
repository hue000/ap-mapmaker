from geopy.distance import great_circle
import random
import datetime
import game_info    

class Game:
    def __init__(self):
        self.airlines = {}    
        self.airports = []
        self.cities = []
        self.passengers = {}
        self.date = datetime.date.today()
        self.country_current_suffix = {}
        self.game_info = game_info.GameInfo()
    
    def game_start(self):
        self.airport_graph.calculate_daily_pessengers()

        self.show_me_the_money()


    def game_end(self):
        pass

    # 添加航空公司
    def add_airlines(self,airlines_name,airline_code):

        if airline_code in self.airlines:
            print("航空公司已存在")
        
        self.game_info.add_airline()

        airline = game_info.Airline(airlines_name,airline_code)
        self.airlines[airline_code] = airline

    # 获取航空公司
    def get_airlines(self):
        return self.airlines
        
    # 添加飞机
    def add_aircraft(self,airline_code,model,first_class_capacity,business_class_capacity,economy_class_capacity):
        if airline_code not in self.airlines:
            print("航空公司不存在")
            return
        
        aircraft = game_info.Aircraft(
            id=self.generate_aircraft_registration('CN'),
            model=model,
            first_class_capacity=first_class_capacity,
            business_class_capacity=business_class_capacity,
            economy_class_capacity=economy_class_capacity,
        )
        self.airlines[airline_code].add_aircraft(aircraft)   
        return aircraft.id

    
    def add_flight(self, airline_code, flight_id, from_code, to_code, aircraft_id, first_class_price, business_class_price, economy_class_price, flight_start_time):
        """Add a flight to the game."""
        if not self.airport_graph.route_exists(from_code, to_code):
            self.airport_graph.add_route(from_code, to_code)

        flight_time = self.airport_graph.get_route_time(from_code, to_code)
        if flight_time is None:
            return

        flight = game_info.Flight(
            flight_id=flight_id,
            from_code=from_code,
            to_code=to_code,
            aircraft_id=aircraft_id,
            first_class_price=first_class_price,
            business_class_price=business_class_price,
            economy_class_price=economy_class_price,
            flight_takeoff_time=datetime.datetime.strptime(flight_start_time, "%H:%M"),
            flight_landing_time=datetime.datetime.strptime(flight_start_time, "%H:%M") + datetime.timedelta(minutes=flight_time),
        )

        if self.airport_graph.add_flight_schedule(flight):
            self.airlines[airline_code].add_flight(flight)
    
        
    def get_airport_graph(self):
        return self.airport_graph   



    def get_flights(self,airline_code):
        return self.airlines[airline_code].get_flights()


    def show_me_the_money(self):
        airline_revenue = {} 
        random_flight_capacity_rate = [random.uniform(0.8,1) for _ in range(3)]

        for airline_code in self.airlines.keys():
            for flight in self.airlines[airline_code].get_flights():

                print (flight.get_aircraft_id())
        print(random_flight_capacity)
        pass

    def calculate_flight_revenue(self, aircraft_id, capacity_rate):
        revenue = 0

        for cang in self.add_airlines 