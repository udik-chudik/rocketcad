import matplotlib.pyplot as plt
from testRocket import testRocket
from Physics import *
import copy

from scipy.integrate import ode

rock = testRocket()

pos0 = euler.euler2mat(0, 0, np.pi/2, axes='sxyz')


ph = Physics(rock, -9.8, 6400000, np.array([0,6400000,0]), np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]), pos0)

r = ode(ph.dynamics6d).set_integrator('vode', method='bdf')

f = np.array([0,6400000,0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
r.set_initial_value(f, 0)

tMax = 35
dt = 0.01

sol = []
times = []
while r.successful() and r.t < tMax:
	times.append(r.t)
	s = r.integrate(r.t+dt)
	sol.append([s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10],s[11]])
	#print(r.t+dt, r.integrate(r.t+dt))

	rock.tick(dt)

sol = np.array(sol)

plt.plot(sol[:,0], sol[:,1])
plt.show()

"""


tMax = 1
dt = 0.1

t = 0

times = []

f = np.array([0,6400000,0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

data = np.array([f])


while t < tMax:

	rock.tick(dt)

	delta = ph.dynamics6d(f)


	f = f + copy.copy(delta*dt)

	t = t + dt

	times.append(t)
	data = np.append(data, f)

print(data)
"""
#plt.plot(times, data[0,:])
#plt.show()