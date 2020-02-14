from bed import Bed
import numpy as np

class Hospital:
	def __init__(self, bed_num):
		# self.bed_num = bed_num
		self.yy = bed_num // 20
		self.xx = bed_num //self.yy
		if bed_num % self.yy:
			self.xx += 1

		self.beds = np.array([])
		for i in range(self.xx):
			for j in range(self.yy):
				bed = Bed(i, j,True)
				self.beds = np.append(self.beds, bed)

	def pickBed(self):
		for bed in self.beds:
			if bed.isEmpty:
				bed.isEmpty = False
				return bed
		return None

	def getX(self):
		return np.array([bed.x for bed in self.beds])

	def getY(self):
		return np.array([bed.y for bed in self.beds])

	def getStatus(self):
		return np.array([bed.isEmpty for bed in self.beds])