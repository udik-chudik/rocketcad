import numpy as np
from transforms3d import euler


class Rocket(object):
	"""
		params:
			position - 	Euler angles of joint coordinate system and start system
				Example: numpy.array([0,0,numpy.pi/2])
			omega - 	the angular velocity
				Example: numpy.array([0,0,0])
		
	"""
	def __init__(self, arg):
		super(Rocket, self).__init__()
		self.params = arg
		

class Stage(object):
	
	def __init__(self, Mc, Mf, engines, CM, I):
		super(Stage, self).__init__()
		self.Mc = Mc
		self.Mf = Mf
		self.engines = engines
		self.CM = CM
		self.I = I

	def getMass(self):
		return self.Mf + self.Mc

	def getInertia(self):
		return self.I

	def getRcm(self):
		return self.CM

	def getThrust(self, dmdt):
		return np.array([e.getThrust(dmdt) for e in self.engines]).sum(axis=0)

	def getMoment(self):
		return 0


class Engine(object):

	def __init__(self, u, r, o):
		super(Engine, self).__init__()
		self.u = u
		self.R = r
		self.O = o
		
	def getThrust(self, dmdt):
		return self.O.dot(np.array([self.u*dmdt, 0, 0]))

		#return self.u*dmdt
		"""
		return euler.euler2mat(self.params['direction'][0],
			self.params['direction'][1],
			self.params['direction'][2], axes='sxyz').dot(np.array([self.params['u']*dmdt, 0, 0]))
		"""
	"""	
	def Momentum(self, dmdt, cm_vector):
		
		#	cm_vector - X, Y, Z of center of mass relative to the initial position
		
		return np.cross(self.Thrust(dmdt), self.params['position'] - cm_vector)
	"""