import numpy as np
from transforms3d import euler
from RocketComponents import *


class OurRocket(Rocket):
	
	def flightController(self):
		t = self.clock.getValue()
		engine = self.engines[0]

		if (t > 0 and t < 10 and not engine.fault and engine.throttle < 1):
			print("Engin ON")
			self.engines[0].setThrottle(1)
		else:

			self.engines[0].setThrottle(0)

def testRocket():


	O = euler.euler2mat(0, 0, 0, axes='sxyz')

	stage_construction = SolidObject(300, np.array([ -1.1, 0, 0 ]))

	tank1 = Tank(2, 1000, np.array([ -0.1, 0, 0 ]))

	fl1 = FuelLine(tank1, 1)

	eng1 = Engine(3000, np.array([ -1.2, 0, 0 ]), O, 20, [fl1])

	st = Stage([stage_construction], [tank1], [eng1], np.array([0,0,0]))

	rock = OurRocket([eng1], [st])


	return rock

