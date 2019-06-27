import paho.mqtt.client as mqtt
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from main import TOPIC

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# app.config['MQTT_BROKER_URL'] = 'm24.cloudmqtt.com'
# app.config['MQTT_BROKER_PORT'] = 14281
# app.config['MQTT_USERNAME'] = 'uwbfgkzz'
# app.config['MQTT_PASSWORD'] = '3rAA12jepUwD'
# app.config['MQTT_REFRESH_TIME'] = 1.0
socketio = SocketIO(app)

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the ESP8266.


def on_message(client, userdata, message):
    #socketio.emit('my variable')
    print("Received message '" + str(message.payload.decode("utf-8")) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))
    if message.topic == TOPIC:
        socketio.emit('dht_temperature', {
                      'data': message.payload.decode("utf-8")})


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set("uwbfgkzz", "3rAA12jepUwD")
mqttc.connect("m24.cloudmqtt.com", 14281, 60)
# mqttc.connect("localhost",1883,60)
mqttc.loop_start()


@app.route("/a")
def main1():
   # Pass the template data into the template main.html and return it to the user
   mqttc.publish(TOPIC,'1')
   return jsonify({'asd': 1})


@app.route("/b")
def main2():
   # Pass the template data into the template main.html and return it to the user
   mqttc.publish(TOPIC,'2')
   return jsonify({'asd': 2})


@app.route("/c")
def main3():
   # Pass the template data into the template main.html and return it to the user
   mqttc.publish(TOPIC,'3')
   return jsonify({'asd': 3})


@app.route("/d")
def main4():
   # Pass the template data into the template main.html and return it to the user
   mqttc.publish(TOPIC,'4')
   return jsonify({'asd': 4})


@app.route("/f")
def main5():
   # Pass the template data into the template main.html and return it to the user
   mqttc.publish(TOPIC,'5')
   return jsonify({'asd': 5})


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json data here: ' + str(json))


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8181, debug=True)