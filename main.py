import os
from dotenv import load_dotenv
import requests
load_dotenv()


def shorten_link(api_key, api_url, user_url):
	
	params = {
		"url": user_url,
		"access_token": api_key,
		"v": "5.199",
	}
	
	response = requests.get(api_url, params=params)
	response.raise_for_status()
	short_url = response.json()
	short = short_url["response"]["short_url"]
	return short


def main():

	user_url = input('Введите ссылку ')
	api_key = os.getenv('API_KEY')
	api_url = 'https://api.vk.ru/method/utils.getShortLink'
	print('Сокращенная ссылка:', shorten_link(api_key, api_url, user_url))
	
	try:
		short = shorten_link(api_key, api_url, user_url)
	except :
		print('ошибка')



if __name__ == '__main__':
	main()
	