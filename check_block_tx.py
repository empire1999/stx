import sys
import requests
import json
from datetime import datetime
import time
import binascii

def hex_to_str(hex_str):
	hex = hex_str.encode('utf-8')
	str_bin = binascii.unhexlify(hex)
	return str_bin.decode('utf-8')

def get_stacks_block_height():
	url = "https://api.mainnet.hiro.so/extended/v1/block"
	json_data = requests.get(url).json()
	block_height_now = json_data['total']

	return block_height_now

def check_block_tx(block_height):
	offset = 0
	limit = 50
	url = "https://api.mainnet.hiro.so/extended/v1/tx/block_height/" + block_height + "?limit=" + str(limit)
	json_data = requests.get(url).json()
	total = json_data['total']
	results_list = json_data['results']
	
	tx_list = []
	while offset < total :
	
		for tx in results_list :
			tx_type = tx['tx_type']
			if tx_type == "token_transfer" :
				# 将stxmap铭文加到list
				nonce = tx['nonce']
				tx_index = tx['tx_index']
				fee_rate = int(tx['fee_rate']) / 1000000
				rec_addr = tx['token_transfer']['recipient_address']
				memo_hex = tx['token_transfer']['memo']
				memo = hex_to_str(memo_hex[2:28])
				if memo.find("stxmap") >= 0:
					dict = {'nonce' : nonce, 'fee_rate' : fee_rate, 'rec_addr' : rec_addr, 'memo' : memo, 'tx_index' : tx_index}
					tx_list.append(dict)
		
		offset = offset + limit
		url = "https://api.mainnet.hiro.so/extended/v1/tx/block_height/" + block_height + "?limit=" + str(limit) + "&offset=" + str(offset)
		json_data = requests.get(url).json()
		total = json_data['total']
		results_list = json_data['results']
		
	print("\n◇ block_height: ", block_height)
	print("stxmap | (tx_index) | rec_addr | [nonce] | fee_rate(stx)")
	print("-----------------------------------------------------")

	# List按照memo和fee排序后打印
	tx_list.sort(key = lambda k: (k.get('memo', 0), k.get('fee_rate', 0)))
	for idx, tx in enumerate(tx_list) :
		print(tx['memo'] + " | (" + str(tx['tx_index']) + ") | " + tx['rec_addr'] + " | [" + str(tx['nonce']) + "] | "  + str(tx['fee_rate']))

	print("-----------------------------------------------------\n")
	

# 当前block的tx
def exec_check_current_block_tx():
	block_height_now = get_stacks_block_height()
	check_block_tx(str(block_height_now))

# 前几个block的tx
def exec_check_blocks_tx(num):
	block_to = get_stacks_block_height()
	block_id = block_to - num
	while block_id < block_to:
		block_id = block_id + 1
		check_block_tx(str(block_id))

# 区间block的tx
def exec_check_range_blocks_tx(block_from, block_to):
	block_id = block_from
	while block_id <= block_to:
		check_block_tx(str(block_id))
		block_id = block_id + 1

def main():
	argv_len = len(sys.argv)
	if argv_len == 1 :
		exec_check_current_block_tx()
	elif argv_len == 2 :
		num = int(sys.argv[1])
		exec_check_blocks_tx(num)
	elif argv_len == 3 :
		block_from = int(sys.argv[1])
		block_to = int(sys.argv[2])
		exec_check_range_blocks_tx(block_from, block_to)
	else :
		print("para err!!!")

# 主函数
if __name__=="__main__":
	main()
