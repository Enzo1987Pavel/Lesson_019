import jwt
from flask import request, abort

from constants import JWT_SECRET, JWT_ALGORITHM


def auth_required(func):
	def wrapper(*args, **kwarags):

		if not "Authorization" in request.headers:
			abort(401)

		data = request.headers["Authorization"]  # Получаем заголовок 'Authorization'
		token = data.split("Bearer ")[-1]  # Делим по строке 'Bearer ' и забираем последнее значение

		try:
			jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
		except Exception as e:
			print(f"JWT decode error: {e}")
			abort(401)

		return func(*args, **kwarags)
	return wrapper


def admin_required(func):
	def wrapper(*args, **kwarags):

		if not "Authorization" in request.headers:
			abort(401)

		data = request.headers["Authorization"]  # Получаем заголовок 'Authorization'
		token = data.split("Bearer ")[-1]  # Делим по строке 'Bearer ' и забираем последнее значение

		try:
			data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
		except Exception as e:
			print(f"JWT decode error: {e}")
			abort(401)
		else:
			if data["role"] == "admin":
				return func(*args, **kwarags)
		abort(403)
	return wrapper
