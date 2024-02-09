import sys
import requests
import json
from datetime import datetime
import time

def get_blocks():
	offset = 127980
	limit = 30

	print("height" + "," + "burn_block_height" + "," + "burn_block_time" + "," + "txs" + "," + "miner_txid")
	print("----------------------------------------------------------------------------------------------------------")

	url = "https://api.mainnet.hiro.so/extended/v1/block?limit=" + str(limit) + "&offset=" + str(offset)
	json_data = requests.get(url).json()
	total = json_data['total']
	results_list = json_data['results']
	
	while offset < total :
	
		for block in results_list :
			height = block['height']
			burn_block_height = block['burn_block_height']
			burn_block_time = datetime.fromtimestamp(block['burn_block_time'])
			burn_block_time_str = burn_block_time.strftime("%Y-%m-%d %H:%M:%S")
			txs = len(block['txs'])
			miner_txid = "https://mempool.space/tx/" + block['miner_txid'][2:70]
			
			print(str(height) + "," + str(burn_block_height) + "," + burn_block_time_str + "," + str(txs) + "," + miner_txid)
		
		offset = offset + limit
		url = "https://api.mainnet.hiro.so/extended/v1/block?limit=" + str(limit) + "&offset=" + str(offset)
		json_data = requests.get(url).json()
		total = json_data['total']
		results_list = json_data['results']
		

def main():
	get_blocks();

# 主函数
if __name__=="__main__":
	main()