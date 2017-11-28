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
	newData  = QtCore.pyqtSignal(str)

	def __init__(self):
		super(simulator, self).__init__()
		self.T = 4.6  # Temperature 
		self.MAX_T = 30. 
		self.nSites   = 20

		self.ET = open('data/et_%d.txt'%(self.nSites),'wt')
		self.CT = open('data/ct_%d.txt'%(self.nSites),'wt')
		self.MT = open('data/mt_%d.txt'%(self.nSites),'wt')
		self.ChiT = open('data/chit_%d.txt'%(self.nSites),'wt')

		self.ENERGY_EQUILIBRIUM = 0
		self.ENERGY_DELTA=0
		self.MAG_EQUILIBRIUM = 0
		self.MAG_DELTA=0
		self.DATAPOINTS=20
		self.THERMALIZATION = self.nSites**5		#steps for thermalization
		self.AVERAGING_OVER = self.nSites**5

		self.state = (np.round(np.random.rand(self.nSites,self.nSites,self.nSites))*2).astype(int)-1

		self.E=[]
		self.M=[]
		print 'nSites = ', self.nSites
		print 'Steps = ',self.THERMALIZATION
		print 'Temp = ',self.T
		self.ran_for=0
		self.points_taken=0
		self.running=False



	def dU(self,i, j, k):
	   m = self.nSites - 1 
	   if i == 0 :                # state[0,j]
		  top = self.state[m,j,k]
	   else : 
		  top = self.state[i-1,j,k]

	   if i == m :                # state[m,j]
		  bottom = self.state[0,j,k]
	   else : 
		  bottom = self.state[i+1,j,k]  

	   if j == 0 :                # state[i,0]
		  left = self.state[i,m,k]
	   else : 
		  left = self.state[i,j-1,k]

	   if j == m :                # state[i,m]
		  right = self.state[i,0,k]
	   else : 
		  right = self.state[i,j+1,k]  

	   if k == 0 :                
		  down = self.state[i,j,m]
	   else : 
		  down = self.state[i,j,k-1]  

	   if k == m :                
		  up = self.state[i,j,0]
	   else : 
		  up = self.state[i,j,k+1]




	   return 2.*self.state[i,j,k]*(top+bottom+left+right+up+down)


	def Energy_latt(self,latt):
		"Energy of a 2D Ising lattice at particular configuration"
		Ene = 0
		N=self.nSites
		up = 0.0
		down = 0.0
		for i in range(N):
			for j in range(N):
				for k in range(N):
					S = latt[i,j,k]
					if S==1: up+=1
					else: down +=1
					WF = latt[(i+1)%N, j,k] + latt[i,(j+1)%N,k] + latt[(i-1)%N,j,k] + latt[i,(j-1)%N,k] + latt[i,j,(k-1)%N] + latt[i,j,(k+1)%N]  
					Ene += -WF*S # Each neighbor gives energy 1.0

		magnetization = (up-down)/N**3
		Ene = Ene/(2.0*N*N*N)
		return Ene , magnetization # Each pair counted twice


	def simulateData(self):
		# an infinite while loop that simulates stuff
		while self.T<self.MAX_T:
			time.sleep(0.00000001)
			if not self.running:
				time.sleep(0.001)
				continue
			i = int(np.random.rand()*self.nSites) 
			j = int(np.random.rand()*self.nSites)  
			k = int(np.random.rand()*self.nSites)  
			# Any system energy change if flip dipol
			dE = self.dU(i,j,k)
			# flip if system will have lower energy
			if dE <= 0. :
				self.state[i][j][k] = -self.state[i][j][k]
				if(self.state[i][j][k]>0):dm=3
				else:dm=-3
				if self.ran_for >= self.THERMALIZATION:
					self.ENERGY_DELTA += dE/(1.*self.nSites**3)
					self.MAG_DELTA += dm/(1.*self.nSites**3)

			# otherwise do random decision     
			elif np.random.rand() < np.exp(-dE/self.T) :
				self.state[i][j][k] = -self.state[i][j][k]
				if(self.state[i][j][k]>0):dm=3
				else:dm=-3
				if self.ran_for >= self.THERMALIZATION:
					self.ENERGY_DELTA += dE/(1.*self.nSites**3)
					self.MAG_DELTA += dm/(1.*self.nSites**3)
			else:
				dm=0
				
			self.ran_for+=1




			if self.ran_for >= self.THERMALIZATION:
				if self.ran_for == self.THERMALIZATION:	#Calculate energy,M using site by site analysis before starting
					self.ENERGY_EQUILIBRIUM,self.MAG_EQUILIBRIUM = self.Energy_latt(self.state)
					print 'mag , ene eq',self.MAG_EQUILIBRIUM,self.ENERGY_EQUILIBRIUM

				if self.ran_for%(self.THERMALIZATION/4) ==0 :		# Data gathering once thermalization is complete
					self.E.append(self.ENERGY_EQUILIBRIUM+self.ENERGY_DELTA)
					self.M.append(self.MAG_EQUILIBRIUM+self.MAG_DELTA)
					self.points_taken+=1
					self.newData.emit('Gathering(%d): T=%.2f\tE=%.2e\tM=%.2e'%(self.points_taken,self.T,self.ENERGY_EQUILIBRIUM+self.ENERGY_DELTA,self.MAG_EQUILIBRIUM+self.MAG_DELTA))


			if self.points_taken==self.DATAPOINTS:
				print '\n\n#####################################'
				print 'steps taken ', self.ran_for
				self.E=np.array(self.E)
				self.M=np.array(self.M)
				e,m = self.Energy_latt(self.state)
				self.ET.write('%f %f\n'%(self.T, np.average(self.E) ) )
				print 'dumped to file, T was ',self.T, ', energy is ',self.ENERGY_EQUILIBRIUM+self.ENERGY_DELTA

				cv=(np.average(self.E*self.E) - np.average(self.E)**2 )/(self.T**2)
				print 'specific heat ',cv
				self.CT.write('%f %f\n'%(self.T, cv ))

				print 'magnetization ',self.MAG_EQUILIBRIUM+self.MAG_DELTA
				self.MT.write('%f %f\n'%(self.T, np.average(abs(self.M)) ) )

				chi=(np.average(self.M**2) - np.average(abs(self.M))**2 )/(self.T**2)
				print 'susceptibility ',chi
				self.ChiT.write('%f %f\n'%(self.T, chi))

				MESSAGE = 'DONE T=%.2f\tE=%.2f\tCv=%.2e\tM=%.2f\tChi=%.2f'%(self.T,np.average(self.E),cv,np.average(abs(self.M)),chi)

				self.E=[]
				self.M=[]
				self.ENERGY_DELTA=0.0
				self.MAG_DELTA=0.0
				
				self.T=self.T+0.1
				self.points_taken=0
				self.state = (np.round(np.random.rand(self.nSites,self.nSites,self.nSites))*2).astype(int)-1
				E=self.Energy_latt(self.state)
				print 'reordering: ', E
				self.newData.emit('%s | reordered. E -> %.2e , M-> %.2e | '%(MESSAGE,E[0],E[1]))
				self.ran_for=0






from layout import Ui_MainWindow

        
class AppWindow(QtGui.QMainWindow,Ui_MainWindow):
	def __init__(self,parent=None):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.statusBar = self.statusBar()

		pg.setConfigOptions(antialias=True)
		
		self.w = gl.GLViewWidget()
		self.w.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)


		self.w.opts['distance'] = 40
		self.w.setWindowTitle('ISING MODEL SIMULATION')

		self.g = gl.GLGridItem()
		self.w.addItem(self.g)
		self.plotLayout.addWidget(self.w)

		
		self.simul = simulator()
		self.simul.newData.connect(self.gotParams)
		self.simulthread = QtCore.QThread()
		self.simul.moveToThread(self.simulthread)
		self.simulthread.started.connect(self.simul.simulateData)


		####################### GRAPHICS ###############
		self.paramMessage=''
		self.hideStatusUp = False
		self.hideStatusDown = False
		
		self.doSlice=False
		self.sliceLevel=50
		self.sliceArea = (self.simul.nSites**2)
		self.sliceStart = int(self.sliceArea*self.sliceLevel*self.simul.nSites/100.)
		self.sliceZ = int(self.sliceLevel*self.simul.nSites/100.)

		
		self.pos3 = np.zeros((self.simul.nSites,self.simul.nSites,self.simul.nSites,3))
		self.pos3[:,:,:,:3] = np.mgrid[:self.simul.nSites, :self.simul.nSites, :self.simul.nSites].transpose(1,3,2,0) * [-20./self.simul.nSites,-20./self.simul.nSites,20./self.simul.nSites]
		self.pos3 += [10,10,-10]
		self.points = self.simul.nSites**3
		self.pos3 = self.pos3.reshape(self.points,3)
		self.sp3 = gl.GLScatterPlotItem(pos=self.pos3, color=(1,1,1,.3), size=20./self.simul.nSites, pxMode=False)
		self.w.addItem(self.sp3)

		###################

		self.t = QtCore.QTimer()
		self.t.timeout.connect(self.update)
		self.t.start(100)
		self.simulthread.start()


	def update(self):
		self.statusBar.showMessage('%s | iterations: %d'%(self.paramMessage,self.simul.ran_for))
		if self.hideStatusDown and self.hideStatusUp: return
		## update surface positions and colors
		if not self.doSlice:
			linear = self.simul.state.reshape(self.points)#-0.5
			color = np.empty((len(self.pos3),4), dtype=np.float32)
		else:
			linear = self.simul.state[:,:,self.sliceZ].reshape(self.sliceArea)#-0.5
			color = np.empty((self.sliceArea,4), dtype=np.float32)

		color[:,0] = np.clip(linear*2, 0, 1)
		color[:,1] = np.clip(0.2 , 0, 1)
		color[:,2] = np.clip(0.5 , 0, 1)

		color[:,3] = 0.15
		if self.hideStatusDown: color[:,3] = np.clip(linear,0,0.5)
		if self.hideStatusUp: color[:,3] = np.clip(-1*linear,0,0.5)


		if not self.doSlice:
			self.sp3.setData(pos=self.pos3 ,color=color)
		else:
			color[:,3] = 1.
			color[:,0] = np.round(linear*2)
			color[:,1] = np.clip(0.2 , 0, 1)
			color[:,2] = np.clip(0.5 , 0, 1)
			self.sp3.setData(pos=self.pos3[self.sliceStart:self.sliceStart+self.sliceArea] ,color=color)
        
	def gotParams(self,msg):
		self.paramMessage = msg
	def play(self):
		self.simul.running=True
	def pause(self):
		self.simul.running=False
	def hideUp(self,state):
		self.hideStatusUp=state
		if self.hideStatusDown and self.hideStatusUp: self.sp3.setData(pos=[[1,1,1]] )
	def hideDown(self,state):
		self.hideStatusDown=state
		if self.hideStatusDown and self.hideStatusUp: self.sp3.setData(pos=[[1,1,1],[1,2,1]] )

	def force(self):
		print('force approach thermalization')
		self.simul.ran_for = self.simul.THERMALIZATION-10
	def slicing(self,val):
		self.doSlice = val
	def setSlicing(self,val):
		self.sliceLevel = val
		self.sliceZ = int(self.sliceLevel*self.simul.nSites/100.)
		self.sliceStart = int(self.sliceArea*int(self.sliceLevel*self.simul.nSites/100.))
	def setT(self,val):
		self.simul.T = val

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = AppWindow()
    main.show()
    sys.exit(app.exec_())
