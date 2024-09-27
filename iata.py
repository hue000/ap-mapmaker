# game_info.py
from geopy.distance import great_circle
from datetime import datetime
from passenger import PassengerSimulator


AIRCRAFT = {
    "A320": {"capacity": 180, "first_class_capacity": 20, "business_class_capacity": 30, "economy_class_capacity": 130, "distance": 6000},
    "B737": {"capacity": 180, "first_class_capacity": 20, "business_class_capacity": 30, "economy_class_capacity": 130, "distance": 6000},
    "A330": {"capacity": 250, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 180, "distance": 12000},
    "B777": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 12000},
    "A350": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 12000},
    "B787": {"capacity": 300, "first_class_capacity": 30, "business_class_capacity": 40, "economy_class_capacity": 230, "distance": 9000},
}

AIRPORT_INFO = {
    "PEK": {"name": "北京大兴国际机场", "coords": (40.08011, 116.58472), "city": "北京", "country": "中国", "capacity": 100000, "runway_count": 2, "takeoff_landing_interval": 15},
    "HRB": {"name": "哈尔滨太平国际机场", "coords": (45.62308, 126.22229), "city": "哈尔滨", "country": "中国", "capacity": 50000, "runway_count": 2, "takeoff_landing_interval": 15},
    "PVG": {"name": "上海浦东国际机场", "coords": (31.1965, 121.8052), "city": "上海", "country": "中国", "capacity": 80000, "runway_count": 2, "takeoff_landing_interval": 15},
    "SHA": {"name": "上海虹桥国际机场", "coords": (31.1965, 121.3355), "city": "上海", "country": "中国", "capacity": 70000, "runway_count": 2, "takeoff_landing_interval": 15},
    "CAN": {"name": "广州白云国际机场", "coords": (23.3924, 113.2991), "city": "广州", "country": "中国", "capacity": 90000, "runway_count": 2, "takeoff_landing_interval": 15},
    "CTU": {"name": "成都双流国际机场", "coords": (30.5705, 103.9400), "city": "成都", "country": "中国", "capacity": 1000000, "runway_count": 2, "takeoff_landing_interval": 15},
    "XIY": {"name": "西安咸阳国际机场", "coords": (34.4462, 108.7505), "city": "西安", "country": "中国", "capacity": 1000000, "runway_count": 2, "takeoff_landing_interval": 15},
    "HGH": {"name": "杭州萧山国际机场", "coords": (30.2294, 120.4328), "city": "杭州", "country": "中国", "capacity": 1000000, "runway_count": 2, "takeoff_landing_interval": 15},  
    "NKG": {"name": "南京禄口国际机场", "coords": (31.7420, 118.8618), "city": "南京", "country": "中国", "capacity": 1000000, "runway_count": 2, "takeoff_landing_interval": 15},
    "SZX": {"name": "深圳宝安国际机场", "coords": (22.6397, 113.8948), "city": "深圳", "country": "中国", "capacity": 80000, "runway_count": 2, "takeoff_landing_interval": 15},
    "KMG": {"name": "昆明长水国际机场", "coords": (25.2183, 102.7900), "city": "昆明", "country": "中国", "capacity": 1000000, "runway_count": 2, "takeoff_landing_interval": 15},
    "CKG": {"name": "重庆江北国际机场", "coords": (29.7092, 106.6300), "city": "重庆", "country": "中国", "capacity": 1000000, "runway_count": 2, "takeoff_landing_interval": 15},
    "CSX": {"name": "长沙黄花国际机场", "coords": (28.1435, 113.2192), "city": "长沙", "country": "中国", "capacity": 1000000, "runway_count": 2, "takeoff_landing_interval": 15},
    "WUH": {"name": "武汉天河国际机场", "coords": (30.7048, 114.2080), "city": "武汉", "country": "中国", "capacity": 1000000, "runway_count": 2, "takeoff_landing_interval": 15},
}


class IATA:
    def __init__(self):
        self.airports = {}
        for airport_code in AIRPORT_INFO:
            self.add_airport(Airport(airport_code, AIRPORT_INFO[airport_code]["name"], AIRPORT_INFO[airport_code]["city"], AIRPORT_INFO[airport_code]["country"], AIRPORT_INFO[airport_code]["capacity"]))    
       
        self.routes = {}
        self.flights = {}
        self.aircrafts = {}
        self.airlines = {}
        self.aircrafts_counter = {}
        self.flights_scheduled = {}
    
    def add_airport(self, airport):
        self.airports[airport.airport_code] = airport

    def add_aircraft(self, model, airline_code, first_class_capacity, business_class_capacity, economy_class_capacity):
        aircraft_id = self.generate_aircraft_registration(self.airlines[airline_code].country_code)
        self.aircrafts[aircraft_id] = Aircraft(aircraft_id, model, airline_code, first_class_capacity, business_class_capacity, economy_class_capacity)
        return aircraft_id

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
    
    def generate_aircraft_registration(self, country_code):
        registration_prefixes = {
            "CN": "B-",  # 中国
            "US": "N-",   # 美国
            "GB": "G-",  # 英国
            "JP": "JA-",  # 日本
            "DE": "D-",  # 德国
            "FR": "F-",  # 法国
            # 可以根据需要添加更多国家
        }
        
        prefix = registration_prefixes.get(country_code, "XX-")  # 如果国家代码未知,使用 "XX-" 作为默认前缀
        if country_code not in self.aircrafts_counter:
            self.aircrafts_counter[country_code] = 1
        # 生成随机的4位数
        number = f"{self.aircrafts_counter[country_code]:04d}"
        self.aircrafts_counter[country_code] += 1
        return f"{prefix}{number}"
    
    def add_airline(self, airline):
        self.airlines[airline.airline_code] = airline

    def add_flight(self, flight):  
        self.airlines[flight.airline_code].add_flight(flight.flight_id)
        if flight.from_code not in self.routes:
            self.routes[flight.from_code] = {}
        if flight.to_code not in self.routes:
            self.routes[flight.to_code] = {}
        self.routes[flight.from_code][flight.to_code] = self.calculate_flight_time(flight.from_code,flight.to_code)
        self.routes[flight.to_code][flight.from_code] = self.calculate_flight_time(flight.to_code,flight.from_code)
        
    def add_flight_schedule(self, flight):
        if flight.flight_id not in self.flights_scheduled:
            self.flights_scheduled[flight.flight_id] = flight
            return True
        return False

    def add_route(self, from_airport, to_airport):
        if from_airport not in self.routes:
            self.routes[from_airport] = {}

        # 如果目的地机场不存在，则创建一个新的字典
        if to_airport not in self.routes:
            self.routes[to_airport] = {}

        # 如果目的地机场不存在，则创建一个新的字典
        if to_airport not in self.routes[from_airport]:
            self.routes[from_airport][to_airport] = self.calculate_flight_time(from_airport,to_airport)  
        
        if from_airport not in self.routes[to_airport]:
            self.routes[to_airport][from_airport] = self.calculate_flight_time(to_airport,from_airport)


class Airline:
    def __init__(self, airline_code, airline_name, country_code):
        self.airline_code = airline_code
        self.airline_name = airline_name
        self.country_code = country_code
        self.flights = []
        self.aircrafts = []
    def add_flight(self, flight_id):
        self.flights.append(flight_id)
    def add_aircraft(self, aircraft_id):
        self.aircrafts.append(aircraft_id)

class Aircraft:
    def __init__(self, id, model, airline_code, first_class_capacity, business_class_capacity, economy_class_capacity):
        self.id = id # 飞机编号
        self.model = model  # 飞机型号
        self.airline_code = airline_code  # 航空公司代码
        self.first_class_capacity = first_class_capacity  # 头等舱容量
        self.business_class_capacity = business_class_capacity  # 商务舱容量
        self.economy_class_capacity = economy_class_capacity  # 经济舱容量  
    
class Airport:
    def __init__(self, airport_code, airport_name, city, country, capacity):
        self.airport_code = airport_code
        self.airport_name = airport_name
        self.city = city
        self.country = country
        self.capacity = capacity

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

        if self.has_no_conflict(schedule_time):
            self.schedule.append({"flight_id": flight.flight_id, "action": action, "schedule_time": schedule_time, "aircraft_id": flight.aircraft_id, "from_code": flight.from_code, "to_code": flight.to_code})
        else:
            print(f"航班{flight.flight_id}在{schedule_time}的时间与已有航班冲突")
            return False
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


if __name__ == "__main__":
    iata = IATA()

    iata.add_airline(Airline("CA","中国国际航空","CN"))
    iata.add_airline(Airline("MU","中国东方航空","CN"))
    iata.add_airline(Airline("CZ","中国南方航空","CN"))
    

    aircraft_id = iata.add_aircraft("A320","CA",20,30,130)
    iata.add_flight(Flight("CA","CA1001","PEK","HRB",aircraft_id,3000,2000,1000,datetime(2024,1,1,8,0),datetime(2024,1,1,10,0)))
    iata.add_flight(Flight("CA","CA1001","PEK","CAN",aircraft_id,3000,2000,1000,datetime(2024,1,1,8,0),datetime(2024,1,1,10,0)))
    iata.add_flight(Flight("CA","CA1001","PEK","SZX",aircraft_id,3000,2000,1000,datetime(2024,1,1,8,0),datetime(2024,1,1,10,0)))
    iata.add_flight(Flight("CA","CA1001","PEK","SHA",aircraft_id,3000,2000,1000,datetime(2024,1,1,8,0),datetime(2024,1,1,10,0)))

    aircraft_id = iata.add_aircraft("A320","MU",20,30,130)
    iata.add_flight(Flight("MU","MU1001","PEK","HRB",aircraft_id,3000,2000,1000,datetime(2024,1,1,8,0),datetime(2024,1,1,10,0)))

    aircraft_id = iata.add_aircraft("A320","CZ",20,30,130)
    iata.add_flight(Flight("CZ","CZ1001","PEK","HRB",aircraft_id,3000,2000,1000,datetime(2024,1,1,8,0),datetime(2024,1,1,10,0)))


    passenger_simulator = PassengerSimulator()
    passenger_simulator.simulator_routes_passengers(iata.routes,iata.airports)
