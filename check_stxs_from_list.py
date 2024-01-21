import requests
import json
from datetime import datetime
import time
import csv

def check_stxs_from_list():
    filename_in = "./list.txt"
    try:
        with open(filename_in, encoding='utf-8', newline='') as f_in:
           for cols in csv.reader(f_in, delimiter='\t'):
               stxs_name = cols[0]
               #print(stxs_name)
               check_stxs_by_id(stxs_name)
    except Exception as e:
        print(e)
    finally:
        f_in.close()

def check_stxs_by_id(block_id):
    global headers
    global fee_rate_max

    url = "https://api.stx20.com/api/v1/domain/" + block_id
    json_data = requests.get(url).json()
    print(block_id + " : ", json_data)

    #json_str = json.dumps(json_data, indent=4)
    #print(json_str)


def exec_check_stxs():
    check_stxs_from_list()

def main():
    exec_check_stxs()

# 主函数
if __name__=="__main__":
    main()
