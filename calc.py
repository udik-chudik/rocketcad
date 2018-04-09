import matplotlib.pyplot as plt
from testRocket import testRocket

rock = testRocket()

tMax = 150
dt = 1

t = 0

times = []
data = []

while t < tMax:
	rock.tick(dt)
	t = t + dt
	times.append(t)
	data.append(rock.getMoment())

plt.plot(times, data)
plt.show()