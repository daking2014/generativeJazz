# Simple GAN implementation with keras
# adaptation of https://gist.github.com/Newmu/4ee0a712454480df5ee3
import sys
from keras.models import Sequential
from keras import layers
from keras.layers.core import Dense,Dropout
from keras.optimizers import SGD
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde
from scipy.io import wavfile
import theano.tensor as T
import theano
import pydub
from keras.utils import np_utils

batch_size = 96 # 16384
seq_length = 192 # 32768
dec_input_num = 150

print("loading data")

# f = pydub.AudioSegment.from_mp3('../ml-music/07_-_Brad_Sucks_-_Total_Breakdown.mp3')
# data = np.fromstring(f._data, np.int16)
# data = data.astype(np.float64).reshape((-1,2))
# print(data.shape)
# data = data[:,0]+data[:,1]
# #data = data[:,:subsample*int(len(data)/subsample)-1,:]
# data -= data.min()
# data /= data.max() / 2.
# data -= 1.
# print(data.shape)
data = np.load('justNotesSplit.npz')['X']
y = np.load('justNotesSplit.npz')['y']
y = np_utils.to_categorical(y)
print(data.shape)

print("Setting up decoder")
decoder = Sequential()
decoder.add(Dense(dec_input_num, input_dim=seq_length, activation='relu'))
decoder.add(Dropout(0.5))
decoder.add(Dense(int(dec_input_num*0.5), activation='relu'))
decoder.add(Dropout(0.5))
decoder.add(Dense(y.shape[1], activation='sigmoid'))

sgd = SGD(lr=0.01, momentum=0.1)
decoder.compile(loss='binary_crossentropy', optimizer=sgd)

print("Setting up generator")
generator = Sequential()
# model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
# model.add(Dropout(0.2))
# model.add(Dense(y.shape[1], activation='softmax'))
generator.add(layers.LSTM(100, input_shape=(50, 1)))
generator.add(Dropout(0.2))
generator.add(Dense(y.shape[1], activation='softmax'))

generator.compile(loss='binary_crossentropy', optimizer=sgd)

print("Setting up combined net")
gen_dec = Sequential()
gen_dec.add(generator)
for l in decoder.layers:
    l.trainable = False
decoder.trainable=False
gen_dec.add(decoder)

#def inverse_binary_crossentropy(y_true, y_pred):
#    if theano.config.floatX == 'float64':
#        epsilon = 1.0e-9
#    else:
#        epsilon = 1.0e-7
#    y_pred = T.clip(y_pred, epsilon, 1.0 - epsilon)
#    bce = T.nnet.binary_crossentropy(y_pred, y_true).mean(axis=-1)
#    return -bce
#
#gen_dec.compile(loss=inverse_binary_crossentropy, optimizer=sgd)

gen_dec.compile(loss='binary_crossentropy', optimizer=sgd)
gen_dec.summary()

y_decode = np.ones(2*batch_size)
y_decode[:batch_size] = 0.
y_gen_dec = np.ones(batch_size)

def gaussian_likelihood(X, u=0., s=1.):
    return (1./(s*np.sqrt(2*np.pi)))*np.exp(-(((X - u)**2)/(2*s**2)))

#def vis(i):
#    s = 1.
#    u = 0.
#    zs = np.linspace(-1, 1, 500).astype('float32')[:,np.newaxis]
#    xs = np.linspace(-5, 5, 500).astype('float32')[:,np.newaxis]
#    ps = gaussian_likelihood(xs, 1.)
#
#    gs = generator.predict(zs)
#    print gs.mean(),gs.std()
#    preal = decoder.predict(xs)
#    kde = gaussian_kde(gs.flatten())
#
#    plt.clf()
#    plt.plot(xs, ps, '--', lw=2)
#    plt.plot(xs, kde(xs.T), lw=2)
#    plt.plot(xs, preal, lw=2)
#    plt.xlim([-5., 5.])
#    plt.ylim([0., 1.])
#    plt.ylabel('Prob')
#    plt.xlabel('x')
#    plt.legend(['P(data)', 'G(z)', 'D(x)'])
#    plt.title('GAN learning gaussian')
#    fig.canvas.draw()
#    plt.show(block=False)
#    if i%100 == 0:
#        plt.savefig('current.png')
#    plt.pause(0.01)

fig = plt.figure()
epochs = 5000
for i in range(epochs+1):
    print i
    zmb = np.random.uniform(0, 36, size=(batch_size, dec_input_num, 1)).astype('float32')
    # xmb = np.random.normal(1., 1, size=(batch_size, 1)).astype('float32')
    # xmb = np.array([data[n:n+seq_length] for n in np.random.randint(0,data.shape[0]-seq_length,batch_size)])
    X = numpy.reshape(data, (len(data), 50, 1))
    xmb = np.array([data[n, :] for n in np.random.randint(0, data.shape[0], batch_size)])
    if i % 10 == 0:
        r = gen_dec.fit(zmb,y_gen_dec,epochs=1,verbose=0)
        print('E:',np.exp(sum(r.history['loss'])/batch_size))
    else:
        r = decoder.fit(np.vstack([generator.predict(zmb),xmb]),y_decode,epochs=1,verbose=0)
        print('D:',np.exp(sum(r.history['loss'])/batch_size))

    if i % (float(epochs)/10) == 0:
        print("saving fakes")
        fakes = generator.predict(zmb[:16,:])
        for n in range(16):
            np.save('simpleResults\\fake_'+str(i)+"_"+str(n+1), fakes[n, :])
            np.save('simpleResults\\real_'+str(i)+"_"+str(n+1), xmb[n, :])
#        vis(i)