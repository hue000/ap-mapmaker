import random
from collections import defaultdict, OrderedDict

class PassengerSimulator:
    def __init__(self):
        self.base_passenger_rate = 0.6  # 基础旅客率
        self.random_factor = 0.1  # 随机因子,用于增加变化性
        
    def simulator_routes_passengers(self, routes, airports):
        routes_passengers = {}
        
        for from_code in routes:
            if from_code not in routes_passengers:
                routes_passengers[from_code] = {}
            to_airports_count = len(routes[from_code])
            base_passengers = int(self.base_passenger_rate * airports[from_code].capacity/to_airports_count)    

            to_capacity = {}
            for to_code in routes[from_code]:
                to_capacity[to_code] = airports[to_code].capacity
            
            sorted_capacity = sorted(to_capacity.items(), key=lambda x: x[1])
            print(sorted_capacity)
      
            
        return routes_passengers

    def create_sorted_airport_capacity_set(self):
        # 创建一个包含(机场代码, 容量)元组的列表
        airport_capacities = [(airport.code, airport.capacity) for airport in self.airports]
    
        # 按容量升序排序
        sorted_airport_capacities = sorted(airport_capacities, key=lambda x: x[1])
    
        # 创建有序字典
        sorted_capacity_set = OrderedDict(sorted_airport_capacities)
    
        return sorted_capacity_set

    def get_airport_passengers(self):
        sorted_capacity_set = self.create_sorted_airport_capacity_set()
        airport_count = len(self.airports)
        passengers = {}

        for (from_code, capacity) in sorted_capacity_set.items():
            passengers[from_code] = {}
            to_passengers_count_times = {}
            base_passengers = int(self.base_passenger_rate * capacity/(airport_count-1))
            for i, to_code in enumerate(sorted_capacity_set.keys()):
                if to_code != from_code:
                    passengers[from_code][to_code] = int(self.base_passenger_rate * capacity/(airport_count-1))
                    to_passengers_count_times[to_code] = i
            remaining_passengers = capacity - base_passengers * (airport_count-1)
            cal_times = max(to_passengers_count_times.values())
            random_factor = 0.8 / cal_times / len(passengers[from_code])

            for i in range(cal_times):
                if remaining_passengers <= 0:
                    break
                for to_code in passengers[from_code]:
                    random_adjustment = random.uniform(0, random_factor)
                    if to_passengers_count_times[to_code] >= i and remaining_passengers > 0:
                        random_passengers = min(int(capacity * random_adjustment), remaining_passengers)
                        passengers[from_code][to_code] += random_passengers
                        remaining_passengers -= random_passengers
                    if remaining_passengers <= 0:
                        break
                
                
        return passengers


