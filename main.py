from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import requests


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
	api_url = "https://api.vk.ru/method/utils.getLinkStats"
	key = urlparse(short_url).path.lstrip('/')
	params = {
		"key":key,
		"access_token": api_key,
		"interval": "forever",
		"v": "5.199",
	}
	response = requests.get(api_url, params=params)
	response.raise_for_status()
	data = response.json()

	if "error" in data:
		error_msg = data["error"]["error_msg"]
		raise requests.exceptions.HTTPError(error_msg)

	return  data["response"]["stats"][0]["views"]


def is_shorten_link(api_key, url):
	api_url = "https://api.vk.ru/method/utils.getLinkStats"
	key = urlparse(url).path.lstrip('/')
	params = {
		"key": key,
		"access_token": api_key,
		"v": "5.199",
	}

	response = requests.get(api_url, params=params)
	data = response.json()

	return "response" in data


def main():
	load_dotenv()
	user_url = input('Введите ссылку ')
	api_key = os.getenv('API_KEY')


	try:
		if is_shorten_link(api_key, user_url):
			clicks = count_clicks(api_key, user_url)
			print("Количество переходов:", clicks)
		else:
			short_link = shorten_link(api_key, user_url)
			print('Сокращенная ссылка:', short_link)

	except requests.exceptions.HTTPError as error:
		print('ошибка', error)


if __name__ == '__main__':
	main()
	
