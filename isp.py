import cv2
import numpy as np


def arducam108mp_isp(frame, ccm, ccm_list):
	frame = np.where(frame < 16, 0, frame - 16)
	frame = cv2.cvtColor(frame, cv2.COLOR_BayerGR2RGB)
	if ccm:
		if ccm_list:
			frame = color_correction(frame, 4000, ccm_list)
		else:
			print("If you choose to turn on the ccm function, you need to set the tuning file path")
	return frame

def apply_saturation(ccm, saturation):
	RGB2Y  = np.array([0.299, 0.587, 0.114,
					   -0.169, -0.331, 0.500,
					   0.500, -0.419, -0.081]).reshape(3, 3)

	Y2RGB = np.array([1.000, 0.000, 1.402,
					  1.000, -0.345, -0.714,
					  1.000, 1.771, 0.000]).reshape(3, 3)

	S = np.array([1, 0, 0,
				  0, saturation, 0,
				  0, 0, saturation]).reshape(3, 3)

	return np.matmul(np.matmul(np.matmul(Y2RGB, S), RGB2Y), ccm)

def color_correction(img, ct, ccms, saturation=1.0):
	'''
	Input:
		img: H*W*3 numpy array, input image
		ccm: 3*3 numpy array, color correction matrix 
	Output:
		output: H*W*3 numpy array, output image after color correction
	'''

	if ct <= ccms[0]["ct"]:
		ccm = np.array(ccms[0]["ccm"])
	elif ct >= ccms[-1]["ct"]:
		ccm = np.array(ccms[-1]["ccm"])
	else:
		index = 0
		for i in range(len(ccms)):
			if ccms[i]["ct"] >= ct:
				index = i
				break
		# print(ccms[index])
		lam = (ct - ccms[index - 1]["ct"]) / (ccms[index]["ct"] - ccms[index - 1]["ct"])
		ccm = lam * np.array(ccms[index]["ccm"]) + (1.0 - lam) * np.array(ccms[index - 1]["ccm"])

	ccm = ccm.reshape(3,3)
	ccm = apply_saturation(ccm, saturation)

	# RGB ccm 2 BGR ccm
	ccm = np.rot90(ccm, 2)
	# for swapped mul
	ccm = ccm.T

	img2 = img.reshape((img.shape[0] * img.shape[1], 3))
	output = np.matmul(img2, ccm)
	croped = np.clip(output.reshape(img.shape), 0, 255)
	result = croped.astype(img.dtype)
	return result
