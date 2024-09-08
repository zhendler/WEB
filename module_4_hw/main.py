from flask import Flask, render_template, request, redirect, url_for
import socket
import threading
import json
from datetime import datetime


app = Flask(__name__)

app.static_folder = 'static'


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/message', methods=['GET', 'POST'])
def massage():
	if request.method == 'POST':
		username = request.form['username']
		message = request.form['message']


		send_to_socket(username, message)
		return redirect(url_for('index'))
	return render_template('message.html')

@app.errorhandler(404)
def not_found(e):
	return render_template('error.html'), 404



def send_to_socket(username, message):
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('localhost', 5000)
	data = json.dumps({"username": username, "message": message})
	sock.sendto(data.encode(), server_address)


def socket_server():
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('localhost', 5000))

	while True:
		data, _ = sock.recvfrom(1024)
		message_data = json.loads(data.decode())

		timestamp =str(datetime.now())
		with open ('storage/data.json', 'a') as f:
			current_data = {timestamp: message_data}
			json.dump(current_data, f, indent=4)


def run_flask():
	app.run(port=3000)


def run_socket_server():
	threading.Thread(target=socket_server).start()

if __name__ == '__main__':
	run_socket_server()
	run_flask()
