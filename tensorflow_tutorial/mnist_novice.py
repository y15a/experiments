import tensorflow as tf
import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# x isn't a specific value. It's a placeholder, a value that we'll input
# when we ask TensorFlow to run a computation. We want to be able to input
# any number of MNIST images, each flattened into a 784-dimensional
# vector. We represent this as a 2d tensor of floating point numbers, with
# a shape [None, 784]. (Here None means that a dimension can be of any
# length.)
x = tf.placeholder("float", [None, 784])


# We also need the weights and biases for our model. We could imagine
# treating these like additional inputs, but TensorFlow has an even better
# way to handle it: Variable. A Variable is a modifiable tensor that lives
# in TensorFlow's graph of interacting operations. It can be used and even
# modified by the computation. For machine learning applications, one
# generally has the model parameters be Variables.

# We create these Variables by giving tf.Variable the initial value of the
# Variable: in this case, we initialize both W and b as tensors full of
# zeros. Since we are going to learn W and b, it doesn't matter very much
# what they initially are.

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

# Notice that W has a shape of [784, 10] because we want to multiply the
# 784-dimensional image vectors by it to produce 10-dimensional vectors of
# evidence for the difference classes. b has a shape of [10] so we can add
# it to the output.

# We can now implement our model. It only takes one line!

# First, we multiply x by W with the expression tf.matmul(x,W). This is
# flipped from when we multiplied them in our equation, where we had Wx,
# as a small trick to deal with x being a 2D tensor with multiple inputs.
# We then add b, and finally apply tf.nn.softmax.

y = tf.nn.softmax(tf.matmul(x, W) + b)  # matmul = matrix multiply

# That's it. It only took us one line to define our model, after a couple
# short lines of setup. That isn't because TensorFlow is designed to make
# a softmax regression particularly easy: it's just a very flexible way to
# describe many kinds of numerical computations, from machine learning
# models to physics simulations. And once defined, our model can be run on
# different devices: your computer's CPU, GPUs, and even phones!


# TRAINING ------------------------

# In order to train our model, we need to define what it means for the
# model to be good. Well, actually, in machine learning we typically
# define what it means for a model to be bad, called the cost or loss, and
# then try to minimize how bad it is. But the two are equivalent. One very
# common, very nice cost function is "cross-entropy."

# To implement cross-entropy we need to first add a new placeholder to
# input the correct answers:

y_ = tf.placeholder("float", [None, 10])

# Then we can implement the cross-entropy

cross_entropy = -tf.reduce_sum(y_ * tf.log(y))

# Now that we know what we want our model to do, it's very easy to have
# TensorFlow train it to do so. Because TensorFlow knows the entire graph
# of your computations, it can automatically use the backpropagation
# algorithm to efficiently determine how your variables affect the cost
# you ask it minimize. Then it can apply your choice of optimization
# algorithm to modify the variables and reduce the cost.

train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# In this case, we ask TensorFlow to minimize cross_entropy using the
# gradient descent algorithm with a learning rate of 0.01. Gradient
# descent is a simple procedure, where TensorFlow simply shifts each
# variable a little bit in the direction that reduces the cost. But
# TensorFlow also provides many other optimization algorithms: using one
# is as simple as tweaking one line.

# What TensorFlow actually does here, behind the scenes, is it adds new
# operations to your graph which implement backpropagation and gradient
# descent. Then it gives you back a single operation which, when run, will
# do a step of gradient descent training, slightly tweaking your variables
# to reduce the cost.

# Now we have our model set up to train. One last thing before we launch
# it, we have to add an operation to initialize the variables we created:

init = tf.initialize_all_variables()

# We can now launch the model in a Session, and run the operation that
# initializes the variables:

sess = tf.Session()
sess.run(init)

# Let's train -- we'll run the training step 1000 times!

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})


# EVALUATING ----------------

# Let's figure out where we predicted the correct label. tf.argmax is an
# extremely useful function which gives you the index of the highest entry
# in a tensor along some axis. For example, tf.argmax(y,1) is the label
# our model thinks is most likely for each input, while tf.argmax(y_,1) is
# the correct label. We can use tf.equal to check if our prediction
# matches the truth.

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

# That gives us a list of booleans. To determine what fraction are
# correct, we cast to floating point numbers and then take the mean. For
# example, [True, False, True, True] would become [1,0,1,1] which would
# become 0.75.

accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# Finally, we ask for our accuracy on our test data.

print sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})



