import calendar
import datetime

from constants import JWT_SECRET, JWT_ALGORITHM

import jwt

from service.user import UserService


class AuthService:
	def __init__(self, user_service: UserService):
		self.user_service = user_service

	def generate_tokens(self, username, password, is_refresh=True):
		user = self.user_service.get_by_username(username)

		if not user:
			raise Exception("Не задан пользователь!")

		if not is_refresh:
			if not self.user_service.compare_passwords(password, user.password):
				raise Exception("Введен неверный пароль!")

		data = {
			"username": user.username,
			"role": user.role
		}

		# Задание времени жизни токена - 30 минут
		min_30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
		data["expires"] = calendar.timegm(min_30.timetuple())
		access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

		# Задание времени обновления токена - 30 дней
		day_30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
		data["expires"] = calendar.timegm(day_30.timetuple())
		refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

		return {"access_token": access_token, "refresh_token": refresh_token}

	def approve_refresh_token(self, refresh_token):
		data = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
		username = data["username"]
		user = self.user_service.get_by_username(username)

		if not user:
			# raise Exception("Пользователя с таким именем не существует!")
			raise Exception("Данного токена не существует!")

		now = calendar.timegm(datetime.datetime.utcnow().timetuple())
		exp_token = data["expires"]

		if now > exp_token:
			return "Время существования токена истекло!"

		return self.generate_tokens(username, user.password, is_refresh=True)
