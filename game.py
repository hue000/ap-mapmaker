from iata import IATA
from iata import Flight

class Game:
    def __init__(self):
        self.iata = IATA()
    
    def game_start(self):
        
        self.show_me_the_money()


    def game_end(self):
        pass

    # 添加航空公司
    def add_airline(self,airlines_name,airline_code):
        self.iata.add_airline(airlines_name,airline_code)

    def buy_aircraft(self,airline_code):
        aircraft_id = self.iata.add_aircraft("A320", airline_code, 20, 30,130)    
    
    def add_flight(self, airline_code, flight_id, from_code, to_code, aircraft_id, first_class_price, business_class_price, economy_class_price, flight_start_time):
        self.iata.add_flight(Flight(airline_code, flight_id, from_code, to_code, aircraft_id, first_class_price, business_class_price, economy_class_price, flight_start_time))
