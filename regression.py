import tensorflow as tf
import numpy as np
D = 2
alpha_d = [0 for i in range(D)]
multiplier = [0 for i in range(D)]
obj_func = [0 for i in range(D)]
loss = [0 for i in range(D)]
train_op = [0 for i in range(D)]
ratings = tf.constant([1.,2.],shape = [1,D])
sigma_matr = tf.Variable(tf.diag(tf.ones(4)))
delta = tf.Variable(0.2)
for i in range(D):
	alpha_d[i] = tf.Variable(tf.random_uniform([4,1],0,1))
	x[i] = tf.multiply(tf.pow(tf.multiply(2.,tf.square(delta)),-1),
		tf.subtract(ratings[i],tf.square(tf.reduce_sum(tf.matmul(tf.transpose(alpha_d[i]),alpha_d[i])))))
	y[i] = tf.reduce_sum(tf.matmul(tf.transpose(alpha_d[i]),tf.matmul(sigma_matr,alpha_d[i])))

	obj_func[i] = tf.add(x[i]+y[i])
	loss[i] = obj_func[i]+tf.square(1-tf.reduce_sum(alpha_d[i]))
	train_op[i] = tf.train.GradientDescentOptimizer(0.01).minimize(loss[i])

init = tf.initialize_all_variables()

with tf.Session() as sess:
	sess.run(init)
	for i in range(2000):
		for j in range(D):
			sess.run(train_op[j])
	print(sess.run(alpha_d))