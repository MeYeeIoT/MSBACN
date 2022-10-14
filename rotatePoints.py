import numpy as np

class rotatePoints:
	def __init__(self, x, y, theta):
		self.x = x
		self.y = y
		self.theta = theta

	def sinD(self, number):
		number = np.sin(np.radians(number))
		return number

	def cosD(self, number):
		number = np.cos(np.radians(number))
		return number

	def rotate(self, x, y, theta):
		x2=self.x
		y2=self.y
		finalX = (x2*self.cosD(theta))-(y2*self.sinD(theta))
		finalY = (x2*self.sinD(theta))+(y2*self.cosD(theta))
		return finalX, finalY

#object = rotatePoints(51, -40, 330)
#print(object.sinD(-79))
#print(object.rotate(object.x, object.y, object.theta))
#print(object.sinD(30))