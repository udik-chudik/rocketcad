import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import sys

sol = np.load('solution.npy')

ax = plt.subplot(111, aspect=1)

if (len(sys.argv) == 1):

	ax.plot(sol[:,1], sol[:,2])

	earth = mpatches.Circle((0, 0), 6400000, fc="g")
	atmosphere = mpatches.Circle((0, 0), 6500000, facecolor='none', edgecolor='r', linestyle='--')
	ax.add_patch(earth)
	ax.add_patch(atmosphere)
	plt.show()


elif (sys.argv[1] == 'V'):

	ax.plot(sol[:,0], np.sqrt(sol[:,4]**2 + sol[:,5]**2 + sol[:,6]**2))
	plt.show()

elif (sys.argv[1] == 'M'):

	ax.plot(sol[:,0], sol[:,13])
	plt.show()

elif (sys.argv[1] == 'H'):

	ax.plot(sol[:,0], (np.sqrt(sol[:,1]**2 + sol[:,2]**2 + sol[:,3]**2) - 6400000)/1000)
	plt.show()

elif (sys.argv[1] == 'Rcm'):

	ax.plot(sol[:,0]/100, sol[:,14])
	plt.show()