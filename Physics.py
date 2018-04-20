import numpy as np
from transforms3d import euler


class Physics(object):
	"""docstring for Physics"""
	def __init__(self, rocket, g0, R0, Radius, Velocity, Angles, AngularVelocities, pos):
		super(Physics, self).__init__()
		self.rocket = rocket
		self.g0 = g0
		self.R0 = R0
		self.Radius = Radius
		self.Velocity = Velocity
		self.Angles = Angles,
		self.AngularVelocities = AngularVelocities
		self.pos = pos

		



	def dynamics6d(self, t, f):


		X, Y, Z, Vx, Vy, Vz, gamma, psi, thetta, omega_x, omega_y, omega_z = f


		R2 = X**2 + Y**2 + Z**2
		R = np.sqrt(R2)

		V = np.array([Vx, Vy, Vz])

		rot2rocket = euler.euler2mat(gamma, psi, thetta, axes='sxyz')

		rot = self.pos.dot(rot2rocket)


		Ipv = self.rocket.getInertia()


		a = np.concatenate([
			rot.dot(V),
			
			self.rocket.getThrust()/self.rocket.getMass() - np.cross(np.array([omega_x, omega_y, omega_z]), V)
			+ self.g0*(self.R0**2/R2)*np.array([X/R, Y/R, Z/R]).dot(rot),
			
			np.array([omega_x, omega_y, omega_z]),
			
			self.rocket.getMoment()/Ipv - np.array([
				(Ipv[2] - Ipv[1])*omega_y*omega_z/Ipv[0],
				(Ipv[0] - Ipv[2])*omega_z*omega_x/Ipv[1],
				(Ipv[1] - Ipv[0])*omega_x*omega_y/Ipv[2]
				])
			])

		#print(a)


		return a