import numpy as np
from transforms3d import euler
from RocketComponents import *


class ElectronRocket(Rocket):
	
	def flightController(self):
		t = self.clock.getValue()
		engine1 = self.engines[0]
		engine2 = self.engines[1]

		stage1 = self.stages[0]

		if (t < 144):
			engine1.setThrottle(1)
		else:
			stage1.separate()
			engine2.setThrottle(1)

def Electron():

	#Initial position
	O = euler.euler2mat(0, 0, 0, axes='sxyz')

	stage1_construction = SolidObject(950, np.array([ -6.0, 0, 0 ]))

	tank1 = Tank(10, 9250, np.array([ -1, 0, 0 ]))

	fl1 = FuelLine(tank1, 1.0)

	eng1 = Engine(3000, np.array([ -12.1, 0, 0 ]), O, 64, [fl1])

	st1 = Stage([stage1_construction], [tank1], [eng1], np.array([-2.4,0,0]))


	stage2_construction = SolidObject(300, np.array([ -1.7, 0, 0 ]))

	tank2 = Tank(1.8, 2150, np.array([ -0.5, 0, 0 ]))
	fl2 = FuelLine(tank2, 1.0)

	eng2 = Engine(3300, np.array([ -2.4, 0, 0 ]), O, 7, [fl2])

	st2 = Stage([stage2_construction], [tank2], [eng2], np.array([0,0,0]))

	rock = ElectronRocket([eng1, eng2], [st1, st2])


	return rock

