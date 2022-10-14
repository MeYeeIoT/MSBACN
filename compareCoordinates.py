class compareCoordinates:

	def __init__(self, interval):
		self.interval = interval

	def compare(self, interval):
		xArr = []
		yArr = []
		xArrB = []
		yArrB = []
		highestSimilarity = 0
		similarityCounter = 0
		cOrientation=0
		f = open("/home/brynm/sf2022/starConnections/starCoords.txt", "r")
		firstCount = len(f.readlines())
		f.seek(0)
		for r in range(firstCount):
			cLine = f.readline()
			comma = cLine.find(" , ")
			xCoord = cLine[0:comma]
			yCoord = cLine[comma+3:len(cLine)]
			xArrB.append(float(xCoord))
			yArrB.append(float(yCoord))
		f.close()
		for i in range(0, 360, self.interval):
			f = open("/home/brynm/sf2022/stararrays/pointArr.txt", "r+")
			#f = open("/home/brynm/sf2022/stararrays/pointArr"+str(i)+".txt", "r+")
			secondCount = len(f.readlines())
			f.seek(0)
			for r in range(secondCount):
				cLine = f.readline()
				comma = cLine.find(" , ")
				xCoord = cLine[0:comma]
				yCoord = cLine[comma+3:len(cLine)]
				xArr.append(float(xCoord))
				yArr.append(float(yCoord))
			for k in range(firstCount):
				for m in range(secondCount):
					if(((xArrB[k]-200) <= xArr[m] <= (xArrB[k]+200)) and ((yArrB[k]-200) <= yArr[m] <= (yArrB[k]+200))):
						#Used 150 with good results
						similarityCounter = similarityCounter+1
						#print("Coordinate :", xArr[m], yArr[m])
						#print("Fits in the range: ", (xArrB[k]-150), (xArrB[k]+150), " for xs and : ", (yArrB[k]-150), (yArrB[k]+150), "for ys")
			if(similarityCounter>highestSimilarity):
				highestSimilarity = similarityCounter
				cOrientation = i
			similarityCounter=0
			xArr.clear()
			yArr.clear()
		#print("Corret Orientation is: ", cOrientation, " With: ", highestSimilarity)
		#print("Similarity Counter: ", similarityCounter)
		f.close()
		return cOrientation, highestSimilarity

