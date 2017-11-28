# -*- coding: utf-8 -*-
"""
Demonstrates use of GLScatterPlotItem with rapidly-updating plots.

"""
import sys,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

import pyqtgraph as pg
import numpy as np



class simulator(QtCore.QObject):
	newData  = QtCore.pyqtSignal(object)

	def __init__(self):
		super(simulator, self).__init__()
		self.T = 0.001  # Temperature  
		self.nSites   = 100

		self.ENERGY_EQUILIBRIUM = 0
		self.ENERGY_DELTA=0
		self.MAG_EQUILIBRIUM = 0
		self.MAG_DELTA=0
		self.DATAPOINTS=20
		self.THERMALIZATION = self.nSites**4		#steps for thermalization
		self.AVERAGING_OVER = self.nSites**4

		self.state = (np.round(np.random.rand(self.nSites,self.nSites))*2).astype(int)-1

		self.E=[]
		self.M=[]
		print 'nSites = ', self.nSites
		print 'Steps = ',self.THERMALIZATION
		print 'Temp = ',self.T
		self.ran_for=0
		self.points_taken=0


	def dU(self,i, j):    
	   m = self.nSites - 1 
	   if i == 0 :                # state[0,j]
		  top = self.state[m,j]
	   else : 
		  top = self.state[i-1,j]

	   if i == m :                # state[m,j]
		  bottom = self.state[0,j]
	   else : 
		  bottom = self.state[i+1,j]  

	   if j == 0 :                # state[i,0]
		  left = self.state[i,m]
	   else : 
		  left = self.state[i,j-1]

	   if j == m :                # state[i,m]
		  right = self.state[i,0]
	   else : 
		  right = self.state[i,j+1]  

	   return 2.*self.state[i,j]*(top+bottom+left+right)


	def Energy_latt(self,latt):
		"Energy of a 2D Ising lattice at particular configuration"
		Ene = 0
		N=self.nSites
		up = 0.0
		down = 0.0
		for i in range(N):
			for j in range(N):
				S = latt[i,j]
				if S==1: up+=1
				else: down +=1
				WF = latt[(i+1)%N, j] + latt[i,(j+1)%N] + latt[(i-1)%N,j] + latt[i,(j-1)%N]
				Ene += -WF*S # Each neighbor gives energy 1.0

		magnetization = (up-down)/N**2
		Ene = Ene/(2.0*N*N)
		return Ene , magnetization # Each pair counted twice


	def simulateData(self):
		# an infinite while loop that simulates stuff
		while True:
			time.sleep(0.000001)
			i = int(np.random.rand()*self.nSites) 
			j = int(np.random.rand()*self.nSites)  
			# Any system energy change if flip dipol
			dE = self.dU(i,j)
			# flip if system will have lower energy
			if dE <= 0. :
				self.state[i][j] = -self.state[i][j]
				if(self.state[i][j]>0):dm=2
				else:dm=-2
				if self.ran_for > self.THERMALIZATION:
					self.ENERGY_DELTA += dE/(1.*self.nSites**2)
					self.MAG_DELTA += dm/(1.*self.nSites**2)

			# otherwise do random decision     
			elif np.random.rand() < np.exp(-dE/self.T) :
				self.state[i][j] = -self.state[i][j]
				if(self.state[i][j]>0):dm=2
				else:dm=-2
				if self.ran_for > self.THERMALIZATION:
					self.ENERGY_DELTA += dE/(1.*self.nSites**2)
					self.MAG_DELTA += dm/(1.*self.nSites**2)
			else:
				dm=0
				
			self.ran_for+=1


			if self.ran_for == self.THERMALIZATION:	#Calculate energy,M using site by site analysis before starting
				self.ENERGY_EQUILIBRIUM,self.MAG_EQUILIBRIUM = self.Energy_latt(state)
				print 'mag , ene eq',self.MAG_EQUILIBRIUM,self.ENERGY_EQUILIBRIUM



			if self.ran_for%(self.THERMALIZATION/2) ==0 :		# Data gathering once thermalization is complete
				self.E.append(self.ENERGY_EQUILIBRIUM+self.ENERGY_DELTA)
				self.M.append(self.MAG_EQUILIBRIUM+self.MAG_DELTA)
				self.points_taken+=1
				#print 'E , M',E,M


			if self.points_taken==self.DATAPOINTS:
				print 'steps taken ', self.ran_for
				self.E=np.array(self.E)
				self.M=np.array(self.M)
				#e,m = Energy_latt(state)
				#ET.write('%f %f\n'%(T, np.average(E) ) )
				#print 'dumped to file, T was ',T, ', energy is ',ENERGY_EQUILIBRIUM+ENERGY_DELTA

				#cv=(np.average(E*E) - np.average(E)**2 )/(T*T)
				#print 'specific heat ',cv
				#CT.write('%f %f\n'%(T, cv ))

				#print 'magnetization ',MAG_EQUILIBRIUM+MAG_DELTA
				#MT.write('%f %f\n'%(T, np.average(abs(M)) ) )

				#chi=(np.average(M*M) - np.average(abs(M))**2 )/(T*T)
				#print 'susceptibility ',chi
				#ChiT.write('%f %f\n'%(T, chi))

				self.E=[]
				self.M=[]
				self.ENERGY_DELTA=0.0
				self.MAG_DELTA=0.0
				
				self.T=self.T+0.01
				self.points_taken=0
				#sys.exit(1)
				if T>3:
					sys.exit(1)
				self.state = (np.round(np.random.rand(self.nSites,self.nSites))*2).astype(int)-1
				print 'reordering: ', Energy_latt(state)
				self.ran_for=0
			self.newData.emit(self.state)






    

        
class MainWin(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		pg.setConfigOptions(antialias=True)

		self.w = gl.GLViewWidget()
		self.w.opts['distance'] = 40
		self.w.setWindowTitle('ISING MODEL SIMULATION')

		self.g = gl.GLGridItem()
		self.w.addItem(self.g)
		self.setCentralWidget(self.w)

		self.simul = simulator()
		self.simulthread = QtCore.QThread()
		self.simul.moveToThread(self.simulthread)
		self.simulthread.started.connect(self.simul.simulateData)


		####################### GRAPHICS ###############
		self.pos3 = np.zeros((self.simul.nSites,self.simul.nSites,3))
		print len(self.pos3),self.pos3.shape
		self.pos3[:,:,:2] = np.mgrid[:self.simul.nSites, :self.simul.nSites].transpose(1,2,0) * [-20./self.simul.nSites,20./self.simul.nSites]
		self.pos3 += [10,-10,0.5]
		self.points = self.simul.nSites**2
		self.pos3 = self.pos3.reshape(self.points,3)
		self.sp3 = gl.GLScatterPlotItem(pos=self.pos3, color=(1,1,1,.3), size=20./self.simul.nSites, pxMode=False)
		self.w.addItem(self.sp3)

		###################

		self.t = QtCore.QTimer()
		self.t.timeout.connect(self.update)
		self.t.start(100)
		self.simulthread.start()


	def update(self):
		## update surface positions and colors
		linear = self.simul.state.reshape(self.points)#-0.5
		#pos3[:,2] = linear
		color = np.empty((len(self.pos3),4), dtype=np.float32)
		color[:,3] = 1
		color[:,0] = np.clip(linear*2, 0, 1)
		color[:,1] = np.clip(0.2 , 0, 1)
		color[:,2] = np.clip(0.5 , 0, 1)
		self.sp3.setData(pos=self.pos3 ,color=color)
        

            
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWin()
    main.show()
    sys.exit(app.exec_())
