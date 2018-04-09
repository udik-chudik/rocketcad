import numpy as np
from transforms3d import euler
from RocketComponents import *

def testRocket():


	O = euler.euler2mat(0, 0, 0.1, axes='sxyz')

	stage_construction = SolidObject(300, np.array([ -1.1, 0, 0 ]))

	tank1 = Tank(2, 1000, np.array([ -0.1, 0, 0 ]))

	fl1 = FuelLine(tank1, 1)

	eng1 = Engine(3000, np.array([ -1.2, 0, 0 ]), O, 10, [fl1])

	st = Stage([stage_construction], [tank1], [eng1], np.array([0,0,0]))

	rock = Rocket([eng1], [st])

	return rock

