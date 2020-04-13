import threading
from collections import deque
import time
import psutil

up_rate = []
down_rate = []

def calc_ul_dl(rate, dt=3, interface='wlp2s0'):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True)[interface]
    tot = (counter.bytes_sent, counter.bytes_recv)

    while True:
        last_tot = tot
        time.sleep(dt)
        counter = psutil.net_io_counters(pernic=True)[interface]
        t1 = time.time()
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [(now - last) / (t1 - t0) / 1000.0
                  for now, last in zip(tot, last_tot)]
        rate.append((ul, dl))
        t0 = time.time()


def print_rate(rate):
    try:
        print(f'UL: {rate[0][0]:.2f} kB/s / DL: {rate[-1][-1]:.2f} kB/s')
    except IndexError:
        'UL: - kB/s/ DL: - kB/s'

def get_rate(rate):
    try:
        up_rate.append(rate[0][0])
        down_rate.append(rate[-1][-1])
        return [up_rate, down_rate]
    except IndexError:
        return [0, 0]

# Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
transfer_rate = deque(maxlen=1)
t = threading.Thread(target=calc_ul_dl, args=(transfer_rate,))

# The program will exit if there are only daemonic threads left.
t.daemon = True
t.start()

# The rest of your program, emulated by me using a while True loop
# while True:
#     print_rate(transfer_rate)
#     time.sleep(2)