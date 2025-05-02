from flask import jsonify
from jose import jwt
import requests
import os
from constants import BASE_URL,API_KEY,fetch_weather
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
ALGORITHMS = ["RS256"]

def verify_token(token):
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    unverified_header = jwt.get_unverified_header(token)
    print(unverified_header)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if not rsa_key:
        raise Exception("RSA key not found")
    payload = jwt.decode(
        token,
        rsa_key,
        algorithms=ALGORITHMS,
        audience=API_AUDIENCE,
        issuer=f"https://{AUTH0_DOMAIN}/"
    )
    return payload

def get_weather(token, city):
    try:
        verify_token(token)

        weather_data, status_code, message = fetch_weather(city)
        if status_code != 200:
            return jsonify({"error": message}), status_code

        return jsonify({
            "city": weather_data["city"],
            "temperature": f"{weather_data['temperature']}°C",
            "humidity": f"{weather_data['humidity']}%",
            "wind": f"{weather_data['wind']} km/h"
})

    except Exception as e:
        return jsonify({"error": str(e)}), 401

def post_weather(token, data):
    try:
        verify_token(token)
        
        city = data.get("city")
        if not city:
            return jsonify({"error": "City name is required"}), 400

        weather_data, status_code, message = fetch_weather(city)
        if status_code != 200:
            return jsonify({"error": message}), status_code

        return jsonify({
            "city": weather_data["city"],
            "temperature": f"{weather_data['temperature']}°C",
            "humidity": f"{weather_data['humidity']}%",
            "wind": f"{weather_data['wind']} km/h"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 401

