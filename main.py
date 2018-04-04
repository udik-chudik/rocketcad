import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from transforms3d import euler
import matplotlib.patches as mpatches


omega = np.array([0,0,-0.0])
#omega = np.array([0,0,0])

F = np.array([9.8,0,0])
M = np.array([0,0,0.0])
Tburn = 10

Tsim = 4*Tburn
pressision = Tsim*10

#Cd = 0.1
#Cl = 0.001

def Cd(alpha):
	#print(alpha*180/np.pi)
	#return 0.1+0.01*alpha*180/np.pi if alpha < np.pi/4 else 0.1+0.45
	return 0.1 + 1*np.sin(2*alpha)

def Cl(alpha):
	#return 0.04*alpha*180/np.pi if alpha < np.pi/4 else 0.04*45
	return 0.8*np.sin(2*alpha)

rho = 1.29

Sd = 0.001
Sl = 0.0

S = 0.05

I = np.array([
	[1, 0, 0],
	[0, 100, 0],
	[0, 0, 100]
	])


Ipv = np.array([1,100,100])

Rf = np.array([-0.3, 0, 0])

Rt = np.array([-0.3, 0, 0])

R0 = 6400000
g0 = -9.81
m = 1

pos0 = euler.euler2mat(0, 0, np.pi/2, axes='sxyz')

def Thurst(y, t):
	thurst = np.array([0,0,0])

	if (t < Tburn):
		thurst = np.array([20, 1, 0])

	return thurst



def dynamics(y, t):

	X, Y, Z, Vx, Vy, Vz, gamma, psi, thetta, omega_x, omega_y, omega_z = y

	R2 = X**2 + Y**2 + Z**2
	R = np.sqrt(R2)

	V = np.array([Vx, Vy, Vz])
	rot2rocket = euler.euler2mat(gamma, psi, thetta, axes='sxyz')

	rot = pos0.dot(rot2rocket)

	V_scal = np.sqrt(Vx**2 + Vy**2 + Vz**2)

	#Xa = Cd*rho*Sd*(Vx**2 + Vy**2 + Vz**2)/2
	#Ya = Cl*rho*Sl*(Vx**2 + Vy**2 + Vz**2)/2
	
	cosAlpha = 1

	
	if (V_scal > 0):
		cosAlpha = Vx/V_scal
	
	sinAlpha = np.sqrt(1-cosAlpha**2)

	Alpha = np.arcsin(sinAlpha)

	Ra = np.array([
		-(1/2)*(Cd(Alpha)*cosAlpha - Cl(Alpha)*sinAlpha)*rho*S*V_scal**2,
		-(1/2)*(Cd(Alpha)*sinAlpha + Cl(Alpha)*cosAlpha)*rho*S*Vy*V_scal/sinAlpha if sinAlpha > 0 else 0,
		-(1/2)*(Cd(Alpha)*sinAlpha + Cl(Alpha)*cosAlpha)*rho*S*Vz*V_scal/sinAlpha if sinAlpha > 0 else 0
		])

	#print(sinAlpha)
	a = np.concatenate([
		rot.dot(V),
		
		Thurst(y, t)/m - np.cross(np.array([omega_x, omega_y, omega_z]), V)
		+ Ra/m
		+ g0*(R0**2/R2)*np.array([X/R, Y/R, Z/R]).dot(rot),
		
		np.array([omega_x, omega_y, omega_z]),
		
		M/Ipv - np.array([
			(Ipv[2] - Ipv[1])*omega_y*omega_z/Ipv[0],
			(Ipv[0] - Ipv[2])*omega_z*omega_x/Ipv[1],
			(Ipv[1] - Ipv[0])*omega_x*omega_y/Ipv[2]
			])
		+ np.cross(Rf, Ra)/Ipv
		+ np.cross(Rt, Thurst(y, t))/Ipv
		])

	return a

#- np.cross(omega, V)

y0 = [0,R0,0,0,0,0,0,0,0, omega[0], omega[1], omega[2]]

t = np.linspace(0,Tsim,pressision)

sol = integrate.odeint(dynamics, y0, t)

#plt.plot(sol[:, 0], sol[:, 1], 'r', label='trajectory')
#plt.plot(sol[:, 1], sol[:, 3], 'r', label='Vx')
#plt.plot(sol[:, 1], sol[:, 4], 'g', label='Vy')

#plt.plot(t, sol[:, 0], 'g', label='X')
#plt.plot(t, sol[:, 1], 'b', label='Y')

#filter(lambda x: x % 2, sol)

Toff = Tburn/(Tsim/pressision)
Toff = int(Toff)

ax = plt.subplot(111, aspect=1)
ax.plot(sol[0:Toff, 0], sol[0:Toff, 1], 'b', label='active')
ax.plot(sol[Toff-1:, 0], sol[Toff-1:, 1], 'r', label='passive')
earth = mpatches.Circle((0, 0), 6400000, fc="g")
atmosphere = mpatches.Circle((0, 0), 6500000, facecolor='none', edgecolor='r', linestyle='--')
#plt.legend()
ax.add_patch(earth)
ax.add_patch(atmosphere)

"""
plt.plot(t, sol[:, 11], 'g', label='omega')
plt.plot(t, sol[:, 8], 'r', label='thetta')
"""
plt.show()


"""
plt.legend(loc='best')
plt.xlabel('x')
plt.ylabel('y')
plt.grid()
plt.show()
"""