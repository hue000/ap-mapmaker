import random
from collections import defaultdict, OrderedDict

class Airport:
    def __init__(self, code, name, city, country, capacity):
        self.code = code
        self.name = name
        self.city = city
        self.country = country
        self.capacity = capacity  # 机场容量
        self.traffic = 0  # 当前流量


class PassengerSimulator:
    def __init__(self, airports):
        self.airports = airports
        self.base_passenger_rate = 0.6  # 基础旅客率
        self.random_factor = 0.1  # 随机因子,用于增加变化性

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
            random_factor = 0.5 / cal_times / len(passengers[from_code])

            for i in range(cal_times):
                if remaining_passengers <= 0:
                    break
                for to_code in passengers[from_code]:
                    random_adjustment = random.uniform(0, random_factor)
                    random_factor *= 1.2
                    if to_passengers_count_times[to_code] >= i and remaining_passengers > 0:
                        random_passengers = min(int(capacity * random_adjustment), remaining_passengers)
                        passengers[from_code][to_code] += random_passengers
                        remaining_passengers -= random_passengers
                    if remaining_passengers <= 0:
                        break
                
                
        return passengers


# 示例使用
if __name__ == "__main__":
     # 创建一些机场
    airports = [
        Airport("PEK", "北京首都国际机场", "北京", "中国", 1000000),  # 年旅客吞吐量约1亿
        Airport("SHA", "上海虹桥国际机场", "上海", "中国", 500000),   # 年旅客吞吐量约5000万
        Airport("CAN", "广州白云国际机场", "广州", "中国", 700000),   # 年旅客吞吐量约7000万
        Airport("SZX", "深圳宝安国际机场", "深圳", "中国", 400000),   # 年旅客吞吐量约4000万
    ]

    passenger_simulator = PassengerSimulator(airports)
   
    print(passenger_simulator.get_airport_passengers())
