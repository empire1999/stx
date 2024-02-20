import requests
import json
from datetime import datetime
import time
import binascii
import os

def get_stacks_block_height():
	url = "https://api.mainnet.hiro.so/extended/v1/block"
	json_data = requests.get(url).json()
	block_height_now = json_data['total']
	return block_height_now

def get_bitcoin_block_tip_height():
	url = "https://mempool.space/api/blocks/tip/height"
	return requests.get(url).text

def mint_stxmap():
	stacks_block_height = 0
	bitcoin_block_height = 0
	
	mint_fee_1 = 500000
	mint_fee_2 = 800000
	mint_fee_3 = 1000000
	
	bef_time = datetime.now()
	while 1:
		try :
			bitcoin_block_height_now = int(get_bitcoin_block_tip_height())
			if bitcoin_block_height_now != 0 and bitcoin_block_height != bitcoin_block_height_now:
				bitcoin_block_height = bitcoin_block_height_now
				now = datetime.now()
				now_str = now.strftime("%Y-%m-%d %H:%M:%S")
				block_time = now - bef_time
				print("◇ <bitcoin height>: " + str(bitcoin_block_height) + " - " + str(stacks_block_height) + " (" + now_str + ")" + " +block_time+ " + str(block_time) + " = " + str(block_time.total_seconds()))
				bef_time = now
				
				if stacks_block_height > 0:
					mint_fee_1 = mint_fee_1 + 100
					cmd1 = "stx send_tokens SPXXXXXXXXXXXXXXXXXXXXXXA 1 " + str(mint_fee_1) + " 320 " + " \"KEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\" \"" + str(stacks_block_height + 2) + ".stxmap\""
					print("------------------------------------------------")
					print("[CMD]\t" + cmd1)
					os.system(cmd1)
					
					time.sleep(3)

					mint_fee_2 = mint_fee_2 + 100
					cmd2 = "stx send_tokens SPXXXXXXXXXXXXXXXXXXXXXXB 1 " + str(mint_fee_2) + " 236 " + " \"KEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\" \"" + str(stacks_block_height + 2) + ".stxmap\""
					print("------------------------------------------------")
					print("[CMD]\t" + cmd2)
					os.system(cmd2)
			
			stacks_block_height_now = int(get_stacks_block_height()) 
			if stacks_block_height_now != 0 and stacks_block_height != stacks_block_height_now:
				stacks_block_height = stacks_block_height_now
				now = datetime.now()
				now_str = now.strftime("%Y-%m-%d %H:%M:%S")
				print("##########################################")
				print("$ <Stxmap> mint_number - block_height: " + str(stacks_block_height + 2) + " - " + str(stacks_block_height_now) + " (" + now_str + ")")

				mint_fee_3 = mint_fee_3 + 100
				cmd3 = "stx send_tokens SPXXXXXXXXXXXXXXXXXXXXXXC 1 " + str(mint_fee_3) + " 240 " + " \"KEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\" \"" + str(stacks_block_height + 1) + ".stxmap\""
				print("------------------------------------------------\n\n")
				print("[CMD]\t" + cmd3)
				os.system(cmd3)

		except Exception:
			time.sleep(5)

		time.sleep(5)

def main():
	mint_stxmap()

# 主函数
if __name__=="__main__":
	main()
