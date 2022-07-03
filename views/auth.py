from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_services

auth_ns = Namespace("auth")


@auth_ns.route("/")
class AuthView(Resource):
	def post(self):
		req_json = request.json
		username = req_json.get("username")
		password = req_json.get("password")

		if not (username or password):
			return "Необходимо указать имя пользователя и пароль!", 400

		try:
			return auth_services.generate_tokens(username, password)
		except Exception:
			return "", 400

	def put(self):
		req_json = request.json
		ref_token = req_json.get("refresh_token")
		if not ref_token:
			return "Не был задан токен!", 400

		tokens = auth_services.approve_refresh_token(ref_token)

		if tokens:
			return tokens
		else:
			return "Ошибка при запросе!", 400

