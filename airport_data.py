import csv

# CSV文件路径

def get_airports_data():
    csv_file_path = 'airport.csv'

    # 要读取的列名
    columns_to_read = ['name','iata_code','latitude_deg', 'longitude_deg']

    # 用于存储读取的数据
    data = []

    # 打开CSV文件
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        # 创建一个csv阅读器
        csv_reader = csv.DictReader(csvfile)
        
        # 遍历CSV文件中的每一行
        for row in csv_reader:
            # 创建一个字典，只包含我们需要的列
            row_data = {column: row[column] for column in columns_to_read if column in row}
            data.append(row_data)

    return data