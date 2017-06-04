import itertools

import numpy as np

class FeedForward:
	def __init__(self, shape):
		self.shape = shape
		self.weights = []

		for idim, odim in pairwise_(shape):
			weights = np.empty((idim + 1, odim)) # +1 is the bias weight
			self.weights.append(weights)

	def randomize(self):
		self.weights = list(map(lambda l: np.random.randn(*l.shape), self.weights))

	def execute(self, input_, all_layers=False):
		input_ = np.array(input_)
		outputs = []

		for layer_weights in self.weights:
			input_with_bias = np.append(input_, np.ones((input_.shape[0], 1)), axis=1)
			outputs.append(input_with_bias)
			output_ = np.dot(input_with_bias, layer_weights)
			output_ = self.fn_activation(output_)
			input_ = output_

		outputs.append(output_)

		if all_layers:
			return outputs
		else:
			return output_

	def train(self, input_, output_, rate):
		input_ = np.array(input_)
		nn_outputs = self.execute(input_, True)

		last_delta = self.fn_error_dy(nn_outputs[-1], output_) * self.fn_activation_dx(nn_outputs[-1])
		deltas = [last_delta]

		for i in range(len(self.weights)-1, 0, -1):
			delta = last_delta.dot(self.weights[i].T) * self.fn_activation_dx(nn_outputs[i])
			deltas.insert(0, delta)
			last_delta = delta[:,:-1]

		for i in range(len(self.weights)):
			samples = deltas[i].shape[0]
			Delta = nn_outputs[i].T.dot(deltas[i]) / samples
			if i != len(self.weights) - 1:
				Delta = Delta[:,:-1]
			self.weights[i] += -rate * Delta

	def fn_activation(self, x):
		raise NotImplementedError

	def fn_activation_dx(self, dx):
		raise NotImplementedError

	def fn_error(self, expected, actual):
		raise NotImplementedError

	def fn_error_dy(self, expected, actual):
		raise NotImplementedError

class MLP(FeedForward):
	def fn_activation(self, x):
		return np.reciprocal(np.add(1, np.exp(np.negative(x))))

	def fn_activation_dx(self, x):
		return np.multiply(x, np.subtract(1, x))

	def fn_error(self, t, y):
		return np.divide(np.square(np.subtract(t, y)), 2)

	def fn_error_dy(self, t, y):
		return np.subtract(t, y)

def pairwise_(iterable):
	"s -> (s0,s1), (s1,s2), (s2, s3), ..."
	a, b = itertools.tee(iterable)
	next(b, None)
	return zip(a, b)
