import sys
import requests
import json
from datetime import datetime
import time

def get_stacks_block_height():
	url = "https://api.mainnet.hiro.so/extended/v1/block"
	json_data = requests.get(url).json()
	block_height_now = json_data['total']

	return block_height_now

def check_stxmaps(block_from, block_to):
	block_id = block_from
	while block_id < block_to:
		check_stxmap_by_id(str(block_id))
		block_id += 1

def check_stxmap_by_id(block_id):

	url = "https://satscreener.com/api/stxmaps/" + block_id
	json_data = requests.get(url).json()
	
	if str(json_data['id']) != "None":
		print(str(json_data['id']) + " | " + json_data['wallet_id'] + " | " + json_data['deploy_time'])
	else:
		print(str(block_id) + " : None")

# 指定区间的bitmap
def exec_check_stxmaps(num):
	print("block_id | owner_addr | time")
	print("------------------------------------------------")

	block_to = int(get_stacks_block_height())
	block_from = block_to - num
	check_stxmaps(block_from, block_to)

def main():
	argv_len = len(sys.argv)
	if argv_len == 1 :
		exec_check_stxmaps(12)
	elif argv_len == 2 :
		num = int(sys.argv[1])
		exec_check_stxmaps(num)
	else :
		print("para err!!!")
	

# 主函数
if __name__=="__main__":
	main()