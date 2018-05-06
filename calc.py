from ElectronRocket import Electron
from Physics import *
import numpy as np
from scipy.integrate import ode

rock = Electron()

pos0 = euler.euler2mat(0, 0, np.pi/2, axes='sxyz')


ph = Physics(rock, -9.8, 6400000, np.array([0,6400000,0]), np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]), pos0)

r = ode(ph.dynamics6d).set_integrator('vode', method='bdf')

f = np.array([0,6400000,0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
r.set_initial_value(f, 0)

tMax = 3600
dt = 1

sol = []
times = []
while r.successful() and r.t < tMax:
	s = r.integrate(r.t+dt)
	sol.append([r.t, s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10],s[11], rock.getMass(), rock.getRcm()[0]])

	rock.tick(dt, np.array([s[3], s[4], s[5]]), np.array([s[9], s[10], s[11]]))

sol = np.array(sol)

np.save('solution', sol)
