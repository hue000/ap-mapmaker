# game_info.py
from geopy.distance import great_circle
import random

AIRPORT_INFO = {
    "PEK": {"name": "北京大兴国际机场", "coords": (40.08010101,116.5849991), "capacity": 100000,"runway_count":2, "takeoff_landing_interval":15},
    "HRB": {"name": "哈尔滨太平国际机场", "coords": (45.623402,126.250000), "capacity": 50000,"runway_count":2, "takeoff_landing_interval":15},
    "PVG": {"name": "上海浦东国际机场", "coords": (31.197999,121.336001), "capacity": 70000,"runway_count":2, "takeoff_landing_interval":15},
    "SHA": {"name": "上海虹桥国际机场", "coords": (31.197999,121.336001), "capacity": 80000,"runway_count":2, "takeoff_landing_interval":15},
    "CAN": {"name": "广州白云国际机场", "coords": (23.129168,113.219192), "capacity": 90000,"runway_count":2, "takeoff_landing_interval":15},
    "CTU": {"name": "成都双流国际机场", "coords": (30.578500,103.946001), "capacity": 80000,"runway_count":2, "takeoff_landing_interval":15},
    "XIY": {"name": "西安咸阳国际机场", "coords": (34.446500,108.751600), "capacity": 50000,"runway_count":2, "takeoff_landing_interval":15},
    "HGH": {"name": "杭州萧山国际机场", "coords": (30.229500,120.435000), "capacity": 70000,"runway_count":2, "takeoff_landing_interval":15},  
    "NKG": {"name": "南京禄口国际机场", "coords": (31.738056,118.861944), "capacity": 60000,"runway_count":2, "takeoff_landing_interval":15},
    "SZX": {"name": "深圳宝安国际机场", "coords": (22.639361,113.810316), "capacity": 70000,"runway_count":2, "takeoff_landing_interval":15},
    "KMG": {"name": "昆明长水国际机场", "coords": (25.218333,102.920000), "capacity": 30000,"runway_count":2, "takeoff_landing_interval":15},
    "CKG": {"name": "重庆江北国际机场", "coords": (29.719167,106.630167), "capacity": 70000,"runway_count":2, "takeoff_landing_interval":15},
    "CSX": {"name": "长沙黄花国际机场", "coords": (28.189270,113.219920), "capacity": 30000,"runway_count":2, "takeoff_landing_interval":15},
    "WUH": {"name": "武汉天河国际机场", "coords": (30.792300,114.208000), "capacity": 60000,"runway_count":2, "takeoff_landing_interval":15},
}

AIRCRAFT = {
    "A320": {"capacity": 180, "first_class_capacity": 20, "business_class_capacity": 30, "economy_class_capacity": 130, "distance": 6000},
    "B737": {"capacity": 180, "first_class_capacity": 20, "business_class_capacity": 30, "economy_class_capacity": 130, "distance": 6000},
    "A330": {"capacity": 250, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 180, "distance": 12000},
    "B777": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 12000},
    "A350": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 12000},
    "B787": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 9000},
}

class GameInfo:
    def __init__(self):
        self.airlines = {}  # 存储航空公司

        self.airports = {}  # 存储机场
        for airport_code in AIRPORT_INFO:
            self.add_airport(airport_code, AIRPORT_INFO[airport_code]["capacity"])

        self.aircrafts = {}  # 存储世界上所有飞机
        self.flights = {}  # 存储航班

        self.routes = {} # 存储航线

    # 生成飞机注册号    
    def generate_aircraft_registration(self, country_code):
        import string

        # 根据国家代码生成注册号的前缀
        country_prefixes = {
            'US': 'N',
            'CN': 'B',
            'UK': 'G',
            'DE': 'D',
            'FR': 'F',
            # 可以根据需要添加更多国家
        }

        prefix = country_prefixes.get(country_code, 'X')  # 默认前缀为'X'
        if country_code not in self.country_current_suffix:
            self.country_current_suffix[country_code] = 1
        # 生成自增的后缀，确保后缀为6位数
        suffix = str(self.country_current_suffix[country_code]).zfill(6)    
        self.country_current_suffix[country_code] += 1
        return f"{prefix}-{suffix}"

    # 获取机场的乘客
    def get_airport_passengers(self, from_code, route):

        """Generate a dictionary of passengers for each airport"""
        BASE_PASSENGERS_FACTOR = 0.6

        route_passengers = {}
        to_airport_passenger = {}

        for to_code in route:
            to_airport_passenger[to_code] = self.airport_capacity[to_code]
            
        to_airport_count = len(to_airport_passenger)
        if to_airport_count ==0:
            return None    

        random_factor = 0.8 / (to_airport_count+1)/to_airport_count/2
        
        sorted_passengers = sorted(to_airport_passenger.items(), key=lambda x: x[1], reverse=False)

        base_passengers = self.airport_capacity[from_code] / to_airport_count * BASE_PASSENGERS_FACTOR
        remaining_passengers = self.airport_capacity[from_code]  - base_passengers * to_airport_count

        for i, (code, capacity) in enumerate(sorted_passengers):
            route_passengers[code] = base_passengers
            random_adjustment = random.uniform(0, random_factor)
            for j in range(0,i+1):
                random_passengers = min(int(capacity * random_adjustment), remaining_passengers)
                route_passengers[code] = route_passengers.get(code, 0) + random_passengers
                remaining_passengers -= random_passengers
            if remaining_passengers <= 0:
                break          
        return route_passengers
    
    def add_aircraft(self,airline_code, model, first_class_capacity, business_class_capacity, economy_class_capacity):
        id = self.generate_aircraft_registration("CN")
        aircraft = Aircraft(id, model, first_class_capacity, business_class_capacity, economy_class_capacity)
        self.aircrafts[id] = aircraft
        self.airlines[airline_code].add_aircraft(aircraft)  

    def get_aircraft(self, id):
        return self.aircrafts[id]

    def add_airline(self, name, airline_code):
        self.airlines[airline_code] = Airline(name, airline_code)   
    def get_airline(self, airline_code):
        return self.airlines[airline_code]
    
    def add_flight(self, airline_code, flight_id, from_code, to_code, aircraft_id, first_class_price, business_class_price, economy_class_price, flight_takeoff_time,flight_landing_time): 
        
        flight = Flight(airline_code, flight_id, from_code, to_code, aircraft_id, first_class_price, business_class_price, economy_class_price, flight_takeoff_time,flight_landing_time)
        self.flights[flight_id] = flight
        self.airlines[airline_code].add_flight(flight)
    
    def get_flight(self, flight_id):
        return self.flights[flight_id]

        
    def add_route(self, from_code, to_code):
        if from_code not in self.routes:
            self.routes[from_code][to_code] = self.calculate_flight_time(from_code, to_code)

        # 如果目的地机场不存在，则创建一个新的字典
        if to_code not in self.routes:
            self.routes[to_code][from_code] = self.calculate_flight_time(to_code, from_code)    

    def calculate_flight_time(self, form_code, to_code):

        upload_time = 20
        download_time = 20
        takeoff_time = 30
        landing_time = 30
        from_airport = AIRPORT_INFO[form_code]
        to_airport = AIRPORT_INFO[to_code]
        distance = great_circle(from_airport["coords"], to_airport["coords"]).kilometers
        
        min_distance = 250
        if distance < min_distance:
            print("距离太短，无法飞行")
            return 0
        else:
            cruising_speed = 900  # 假设巡航速度为900公里/小时
            cruising_time = distance / cruising_speed * 60
            total_time = upload_time + download_time + takeoff_time + landing_time + cruising_time 
        return total_time


class Airline:
    def __init__(self, name, airline_code):
        self.name = name
        self.airline_code = airline_code
        self.money = 0
        self.aircrafts = {}  # 存储飞机
        self.flights = []  # 存储航班
    
    def add_aircraft(self, aircraft):
        self.aircrafts[aircraft.id] = aircraft

    def add_flight(self, flight):
        self.flights.append(flight)

class Flight:
    def __init__(self, airline_code, flight_id, from_code, to_code, aircraft_id, first_class_price, business_class_price, economy_class_price, flight_takeoff_time,flight_landing_time):
        self.airline_code = airline_code
        self.flight_id = flight_id
        self.from_code = from_code
        self.to_code = to_code  
        self.aircraft_id = aircraft_id     
        self.first_class_price = first_class_price
        self.business_class_price = business_class_price
        self.economy_class_price = economy_class_price
        self.flight_takeoff_time = flight_takeoff_time
        self.flight_landing_time = flight_landing_time

class Aircraft:
    def __init__(self, id, model, first_class_capacity, business_class_capacity, economy_class_capacity):
        self.id = id # 飞机编号
        self.model = model  # 飞机型号
        self.first_class_capacity = first_class_capacity  # 头等舱容量
        self.business_class_capacity = business_class_capacity  # 商务舱容量
        self.economy_class_capacity = economy_class_capacity  # 经济舱容量  

class Airport:
    def __init__(self, code, runway_count, takeoff_landing_interval):
        self.code = code
        self.runway_count = runway_count
        self.takeoff_landing_interval = takeoff_landing_interval
        self.routes = {}
        self.flights = {}
    
    def add_flight(self, flight):
        self.flights[flight.flight_id] = flight


class AirportGraph:
    def __init__(self):
     
        self.airport_capacity = {}
        self.airport_schedule = {}
        
   
    
    def get_airport_schedule(self, airport_code):
        return self.add_flight_schedule[airport_code]
   
           


    def get_route(self,from_airport):
        return self.graph[from_airport]

    def route_exists(self, from_airport, to_airport):
        # 检查航线是否存在
        if from_airport not in self.graph:
            return False
        if to_airport not in self.graph[from_airport]:
            return False
        return True


    def add_flight_schedule(self,flight):
        if flight.from_code not in self.airport_schedule:
            return False
        if flight.to_code not in self.airport_schedule:
            return False
        if self.airport_schedule[flight.from_code].add_flight(flight): 
            if self.airport_schedule[flight.to_code].add_flight(flight):
                return True
        return False
    def get_route_time(self,from_code,to_code):
        return self.graph[from_code][to_code]
    

class AirportSchedule:
    def __init__(self, airport_code, runway_count, takeoff_landing_interval):
        
        self.airport_code = airport_code  # 机场代码
        self.runway_count = runway_count  # 跑道数量
        self.takeoff_landing_interval = takeoff_landing_interval  # 起降间隔时间（分钟）
        self.schedule = []

    def add_flight(self, flight):
        # 添加出港航班
        action = "takeoff"
        schedule_time = flight.flight_takeoff_time

        # 如果航班的目的地是当前机场，则添加进港航班
        if flight.to_code == self.airport_code:
            action = "landing"
            schedule_time = flight.flight_landing_time
        '''
        if self.has_no_conflict(schedule_time):
            self.schedule.append({"flight_id": flight.flight_id, "action": action, "schedule_time": schedule_time, "aircraft_id": flight.aircraft_id, "from_code": flight.from_code, "to_code": flight.to_code})
        else:
            print(f"航班{flight.flight_id}在{schedule_time}的时间与已有航班冲突")
            return False
        '''
        return True


        

    def display_schedule(self):
        for flight in self.schedule:
            print(f"航班ID: {flight['flight_id']}, 动作: {flight['action']}, 时间: {flight['schedule_time']}")
    

    def get_schedule_time(self):
        self.schedule.sort(key=lambda flight: flight['schedule_time'])
        for flight in self.schedule:
            print(f"航班ID: {flight['flight_id']}, 动作: {flight['action']}, 时间: {flight['schedule_time']}")

    def has_no_conflict(self, new_flight_time):
        for flight in self.schedule:
            if abs(flight['schedule_time'] - new_flight_time) < 5:  # 判断是否在前后5分钟内
                return False
        return True


