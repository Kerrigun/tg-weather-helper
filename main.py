import telebot

from pyowm import OWM
from pyowm.utils.config import get_default_config

import random

bot = telebot.TeleBot('The token of your bot')

@bot.message_handler(commands=['start'])
def welcome_in_the_bot(message):
	bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.first_name}!\n'
										f'Я - Weather Helper, чтобы узнать прогноз погоды\n'
										f'введите название города в чат!\n'
									  	f'/start - начать взаимодействие с ботом\n'
									  	f'/help - узнать все доступные команды бота\n'
									  	f'/credits - автор бота/контакты'
					 )

@bot.message_handler(commands=['help'])
def help_command_bot(message):
	bot.send_message(message.chat.id,
					 f'Список доступных команд:\n'
					 f'/start - начать взаимодействие с ботом\n'
					 f'/help - позволяет узнать все доступные команды бота\n'
					 f'/credits - автор бота/контакты'
					 )

@bot.message_handler(commands=['credits'])
def credits_bot(message):
	bot.send_message(message.chat.id,
					 f'Автор - illum1na\n'
					 f'ВК - https://vk.com/illum1na\n'
					 f'TG - @juzzytop1gg\n'
					 f'Почта - dranikmister@gmail.com'
					 )

@bot.message_handler(content_types=['text'])
def weather_center_bot(message):
	try:
		place = message.text

		config_dict = get_default_config()
		config_dict['language'] = 'ru'

		owm = OWM('c52242b2d4d80ae028d6e97b46ce1c39', config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather

		t = w.temperature("celsius")
		temp = t['temp']
		feels_like = t['feels_like']
		temp_max= t['temp_max']
		temp_min = t['temp_min']

		wi = w.wind()['speed']
		humi = w.humidity
		cl = w.clouds
		st = w.status
		dt = w.detailed_status
		ti = w.reference_time('iso')
		pr = w.pressure['press']
		vd = w.visibility_distance

		bot.send_message(message.chat.id,
				f'Температура в городе {place} равна {temp} °C\n'
				f'Максимальная температура: {temp_max} °C\n'
				f'Минимальная температура: {temp_min} °C\n'
				f'Ощущается как: {feels_like} °C\n'
				f'Скорость ветра: {wi} м/с\n'
				f'Давление: {pr} мм.рт.ст\n'
				f'Влажность: {humi} %\n'
				f'Видимость: {vd} метров\n'
				f'Сейчас на улице: {dt}'
				)

	except:
		variations = [
			f'Прости, {message.from_user.first_name}, я не понимаю того, что ты пытаешься сказать!',
			f'Извиняюсь, но Вы, случайно, городом не ошиблись?',
			f'Пожалуйста, попытайтесь снова...',
			f'Я не понимаю твоих слов!',
			f'Так, {message.from_user.first_name}, Вы уверены в том, что говорите?',
			f'Это явно неправильная формулировка, подумайте чуточку лучше...',
			f'Введите адекватное название города!',
			f'Я не понимаю Вас...',
			f'Я не понимаю твоих слов, {message.from_user.first_name}!'
		]
		sends = random.choice(variations)
		bot.send_message(message.chat.id, f'{sends}')

bot.polling(none_stop=True, interval=0)