from flask import Flask, render_template
import webview
from speed import *
import json
import threading

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/get_rate')
def get_rates():
	print(get_rate(transfer_rate))
	return json.dumps(get_rate(transfer_rate))

def start_server():
	app.run()

if __name__ == "__main__":
	t = threading.Thread(target=start_server)
	t.daemon = True
	t.start()
	#global window
	window = webview.create_window("Bandwidth consumption", "http://127.0.0.1:5000/", confirm_close=True)
	#sys.exit()
	webview.start()
	sys.exit()