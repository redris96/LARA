import tensorflow as tf
import numpy as np

D = 2
k = 4

alpha_d = [0 for i in range(D)]
multiplier = [0 for i in range(D)]
obj_func = [0 for i in range(D)]
loss = [0 for i in range(D)]
train_op = [0 for i in range(D)]
ratings = tf.constant([1.,2.],shape = [1,D])
x = [0 for i in range(D)]
y = [0 for i in range(D)]

sigma_matr = tf.placeholder(shape = [k,k],dtype = tf.float32)
delta = tf.placeholder(dtype=tf.float32)
mu = tf.placeholder(shape=[k,1],dtype=tf.float32)

for i in range(D):
	alpha_d[i] = tf.Variable(tf.random_uniform([k,1],0,1))
	x[i] = tf.mul(tf.pow(tf.mul(2.,tf.square(delta)),-1),
		tf.sub(ratings[i],tf.square(tf.reduce_sum(tf.matmul(tf.transpose(alpha_d[i]),alpha_d[i])))))
	y[i] = 0.5*tf.reduce_sum(tf.matmul(tf.transpose(tf.sub(alpha_d[i],mu)),
		tf.matmul(tf.matrix_inverse(sigma_matr),tf.sub(alpha_d[i],mu))))

	obj_func[i] = tf.add(x[i],y[i])
	loss[i] = tf.add(0.001*obj_func[i],tf.square(1-tf.reduce_sum(alpha_d[i])))
	train_op[i] = tf.train.GradientDescentOptimizer(0.01).minimize(loss[i])

init = tf.initialize_all_variables()

act_alpha = [ [] for i in range(D)]
act_sigma_matr = np.identity(k)
act_delta = 0.2
act_mu = np.random.rand(k,1)

with tf.Session() as sess:
	sess.run(init)
	for _ in range(3):
		for j in range(D):
			for i in range(80):
				x,_ = sess.run([alpha_d[j],train_op[j]],feed_dict={sigma_matr:act_sigma_matr,
					mu:act_mu,delta:act_delta})
			act_alpha[j]=x
		
		act_mu = (1/D)*np.sum(act_alpha,0)
		act_mu = np.reshape(act_mu,(k,1))
		temp_matr = np.reshape(np.transpose(act_alpha),(k,D))
		act_sigma_matr = np.cov(temp_matr)

	print(act_alpha)
