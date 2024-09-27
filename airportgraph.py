from geopy.distance import great_circle
import random
from datetime import datetime
import game_info

AIRPORT_INFO = {
    "PEK": {"name": "北京大兴国际机场", "coords": (40.08010101,116.5849991), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "HRB": {"name": "哈尔滨太平国际机场", "coords": (45.623402,126.250000), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "PVG": {"name": "上海浦东国际机场", "coords": (31.197999,121.336001), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "SHA": {"name": "上海虹桥国际机场", "coords": (31.197999,121.336001), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "CAN": {"name": "广州白云国际机场", "coords": (23.129168,113.219192), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "CTU": {"name": "成都双流国际机场", "coords": (30.578500,103.946001), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "XIY": {"name": "西安咸阳国际机场", "coords": (34.446500,108.751600), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "HGH": {"name": "杭州萧山国际机场", "coords": (30.229500,120.435000), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},  
    "NKG": {"name": "南京禄口国际机场", "coords": (31.738056,118.861944), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "SZX": {"name": "深圳宝安国际机场", "coords": (22.639361,113.810316), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "KMG": {"name": "昆明长水国际机场", "coords": (25.218333,102.920000), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "CKG": {"name": "重庆江北国际机场", "coords": (29.719167,106.630167), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "CSX": {"name": "长沙黄花国际机场", "coords": (28.189270,113.219920), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "WUH": {"name": "武汉天河国际机场", "coords": (30.792300,114.208000), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15},
    "XIY": {"name": "西安咸阳国际机场", "coords": (34.446500,108.751600), "passengers": 1000000,"runway_count":2, "takeoff_landing_interval":15}  
}
      

class AirportGraph:
    def __init__(self):
        self.graph = {}
        self.airport_routes = {}
        self.airport_passengers = {}
        self.airport_schedule = {}
        for airport_code in AIRPORT_INFO:
            self.add_airport(airport_code)

    def get_graph(self):
        return self.graph
    
    def get_airport_schedule(self, airport_code):
        return self.add_flight_schedule[airport_code]

    def daily_init(self,date,from_airport,to_airport,remaining_passengers):
        if date not in self.graph:
            self.graph[date] = {}
        if from_airport not in self.graph[date]:
            self.graph[date][from_airport] = {}
        if to_airport not in self.graph[date][from_airport]:
            self.graph[date][from_airport][to_airport] = 0

    def add_airport(self, airport_code):
        if airport_code not in self.graph:
            self.graph[airport_code] = {}
            self.airport_schedule[airport_code] = AirportSchedule(airport_code, AIRPORT_INFO[airport_code]["runway_count"],AIRPORT_INFO[airport_code]["takeoff_landing_interval"])   
        if airport_code not in self.airport_passengers:
            self.airport_passengers[airport_code] = {}
           

    def add_route(self, from_airport, to_airport):
        if from_airport not in self.graph:
            self.graph[from_airport] = {}

        # 如果目的地机场不存在，则创建一个新的字典
        if to_airport not in self.graph:
            self.graph[to_airport] = {}

        # 如果目的地机场不存在，则创建一个新的字典
        if to_airport not in self.graph[from_airport]:
            self.graph[from_airport][to_airport] = self.calculate_flight_time(from_airport,to_airport)  
        
        if from_airport not in self.graph[to_airport]:
            self.graph[to_airport][from_airport] = self.calculate_flight_time(to_airport,from_airport)

    def get_route(self,from_airport):
        return self.graph[from_airport]

    def route_exists(self, from_airport, to_airport):
        # 检查航线是否存在
        if from_airport not in self.graph:
            return False
        if to_airport not in self.graph[from_airport]:
            return False
        return True

    def set_daily_passengers(self,airport,date):
        pass


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


