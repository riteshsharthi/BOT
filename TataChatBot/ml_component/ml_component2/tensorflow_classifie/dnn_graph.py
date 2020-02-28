import tflearn
import tensorflow as tf
import  os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def dnn_graph(train_x, train_y):
    try:
        tf.reset_default_graph()
        # Build neural network
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)
    
        # Define model and setup tensorboard
        model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        
    except Exception as e:
        print ("Exception in dnn graph building", e)
        
    
    return model