import math 
class convertCoord:

	def __init__(self, p, phi, theta):
		self.phi = phi
		self.theta = theta
		self.p = p

	def sinA(self, number):
		number = math.radians(number)
		number = math.sin(number)
		return number

	def cosA(self, number):
		number = math.radians(number)
		number = math.cos(number)
		return number

	def convert(self, p, phi, theta):
		phi = 90-phi
		#print("Phi: ", phi, " Theta: ", theta, " P: ", p)
		x = p*(self.sinA(phi))*(self.cosA(theta))
		y = p*(self.sinA(phi))*(self.sinA(theta))
		z = p*(self.cosA(phi))
		print("X: ", x, " Y: ", y, " Z: ", z)
		return x, y, z

object = convertCoord(30, 30, 90)
print(object.convert(object.p, object.phi, object.theta))
print(object.convert(60, object.phi, object.theta))
print(object.convert(90, object.phi, object.theta))