import gzip
import struct
import sys

import numpy as np

MNIST_MAGIC_IMAGE = 2051
MNIST_MAGIC_LABEL = 2049

def load_images(filename):
	with gzip.open(filename) as f:
		(magic,) = _unpack_from_file('>L', f)
		if magic != MNIST_MAGIC_IMAGE:
			print("Invalid magic (%08x) in image file %s" % (magic, filename), file=sys.stderr)
			return None

		(images, rows, cols) = _unpack_from_file('>LLL', f)
		image_array = np.frombuffer(f.read(), np.uint8).reshape((images, rows, cols))

		return image_array

def load_labels(filename):
	with gzip.open(filename) as f:
		(magic,) = _unpack_from_file('>L', f)
		if magic != MNIST_MAGIC_LABEL:
			print("Invalid magic (%08x) in label file %s" % (magic, filename), file=sys.stderr)
			return None

		(labels,) = _unpack_from_file('>L', f)
		label_array = np.frombuffer(f.read(), np.uint8)

		return label_array

def _unpack_from_file(fmt, file_):
	return struct.unpack(fmt, file_.read(struct.calcsize(fmt)))
