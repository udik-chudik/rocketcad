import numpy as np
from transforms3d import euler
from RocketComponents import *


class ElectronRocket(Rocket):
	done = False
	def flightController(self):
		t = self.clock.getValue()
		engine1 = self.engines[0]
		engine2 = self.engines[1]

		stage1 = self.stages[0]

		if (t < 153):
			if engine1.throttle != 1 and not engine1.fault:
				engine1.setThrottle(1)
				print("Engine 1 started.")
			elif engine1.fault:
				print("Engine 1 fault detected", t)
		else:
			if not stage1.is_separated:
				stage1.separate()
				print("The first stage has been separated.")
			if engine2.throttle != 1 and not engine2.fault and not self.done:
				engine2.setThrottle(1)
				print("Engine 2 started.")
			elif engine2.fault and not self.done:
				print("Engine 2 fault detected", t)
				self.done = True
				print("Assumed done.")


def Electron():

	#Initial position
	O = euler.euler2mat(0, 0, 0, axes='sxyz')

	stage1_construction = SolidObject(950 + 50, np.array([ -6.0, 0, 0 ]))

	tank1 = Tank(10, 9250, np.array([ -1, 0, 0 ]))

	fl1 = FuelLine(tank1, 1.0)

	eng1 = Engine(3030, np.array([ -12.1, 0, 0 ]), O, 61, [fl1])

	st1 = Stage([stage1_construction], [tank1], [eng1], np.array([-2.4,0,0]))


	stage2_construction = SolidObject(250 + 50, np.array([ -1.7, 0, 0 ]))

	tank2 = Tank(1.8, 2150, np.array([ -0.5, 0, 0 ]))
	fl2 = FuelLine(tank2, 1.0)

	eng2 = Engine(3330, np.array([ -2.4, 0, 0 ]), O, 6.6, [fl2])

	st2 = Stage([stage2_construction], [tank2], [eng2], np.array([0,0,0]))

	rock = ElectronRocket([eng1, eng2], [st1, st2])


	return rock

