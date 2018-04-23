import numpy as np
from transforms3d import euler
import scipy as sp

class Rocket(object):
	"""
		params:
			position - 	Euler angles of joint coordinate system and start system
				Example: numpy.array([0,0,numpy.pi/2])
			omega - 	the angular velocity
				Example: numpy.array([0,0,0])
		
	"""
	def __init__(self, engines, stages):
		super(Rocket, self).__init__()
		self.engines = engines
		self.stages = stages
		self.recalcRcm()
		self.clock = Sensor(0)

	def getRcm(self):
		return self.Rcm

	def recalcRcm(self):
		self.Rcm = np.array([s.getMass()*(s.R + s.getRcm()) for s in self.stages]).sum(axis=0)/np.array([s.getMass() for s in self.stages]).sum(axis=0)


	def getThrust(self):
		return np.array([e.getThrust() for e in self.engines]).sum(axis=0)

	def getMoment(self):
		return np.array([s.getMoment(self.Rcm) for s in self.stages]).sum(axis=0)

	def getMass(self):
		return np.array([s.getMass() for s in self.stages]).sum(axis=0)

	def getInertia(self):
		#return np.array([[1, 0, 0],[0, 100, 0],[0, 0, 100]])
		return np.array([10, 100, 100])

	def tick(self, dt):
		self.clock.setValue(self.clock.getValue() + dt)
		self.flightController()
		[s.tick(dt) for s in self.stages]
		self.recalcRcm()

	def flightController(self):
		return

class Sensor(object):
	"""docstring for Sensor"""
	def __init__(self, inital_value):
		super(Sensor, self).__init__()
		self.value = inital_value

	def getValue(self):
		return self.value

	def setValue(self, new_value):
		self.value = new_value
		
		

class Stage(object):
	

	def __init__(self, construction, tanks, engines, R):
		super(Stage, self).__init__()

		self.construction = construction
		self.tanks = tanks
		self.engines = engines
		self.R = R

		self.recalcRcm()

	def getMass(self):
		return np.array([c.mass for c in self.construction]).sum(axis=0) + np.array([t.getMass() for t in self.tanks]).sum(axis=0)

	def recalcRcm(self):
		if (self.getMass() == 0):
			self.Rcm = np.array([0,0,0])
		else:
			self.Rcm = ( np.array([c.mass*c.Rcm for c in self.construction]).sum(axis=0) + np.array([t.getMass()*t.getRcm() for t in self.tanks]).sum(axis=0) ) / self.getMass()


	def getRcm(self):
		return self.Rcm

	def getThrust(self):
		return np.array([e.getThrust() for e in self.engines]).sum(axis=0)

	def getInertia(self):
		return self.I

	def getMoment(self, Rcm):
		return np.array([np.cross((e.R + self.R - Rcm), e.getThrust()) for e in self.engines]).sum(axis=0)

	def tick(self, dt):
		[e.tick(dt) for e in self.engines]
		self.recalcRcm()

	def separate(self):
		[c.separate() for c in self.construction]
		[c.separate() for c in self.tanks]
		[c.setThrottle(0) for c in self.engines]
		self.recalcRcm()


			
class SolidObject(object):
	"""docstring for SolidObject"""
	def __init__(self, mass, Rcm):
		super(SolidObject, self).__init__()
		self.mass = mass
		self.Rcm = Rcm

	def separate(self):
		self.mass = 0
		

		
class Tank(object):
	"""docstring for Tank"""
	def __init__(self, l, m0, R):
		super(Tank, self).__init__()
		self.l = l
		self.m0 = m0
		self.m = m0
		self.R = R
		self.recalcRcm()

	def getRcm(self):
		return self.Rcm

	def getMass(self):
		return self.m

	def tick(self, dm):
		if (self.m - dm) < 0:
			raise ValueError('Fuel tank is empty!')
		self.m = self.m - dm
		self.recalcRcm()

	def recalcRcm(self):
		self.Rcm = self.R + np.array([-self.l+self.l*self.m/(2*self.m0), 0, 0])

	def separate(self):
		self.m = 0
		self.recalcRcm()

class FuelLine(object):
	"""docstring for FuelLine"""
	def __init__(self, tank, ratio):
		super(FuelLine, self).__init__()
		self.tank = tank
		self.ratio = ratio
		

class Engine(object):

	def __init__(self, u, r, o, dmdt, fl):
		"""
			u - velocity of gas flow from the nozzle [m/s]
			r - X, Y, Z of nozzle relative to a stage reference system (RS)
			o - rotation matrix from engine RS to a stage RS
			dmdt - design fuel consumption dM/dt [kg/s]
		"""
		super(Engine, self).__init__()
		self.u = u
		self.R = r
		self.O = o
		self.dmdt = dmdt
		self.throttle = 0
		self.fl = fl
		self.fault = False
	
	def setThrottle(self, throttle):
		"""
			throttle - thrust throttle coefficient (0 - engine off, 1 - full thrust)
		"""
		self.throttle = throttle

	def getThrust(self):
		return self.O.dot(np.array([self.u*self.dmdt*self.throttle, 0, 0]))

	def getFuelConsumption(self):
		return self.dmdt*self.throttle

	def getPosition(self):
		return self.R

	def tick(self, dt):
		try:
			[component.tank.tick(self.getFuelConsumption()*dt*component.ratio) for component in self.fl]
		except Exception:
			self.setThrottle(0)
			self.fault = True