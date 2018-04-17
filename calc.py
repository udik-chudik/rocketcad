import matplotlib.pyplot as plt
from testRocket import testRocket
from Physics import *
import copy

rock = testRocket()

pos0 = euler.euler2mat(0, 0, np.pi/2, axes='sxyz')


ph = Physics(rock, -9.8, 6400000, np.array([0,6400000,0]), np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]), pos0)




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

#plt.plot(times, data[0,:])
#plt.show()