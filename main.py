import game



def create_aircraft(game,airline_name,model,first_class_capacity,business_class_capacity,economy_class_capacity):
    game.add_aircraft(airline_name,model,first_class_capacity,business_class_capacity,economy_class_capacity)


if __name__ == "__main__":

    # 创建游戏
    game = game.Game()

    # 创建航空公司
    AIRLINE_NAME = {
        "中国国际航空":"CA",
        "南方航空":"CZ",
        "东方航空":"MU",
        "海南航空":"HU",
        "深圳航空":"ZH",
        "四川航空":"3U",
        "山东航空":"SC",
        "厦门航空":"MF",
        "上海航空":"FM",
        "吉祥航空":"HO",      
    }
    for airline_name,airline_code in AIRLINE_NAME.items():
        game.add_airlines(airline_name,airline_code)

    # 创建飞机
    airline_id = create_aircraft(game,"CA","A320",20,30,130)  



    game.add_flight("CA","CA001","PEK","HRB",airline_id,1000,800,500,"08:00")

    print(game.get())