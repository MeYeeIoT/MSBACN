import time
import math
from astroplan import FixedTarget
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
from convertCoord import convertCoord
from rotatePoints import rotatePoints
from compareCoordinates import compareCoordinates
#Days Since J2000
start = time.time()
divisor = float(4)
timer = float(time.time())
timers = time.gmtime(timer)
print("Current Time: ", timers)
timers= time.strptime("4/1/2022 02:15", "%d/%m/%Y %H:%M")
years = timers.tm_year - 2000
iyears = int(years)
totalDays=years*365 #Years
totalDays=(timers.tm_min/60)+totalDays #Minutes
totalDays=(timers.tm_hour/24)+totalDays #Hours
totalDays=totalDays+timers.tm_yday #Days
for x in range (iyears): #Leap Years
	if (x%4) == 0:
		totalDays = totalDays + 1
totalDays=totalDays-1.5 #Cause January 1st 2000

#For RA and DEC correction
correctionTimer = float(time.time())
correctionTimer = time.gmtime(correctionTimer)
cYears = correctionTimer.tm_year - 2000
cYears = cYears+(correctionTimer.tm_yday/365.25)
cYears = cYears/100

#LST
def findLST(longitude):
	utcDecimal = (timers.tm_min/60)+(timers.tm_hour)
	#print("UTC Decimal: ", utcDecimal)
	lst = 100.46 + (.985647*totalDays) + longitude + (15*utcDecimal)
	while lst>360:
    		lst=lst-360
	return lst

#Hour Angle
def hourAngler(ra, lst):
	#star = FixedTarget.from_name(name)
	hourAngle = lst-(ra)
	if(hourAngle<0):
		hourAngle=hourAngle+360
	return hourAngle

#Operations
def sin(number):
	number = math.radians(number)
	number = math.sin(number)
	return number

def cos(number):
	number = math.radians(number)
	number = math.cos(number)
	return number

def sinD(number):
	number = np.sin(np.radians(number))
	return number

def cosD(number):
    number = np.cos(np.radians(number))
    return number

def tanD(number):
    number = np.tan(np.radians(number))
    return number

def aSin(number):
	#print("Arc Sin Number: ", number, "\n\n")
	number = np.degrees(np.arcsin(number))
	return number

def aCos(number):
	number = np.degrees(np.arccos(number))
	return number

def convertRD(ra, dec, cYears):
	m = ((1.2812323)*cYears)+(.0003879*(cYears*cYears))+(.0000101*(cYears*cYears*cYears))
	n = ((.5567530)*cYears)-(.0001185*(cYears*cYears))+(.0000116*(cYears*cYears*cYears))
	deltaRa = m + (n*sinD(ra)*tanD(dec))
	deltaDec = (n*cosD(ra))
	return deltaRa+ra, deltaDec+dec

highestSimilarity = cOrientation = similarity = orientation = 0
cLong = cLat = 0
def altAz(i, lat, long):
	global hourAngle
	altitude = azimuth = 0.0
	latitude = lat
	longitude = long
	lst = findLST(longitude)
	star = starLocations[i]
	hourAngle = hourAngler(star.ra.degree, lst)
	ra, dec = convertRD(star.ra.degree, star.dec.degree, cYears)
	altitudeS = round((sin(dec)*sin(latitude))+(cos(dec)*cos(latitude)*cos(hourAngle)), 4)
	altitude = round(aSin(altitudeS), 4)
	if(altitude>=90 or altitude<0):
		return -1, -1
	azimuthS = round((sin(dec)-(sin(altitude)*sin(latitude))) / (cos(altitude)*cos(latitude)), 4)
	azimuth = round(aCos(azimuthS), 4)
	if sin(hourAngle)>=0:
		azimuth=360-azimuth
	#print()
	#print("Star: ", star)
	#print("Azimuth: ", azimuth)
	#print("Altitude: ", altitude)
	return azimuth, altitude

possibleMatchLat = []
possibleMatchLong = []
starLocations = []

def getStars():
	s = open('/home/brynm/sf2022/stars3.txt', 'r')
	count = len(s.readlines())
	s.seek(0)
	for i in range(count):
		starName = s.readline()
		star = FixedTarget.from_name(starName)
		starLocations.append(star)
	s.close()

getStars()

def plotGraphs(xArr, yArr, xArrArchive, yArrArchive, lat, long, nameArr, nameArrArchive):
	global savePointArr, highestSimilarity, cOrientation, similarity, orientation, cLat, cLong, possibleMatchLat, possibleMatchLong
	#for j in range(0, 360, 347):
	for j in range(0, 1):
		#Set last Value to the interval
		plot2 = plt.figure(1)
		index = 0
		xArr.clear()
		yArr.clear()
		xArr=xArrArchive.copy()
		yArr=yArrArchive.copy()
		#print("Opening pointArr", str(j), ".txt")
		#print("Opening pointArr", str(347), ".txt")
		#savePointArr = open("/home/brynm/sf2022/stararrays/pointArr"+str(275)+".txt", "w")
		savePointArr = open("/home/brynm/sf2022/stararrays/pointArr.txt", "w")
		#counter = 0
		for x in range(len(xArr)):
			#print("Has Run This Section: ", counter)
			#counter = counter+1
			#Set this to len(xArr) for doing all possible rotations
			rotateObject = rotatePoints(xArr[index], yArr[index], 0)
			#print("X: ", xArr[index], " Y: ", yArr[index], " Theta: ", j)
			a, b = rotateObject.rotate(xArr[index], yArr[index], 349)
			#print("After Rotation: \n X: ", a, " Y: ", b, " Theta: ", j, "\n")
			#print(rotateObject.rotate(xArr[index], yArr[index], j))
			xArr.pop(index)
			xArr.insert(index, a)
			yArr.pop(index)
			yArr.insert(index, b)
			#print("After Switching Values: ")
			#print("X Array: \n", xArr)
			#print("Y Array: \n", yArr)
			if(-2179 <= b <=2137 and -1700 <=a<= 1900):
				savePointArr.write(str(b*.9)+" , "+str(a*.9)+"\n")
			#print("After: A: ", a, " B: ", b, "\n")
			#print("Times Run: ", index)
			index = index+1
			#print("Has run ", j, "times")		
		savePointArr.close()
		for i in range(len(nameArr)):
			plt.text(yArr[i], xArr[i], nameArr[i])
		plt.scatter(yArr, xArr)
		plt.title("Latitude: "+ str(lat)+ " Longitude: "+ str(long))
		#Need to find wa way to convert from the degrees thing to pixels
		#Left Altitude is 47degrees 11' 23,5" (Castor)
		#Right Altitude is 46degrees 08' 30.7 (WDS J00473+2416)
		#Top Altitude is 50degrees 07' 46.7" (23 Cas)
		#Bottom Altitude is 52deg 36' 55.7" (Al Tak II)
		plt.axis([-2179, 2137, -1700, 1900])
		#plt.axis([-2000, 2000, -1500, 1500])
		plt.grid()
		plt.savefig("/home/brynm/sf2022/plots/scatter/"+str(j)+str(lat)+str(long)+".png")
		plt.clf()
	compareObject = compareCoordinates(275)
	(orientation, similarity) = compareObject.compare(compareObject.interval)
	if(highestSimilarity<similarity):
		print("New Best Match")
		print("Latitude: ", lat, " Longitude: ", long)
		cLat = lat
		cLong = long
		print("Lat: ", cLat, " Long: ", cLong)
		print("Orientation: ", orientation, " Similarity: ", similarity)
		highestSimilarity = similarity
		cOrientation = orientation
	elif(highestSimilarity==similarity):
		print("Multiple Possible Matches")
		print(orientation, similarity)
		possibleMatchLat.append(lat)
		possibleMatchLong.append(long)
	similarity=0

#Altitude Calculation
def testPositions(minLat, maxLat, minLong, maxLong, interval):
	print("HERE: ", minLat, maxLat, minLong, maxLong, interval)
	for lat in range(minLat, maxLat, interval):
		for long in range (minLong, maxLong, interval):
			#time.sleep(.01)
			print("Done Sleeping")
			print("Latitude: ", lat, " Longitude: ", long)
			s = open('/home/brynm/sf2022/stars3.txt', 'r')
			count = len(s.readlines())
			s.seek(0)
			plot1 = plt.figure(1)
			#ax = plt.subplot(111, projection = 'polar')
			xArr = []
			yArr = []
			nameArr = []
			for x in range(count):
				starName = s.readline()
				#print("\n"+starName)
				(azimuth, altitude) = altAz(x, lat, long)
				if(altitude==-1):
					#print("Not Viewable")
					continue
				#ax.plot(math.radians(azimuth), 90-altitude, 'w.')
				#ax.annotate(starName, (math.radians(azimuth), 90-altitude), color='white')
				convertObject = convertCoord(2850, altitude, azimuth)
				(xPos, yPos, zPos) = convertObject.convert(convertObject.p, convertObject.phi, convertObject.theta)
				xArr.append(xPos)
				yArr.append(-yPos)
				nameArr.append(starName)
			#print("Y Array Length", len(yArr))
			s.close()
			#ax.set_facecolor('#000000')
			#ax.set_rmax(90)
			#ax.set_theta_offset(np.radians(90))
			#plt.savefig("/home/brynm/sf2022/plots/polar.png")
			#print("\nX Array Length", len(xArr))
			#print("X Array: \n", xArr)
			#print("Y Array: \n", yArr)
			#print("Y Array Length", len(yArr), "\n")
			xArrArchive = xArr.copy()
			yArrArchive = yArr.copy()
			nameArrArchive = nameArr.copy()

			
			plotGraphs(xArr, yArr, xArrArchive, yArrArchive, lat, long, nameArr, nameArrArchive)
			savePointArr.close()
		print("The Current Best Match Is: ", cLat, cLong, " with ", highestSimilarity, " matches")
	return cLat, cLong, highestSimilarity
def looper(lLa, bLa, lLo, bLo, int, laDistance, loDistance): #Trying to add support for multiple possible matchess
	(cLat, cLong, highestSimilarity) = testPositions(lLa, bLa, lLo, bLo, int)
	return cLat, cLong
lLa=20
bLa=50
lLo=-123
bLo=-76
int=1
laDistance=360
loDistance=180

#lLa=41
#bLa=42
#lLo=-81
#bLo=-80
#int=1
#laDistance=1
#loDistance=1

(cLat, cLong) = looper(lLa, bLa, lLo, bLo, int, laDistance, loDistance)
#(cLat, cLong) = looper(cLat-10, cLat+10, cLong-10, cLong+10, 1, 20, 20)
#for j in range(len(possibleMatchLat)):
#	print(str(possibleMatchLat[j])+str(possibleMatchLong[j]))
#for i in range(len(possibleMatchLat)):
#	(cLat, cLong) = looper(possibleMatchLat[i]-10, possibleMatchLat[i]+10, possibleMatchLong[i]-10, possibleMatchLong[i]+10, 1, 20, 20)


print("The Best Match Was: ", cLat, cLong, " with ", highestSimilarity, " matches")
end = time.time()
print(f"Runtime of the program is {end - start}")

