from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from twilio.rest import Client
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)


OWM_API_KEY = "3c5d5b62d7bf81aa8a89c8b35864def5"


TWILIO_SID = "AC632871da8bee40442a2f7ddf68032556"
TWILIO_AUTH = "aed0c5e3ceec71dd6cadca290e3ff516"
TWILIO_NUMBER = "whatsapp:+14155238886"  

client = Client(TWILIO_SID, TWILIO_AUTH)


def get_weather(city):
  
    w_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric"
    w = requests.get(w_url).json()
    if "main" not in w:
        return None

   
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OWM_API_KEY}"
    geo = requests.get(geo_url).json()
    if not geo:
        return None
    lat, lon = geo[0]["lat"], geo[0]["lon"]

    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OWM_API_KEY}"
    aqi_data = requests.get(aqi_url).json()
    aqi_val = aqi_data["list"][0]["main"]["aqi"]
    pm25 = aqi_data["list"][0]["components"]["pm2_5"]

    timezone_offset = w["timezone"]
    local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
    formatted_time = local_time.strftime("%I:%M %p • %d %b %Y")

    data = {
        "city": city,
        "temperature": w["main"]["temp"],
        "condition": w["weather"][0]["description"].title(),
        "humidity": w["main"]["humidity"],
        "wind": w["wind"]["speed"],
        "aqi": aqi_val,
        "pm2_5": pm25,
        "local_time": formatted_time
    }
    return data


def send_whatsapp(mobile, message):
    mobile = "whatsapp:+" + mobile
    msg = client.messages.create(
        from_=TWILIO_NUMBER,
        to=mobile,
        body=message
    )
    return msg.sid
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    mobile = data.get("mobile")
    city = data.get("city")

    if not all([name, age, mobile, city]):
        return jsonify({"error": "All fields are required"}), 400

    weather = get_weather(city)
    if not weather:
        return jsonify({"error": "City not found"}), 400

    message = f"""
🌤️ *Prakritik Weather & AQI Alert*

Hello {name} 👋

📍 City: {city}
🕒 Time: {weather['local_time']}
🌡️ Temperature: {weather['temperature']}°C
🌦️ Condition: {weather['condition']}
💧 Humidity: {weather['humidity']}%
💨 Wind: {weather['wind']} m/s
🌫️ AQI: {weather['aqi']}
PM2.5: {weather['pm2_5']}

Stay safe & updated!
— Prakritik Team
"""

    send_whatsapp(mobile, message)
    return jsonify({"message": "WhatsApp alert sent successfully!", "weather": weather}), 201

# --------------------------
# Start Server
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
