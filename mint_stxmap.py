import requests
import json
from datetime import datetime
import time
import binascii
import os

MINT_END_HEIGHT = 149820
MINT_SEND_ADDR = "SPXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXTO"
MINT_FEE_HIGH = 36100
MINT_FEE_LOW = 26100
MINT_ADDR = "SPXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXFROM"
MINT_KEY = "FROMKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

def get_stacks_block_height():
	url = "https://api.mainnet.hiro.so/extended/v1/block"
	json_data = requests.get(url).json()
	block_height_now = json_data['total']
	return block_height_now

def get_bitcoin_block_tip_height():
	url = "https://mempool.space/api/blocks/tip/height"
	return requests.get(url).text


def get_next_nonce():
	url = "https://api.mainnet.hiro.so/extended/v1/address/" + MINT_ADDR + "/nonces"
	json_data = requests.get(url).json()
	detected_missing_nonces = json_data['detected_missing_nonces']
	if len(detected_missing_nonces) :
		return -1
	else :
		possible_next_nonce = json_data['possible_next_nonce']
		return possible_next_nonce

def mint_stxmap():
	stacks_block_height = 0
	bitcoin_block_height = 0
	mint_flag = 0

	mint_nonce = get_next_nonce()
	if mint_nonce < 0 :
		print("取得possible_next_nonce失败")
		return
	
	print("发送到地址：" + MINT_SEND_ADDR)
	print("mint地址：" + MINT_ADDR)
	print("可能的下一个nonce:" + str(mint_nonce))
	print("fee(high)：" + str(MINT_FEE_HIGH) + ", fee(low)：" + str(MINT_FEE_LOW))
	
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
				print("------------------------------------------------")
				bef_time = now
				
				if stacks_block_height > 0 and stacks_block_height < MINT_END_HEIGHT:
					mint_fee = MINT_FEE_LOW
					if mint_flag == 0:
						mint_fee = MINT_FEE_HIGH
					cmd = "stx send_tokens " + MINT_SEND_ADDR + " 1 " + str(mint_fee) + " " + str(mint_nonce) + " \"" + MINT_KEY + "\" \"" + str(stacks_block_height + 2) + ".stxmap\""
					print("[CMD]\t" + cmd)
					#os.system(cmd)
					mint_nonce += 1
					mint_flag = 1
			
			stacks_block_height_now = int(get_stacks_block_height()) 
			if stacks_block_height_now != 0 and stacks_block_height != stacks_block_height_now:
				stacks_block_height = stacks_block_height_now
				now = datetime.now()
				now_str = now.strftime("%Y-%m-%d %H:%M:%S")
				print("------------------------------------------------")
				print("$ <Stxmap> mint_number - block_height: " + str(stacks_block_height + 2) + " - " + str(stacks_block_height_now) + " (" + now_str + ")\n\n")
				
				mint_flag = 0

		except Exception:
			time.sleep(5)

		time.sleep(5)

def main():
	mint_stxmap()

# 主函数
if __name__=="__main__":
	main()
