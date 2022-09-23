# Raul Jimenez 19017
# Donaldo Garcia 19683

# %%
import random
import math

"""
	Give a VA expotential distribution
		labdaa: rate of the distribution
"""
def exponential(lambdaa):
	return - (1/lambdaa) * math.log(random.random())

"""
	Give a VA exponential  poisson distribution
		last: last time
		lambdaa: lambda
"""
def Poisson(last, lambdaa):
	return last - (1/lambdaa) * math.log(random.random())

"""
	Simulate of a single server
		rate: rate of arrivals
		time: time of simulation
		name: name of the server
""" 
def server(rate, time, name):
	T = time
	t = 0 # time of simulation in seconds
	Na = 0 # number of arrivals in time t
	Nd = 0 # number of departures in time t
	n = 0 # number of customers in the system

	A = [] # list of arrivals
	D = [] # list of departures

	ta = 0
	td = 0
	tp = 0

	while t < T:
		if ta <= td and ta <= T:
			t = ta # time of next event
			Na += 1 # number of arrivals
			n += 1 # number of customers in the system
			ta = Poisson(t, rate) # time of next arrival
			if n == 1:
				y = exponential(rate)
				td = t + y # time of next departure
			A.append(t) # arrival time
		elif td < ta and td <= T:
			t = td # time of next event
			n -= 1 # number of customers in the system
			Nd += 1 # number of departures
			if n == 0:
				td = float('inf') # time of next departure
			else:
				y = exponential(rate)
				td = t + y # time of next departure
			D.append(t) # departure time
		elif min(ta, td) > T and n > 0:
			t = td # time of next event
			n -= 1 # number of customers in the system
			Nd += 1 # number of departures
			if n > 0:
				y = exponential(rate)
				td = t + y # time of next departure
				t = td
			D.append(t) # departure time
		elif min(ta, td) > T and n == 0:
			tp = max(t - T, 0)
			break
	print(f'===== RESULTADO DEL SERVIDOR {name} =====')
	print(f'Numero de llegadas: {Na}')
	print(f'El tiempo que estuvo el servidor ocupado fue: {td}')
	print(f'El tiempo que estuvo libre el servidor fue de {td - ta}')
	print(f'Las solicitudes estuvieron en total {D[-1]}')
	print(f'En promedio, cada solicitud estuvo en cola {Na/T}')
	# obtengo el promedio de A y D y los guardo en una variable
	# para despues calcular el tiempo promedio de espera
	# en la cola
	aprom = sum(A)/len(A)
	dprom = sum(D)/len(D)
	print(f'En promedio, hubieron {abs(dprom - aprom)} solicidted en cola cada segundo')
	print(f'El momento de salida de la ultima solicitud fue {D[-1]}')

"""
	Simultate multi server
		time : time of simulation
		num_servers: number of servers
		speed: speed of the servers
"""
def multi_server(time, num_server, speed):
	T = time
	t = 0 # time of simulation in seconds
	Na = 0 # number of arrivals in time t
	Nd = 0 # number of departures in time t
	n = 0 # number of customers in the system

	A = [] # list of arrivals
	D = [] # list of departures
	S = [] # list of servers

	ta = exponential(speed)
	td = [100000]*num_server 
	tp = 0

	ps = [0]*num_server # process servers
	ss = [0]*(1 + num_server) # server solution

	while t < T or ss[0] > 0:
		m = min(td)
		minimun = td.index(m)
		if ta > td[minimun] and ta < T: # last arrival before close and still have time
			t = ta # time of next event
			Na += 1 # number of arrivals
			ta = ta + exponential(speed) # time of next arrival
			A.append(t) # arrival time

			if ss[0] == 0: # if there are no customers in the system
				S.append(t) # time of arrival to the server
				ss[0] += 1 # number of customers in the system
				ss[1] = Na # number of arrival to the server
				td[0] = t + exponential(speed) # time of next departure
			elif ss[0] < num_server: # if there are customers in the system but not all servers are busy
				not_busy = ss.index(0) - 1 # get the first server not busy
				S.append(t) # time of arrival to the server
				ss[0] += 1 # number of customers in the system
				ss[not_busy + 1] = Na # number of arrival to the server
				td[not_busy] = t + exponential(speed) # time of next departure
			else: # if all servers are busy
				ss[0] += 1 # number of customers in the system
		else: # if the next event is a departure
			t = td[minimun] # time of next event
			ps[minimun] += 1 # number of departures
			D.append(t)	# departure time

			if ss[0] <= num_server: # if there are still aviailable servers
				ss[0] -= 1 # number of customers in the system
				td[minimun] = 100000 # time of next departure
				ss[minimun + 1] = 0 # remove the customer from the server
			else: # if there are no available servers
				ss[0] *= -1 # number of customers in the system
				nextt = max(ss) + 1 # get the next customer in the queue
				ss[0] *= -1 # number of customers in the system
				S.apend(t) # time of arrival to the server
				ss[0] -= 1 # remove the customer from the queue
				td[minimun] = t + exponential(speed) # time of next departure
				ss[minimun + 1] = nextt # number of arrival to the server
	# print results
	print(f'===== RESULTADO DEL SERVIDOR MULTIPLE =====')
	print(f'Numero de llegadas: {Na}')
	for i in range(num_server):
		print(f'EL servidor {i + 1} tuvo {ps[i]} departures')
	print(f'El tiempo que estuvo el servidor ocupado fue: {sum(td)}')
	print(f'El tiempo que estuvo libre el servidor fue de {sum(td) - ta}')
	print(f'Las solicitudes estuvieron en total {D[-1]}')
	print(f'En promedio, cada solicitud estuvo en cola {Na/T}')
	total = 0
	for i in range(len(A)):
		diference = S[i] - A[i]
		total += diference
	if len(A) > 0:
		average = total/len(A)
	else:
		average = total
	print(f'En promedio, el tiempo en cola fue de {average}')

# %%
server(100/60, 3600, 'Mountain Mega Computers')
print()
multi_server(3600, 250, 1/6)
# %%
