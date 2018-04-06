import numpy as np
from transforms3d import euler


class FlightController(object):
	"""docstring for FlightController"""
	def __init__(self, arg):
		super(FlightController, self).__init__()
		self.arg = arg
		

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

	def getThrust(self):
		return np.array([e.getThrust() for e in self.engines]).sum(axis=0)

	def getMoment(self):
		return 0


class Engine(object):

	def __init__(self, u, r, o, dmdt, id):
		"""
			u - velocity of gas flow from the nozzle [m/s]
			r - X, Y, Z of nozzle relative to a stage reference system (RS)
			o - rotation matrix from engine RS to a stage RS
			dmdt - design fuel consumption dM/dt [kg/s]
			id - identity of the engine (required by the flight controller)
		"""
		super(Engine, self).__init__()
		self.u = u
		self.R = r
		self.O = o
		self.dmdt = dmdt
		self.id = id
		self.throttle = 0
	
	def setThrottle(self, throttle):
		"""
			throttle - thrust throttle coefficient (0 - engine off, 1 - full thrust)
		"""
		self.throttle = throttle

	def getThrust(self):
		return self.O.dot(np.array([self.u*self.dmdt, 0, 0]))

	def getFuelConsumption(self):
		return self.dmdt*self.throttle


	def getPosition(self):
		return self.R

	"""	
	def Momentum(self, dmdt, cm_vector):
		
		#	cm_vector - X, Y, Z of center of mass relative to the initial position
		
		return np.cross(self.Thrust(dmdt), self.params['position'] - cm_vector)
	"""