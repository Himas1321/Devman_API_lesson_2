from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import requests
load_dotenv()


def shorten_link(api_key, user_url):
	api_url = "https://api.vk.ru/method/utils.getShortLink"
	params = {
		"url": user_url,
		"access_token": api_key,
		"v": "5.199",
	}
	
	response = requests.get(api_url, params=params)
	response.raise_for_status()
	data = response.json()

	if "error" in data:
		error_msg = data["error"]["error_msg"]
		raise requests.exceptions.HTTPError(error_msg)
	

	return data["response"]["short_url"]


def count_clicks(api_key, short_url):
	api_url = "https://dev.vk.ru/ru/method/utils.getLinkStats"
	key = urlparse(short_url).path.lstrip('/')
	params = {
		"key":key,
		"access_token": api_key,
		"interval": "forever",
		"extended": "0",
		"v": "5.199",
	}
	
	response = requests.get(api_url, params=params)
	response.raise_for_status()

	data = response.json()

	if "error" in data:
		error_msg = data["error"]["error_msg"]
		raise requests.exceptions.HTTPError(error_msg)
	print(data)

	return data["response"]["views"]


def main():

	user_url = input('Введите ссылку ')
	api_key = os.getenv('API_KEY')

	
	
	try:
		short_link = shorten_link(api_key, user_url)
		print('Сокращенная ссылка:', short_link)

		clicks = count_clicks(api_key, short_link)
		print("Количество переходов:", clicks)

	except requests.exceptions.HTTPError as e:
		print('ошибка', e)



if __name__ == '__main__':
	main()
