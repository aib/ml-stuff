#!/usr/bin/env python3

import operator
import os.path

import numpy as np

import mnist
import nn

MNIST_DIR = '.'
NN_FILE = './network.pickle'

def main():
	np.set_printoptions(precision=3, suppress=True, linewidth=1000)

	print("Loading training set")
	training_images = mnist.load_images(os.path.join(MNIST_DIR, 'train-images-idx3-ubyte.gz'))
	training_labels = mnist.load_labels(os.path.join(MNIST_DIR, 'train-labels-idx1-ubyte.gz'))

	images = training_images.reshape(training_images.shape[0], training_images.shape[1] * training_images.shape[2]) / 255
	labels = list(map(lambda x: list(map(lambda l: 1 if x == l else 0, range(10))), training_labels))

	print("%d images and %d labels read" % (len(training_images), len(training_labels)))

	try:
		with open(NN_FILE, 'rb') as f:
			print("Loading network")
			net = nn.MLP.from_file(f)
	except FileNotFoundError:
		print("Creating randomized network")
		net = nn.MLP((784, 10, 10))
		net.randomize()

	print("Training")
	for n in range(1):
		print("Pass", n+1)
		for i in range(len(images)):
			net.train([images[i]], [labels[i]], 0.2)

	print("Training complete. Saving network")
	with open(NN_FILE, 'wb') as f:
		net.save(f)

	print("Loading test set")
	test_images = mnist.load_images(os.path.join(MNIST_DIR, 't10k-images-idx3-ubyte.gz'))
	test_labels = mnist.load_labels(os.path.join(MNIST_DIR, 't10k-labels-idx1-ubyte.gz'))
	print("%d images and %d labels read" % (len(test_images), len(test_labels)))

	test_images_reshaped = test_images.reshape(test_images.shape[0], test_images.shape[1] * test_images.shape[2]) / 255

	test_output = net.execute(test_images_reshaped)
	test_output_labels = list(map(lambda o: max(enumerate(o), key=lambda p: p[1])[0], test_output))

	test_output_match_count = len(list(filter(operator.truth, map(operator.eq, test_labels, test_output_labels))))
	true_fraction = test_output_match_count / len(test_labels)
	print(true_fraction, "success rate")

if __name__ == '__main__':
	main()
