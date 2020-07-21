import numpy as np
from sklearn.preprocessing import scale
from scipy.interpolate import interp1d


class Sample:
	"""
	Sample is used to load, store and process the signals obtained 
	from the accelerometers.
	It provides a method to load the signals from file and process them.
	"""
	def __init__(self, acx, acy, acz, gx, gy, gz, a0, a1, a2, a3, a4):
		self.acx = acx
		self.acy = acy
		self.acz = acz
		self.gx = gx
		self.gy = gy
		self.gz = gz
		self.a0 = a0
		self.a1 = a1
		self.a2 = a2
		self.a3 = a3
		self.a4 = a4

	def get_linearized(self, reshape=False):
		if reshape:
			return np.concatenate((self.acx, self.acy, self.acz, self.gx, self.gy, self.gz, self.a0, self.a1, self.a2, self.a3, self.a4)).reshape(1, -1)
		else:
			return np.concatenate((self.acx, self.acy, self.acz, self.gx, self.gy, self.gz, self.a0, self.a1, self.a2, self.a3, self.a4))
		
	@staticmethod
	def load_from_file(filename, size_fit=50):

		data_raw = [[int(x) for x in i.split()[1:-1]] for i in open(filename)]
		# data_raw = [map(lambda x: int(x), i.split(" ")[1:-1]) for i in open(filename)]

		data = np.array(data_raw).astype(float)
		data_norm = scale(data)

		acx = data_norm[:,0]
		acy = data_norm[:,1]
		acz = data_norm[:,2]

		gx = data_norm[:,3]
		gy = data_norm[:,4]
		gz = data_norm[:,5]

		a0 = data_norm[:,6]
		a1 = data_norm[:,7]
		a2 = data_norm[:,8]
		a3 = data_norm[:,9]
		a4 = data_norm[:,10]

		x = np.linspace(0, data.shape[0], data.shape[0])
		f_acx = interp1d(x, acx)
		f_acy = interp1d(x, acy)
		f_acz = interp1d(x, acz)

		f_gx = interp1d(x, gx)
		f_gy = interp1d(x, gy)
		f_gz = interp1d(x, gz)

		f_a0 = interp1d(x, a0)
		f_a1 = interp1d(x, a1)
		f_a2 = interp1d(x, a2)
		f_a3 = interp1d(x, a3)
		f_a4 = interp1d(x, a4)

		xnew = np.linspace(0, data.shape[0], size_fit)
		acx_stretch = f_acx(xnew)
		acy_stretch = f_acy(xnew)
		acz_stretch = f_acz(xnew)

		gx_stretch = f_gx(xnew)
		gy_stretch = f_gy(xnew)
		gz_stretch = f_gz(xnew)

		a0_stretch = f_a0(xnew)
		a1_stretch = f_a1(xnew)
		a2_stretch = f_a2(xnew)
		a3_stretch = f_a3(xnew)
		a4_stretch = f_a4(xnew)

		return Sample(acx_stretch, acy_stretch, acz_stretch, gx_stretch, gy_stretch, gz_stretch, a0_stretch, a1_stretch, a2_stretch, a3_stretch, a4_stretch)
