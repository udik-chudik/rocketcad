import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from ElectronRocket import Electron
from Physics import *
import copy

from scipy.integrate import ode

rock = Electron()

pos0 = euler.euler2mat(0, 0, np.pi/2, axes='sxyz')


ph = Physics(rock, -9.8, 6400000, np.array([0,6400000,0]), np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]), pos0)

r = ode(ph.dynamics6d).set_integrator('vode', method='bdf')

f = np.array([0,6400000,0, 0, 0, 0, 0, 0, 0, 0, 0, -0.0044])
r.set_initial_value(f, 0)

tMax = 3600*2
dt = 1

sol = []
times = []
while r.successful() and r.t < tMax:
	s = r.integrate(r.t+dt)
	sol.append([r.t, s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10],s[11]])
	#print(r.t+dt, r.integrate(r.t+dt))

	rock.tick(dt)

sol = np.array(sol)

np.save('solution', sol)

ax = plt.subplot(111, aspect=1)



ax.plot(sol[:,1], sol[:,2])

earth = mpatches.Circle((0, 0), 6400000, fc="g")
atmosphere = mpatches.Circle((0, 0), 6500000, facecolor='none', edgecolor='r', linestyle='--')
ax.add_patch(earth)
ax.add_patch(atmosphere)


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