from flask import Flask, render_template
import psutil
import json

app = Flask(__name__)

frequency = []
available = []
used = []

def get_size(bytes, suffix="B"):
	factor = 1024
	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f"{bytes:.2f}{unit}{suffix}"
		bytes /= factor

@app.route('/')
def index():
	svmem = psutil.virtual_memory()
	total = get_size(svmem.total)

	data = {
		"total":total
	}
	
	return render_template('index.html', **data)

@app.route('/cpu')
def cpu():
	cpufreq = psutil.cpu_freq()
	global frequency
	frequency.append(cpufreq.current)

	if len(frequency) > 10:
		frequency = frequency[1:10]

	return json.dumps(frequency)

@app.route('/ram_av')
def ram():
	svmem = psutil.virtual_memory()
	global available

	global used
	used.append(svmem.used)

	available.append(svmem.available)
	

	if len(available) > 100:
		available = available[1:100]

	if len(used) > 100:
		used = used[1:100]

	return json.dumps([available, used])

@app.route('/ram_us')
def ram_us():
	svmem = psutil.virtual_memory()
	global used
	used.append(get_size(svmem.used))

	if len(used) > 10:
		used = used[1:10]

	return json.dumps(used)

if __name__ == "__main__":
	app.run(debug=True)