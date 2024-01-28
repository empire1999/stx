import requests
import json
from datetime import datetime
import time

stacks_block_height = 0
bitcoin_block_height = 0

def get_stacks_block_height():
	url = "https://api.mainnet.hiro.so/extended/v1/block"
	try:
		json_data = requests.get(url).json()
		block_height_now = json_data['total']
	except requests.exceptions.RequestException as err:
		print ("RequestException:",e)
		block_height_now = "0"
	except requests.exceptions.HTTPError as e:
		print ("Http Error:",e)
		block_height_now = "0"
	except requests.exceptions.ConnectionError as e:
		print ("Connection Error:",e)
		block_height_now = "0"
	except requests.exceptions.Timeout as e:
		print ("Timeout Error:",e)
		block_height_now = "0"
	return block_height_now

def get_bitcoin_block_tip_height():
	url = "https://mempool.space/api/blocks/tip/height"
	return requests.get(url).text
	
def exec_check_block_height():
	global stacks_block_height
	global bitcoin_block_height

	while 1:
		bitcoin_block_height_now = int(get_bitcoin_block_tip_height())
		if bitcoin_block_height_now != 0 and bitcoin_block_height != bitcoin_block_height_now:
			bitcoin_block_height = bitcoin_block_height_now
			now = datetime.now()
			now_str = now.strftime("%Y-%m-%d %H:%M:%S")
			print("\n◇ bitcoin height: " + str(bitcoin_block_height) + " (" + now_str + ")" + "\a")
			print("------------------------------------------------")
		
		stacks_block_height_now = int(get_stacks_block_height())
		if stacks_block_height_now != 0 and stacks_block_height != stacks_block_height_now:
			stacks_block_height = stacks_block_height_now
			now = datetime.now()
			now_str = now.strftime("%Y-%m-%d %H:%M:%S")
			print("$ Stxmap mint_number - block_height: " + str(stacks_block_height + 2) + " - |" + str(stacks_block_height_now) + "| (" + now_str + ")" + "\a\a")
			print("------------------------------------------------")

		time.sleep(10)

def main():
	exec_check_block_height()

# 主函数
if __name__=="__main__":
	main()