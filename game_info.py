# game_info.py

AIRCRAFT = {
    "A320": {"capacity": 180, "first_class_capacity": 20, "business_class_capacity": 30, "economy_class_capacity": 130, "distance": 6000},
    "B737": {"capacity": 180, "first_class_capacity": 20, "business_class_capacity": 30, "economy_class_capacity": 130, "distance": 6000},
    "A330": {"capacity": 250, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 180, "distance": 12000},
    "B777": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 12000},
    "A350": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 12000},
    "B787": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 9000},
}


class Airline:
    def __init__(self, name, airline_code):
        self.name = name
        self.airline_code = airline_code
        self.fleet = {}  # 存储飞机
        self.routes = []  # 存储航线
        self.flights = []  # 存储航班
         
    def get_name(self):
        return self.name

    def add_aircraft(self, aircraft):
        self.fleet[aircraft.id] = aircraft  # 添加飞机


    def add_flight(self, flight):
        self.flights.append(flight)  # 添加航班

    def get_fleet(self):
        return self.fleet
    
    def get_aircraft(self, aircraft_id):
        return self.fleet.get(aircraft_id, None)
    
    def get_aircrafts(self):
        return self.fleet   
    

    def get_route_by_from_code(self, from_code):
        route = []
        for route in self.routes:
            if route.from_code == from_code:
                route.append(route)
        return route    

class Flight:
    def __init__(self, flight_id, from_code, to_code, aircraft_id, first_class_price, business_class_price, economy_class_price, flight_takeoff_time,flight_landing_time):
        self.flight_id = flight_id
        self.from_code = from_code
        self.to_code = to_code  
        self.aircraft_id = aircraft_id     
        self.first_class_price = first_class_price
        self.business_class_price = business_class_price
        self.economy_class_price = economy_class_price
        self.flight_takeoff_time = flight_takeoff_time
        self.flight_landing_time = flight_landing_time
    
    def get_aircraft_id(self):
        return self.aircraft_id 
    def get_from_code(self):
        return self.from_code
    def get_to_code(self):
        return self.to_code
    def get_first_class_price(self):
        return self.first_class_price
    def get_business_class_price(self):
        return self.business_class_price
    def get_economy_class_price(self):
        return self.economy_class_price
    def get_flight_start_time(self):
        return self.flight_start_time
    def get_daily_flight_times(self):
        return self.daily_flight_times

class Aircraft:
    def __init__(self, id, model, first_class_capacity, business_class_capacity, economy_class_capacity):
        self.id = id # 飞机编号
        self.model = model  # 飞机型号
        self.first_class_capacity = first_class_capacity  # 头等舱容量
        self.business_class_capacity = business_class_capacity  # 商务舱容量
        self.economy_class_capacity = economy_class_capacity  # 经济舱容量  
    

