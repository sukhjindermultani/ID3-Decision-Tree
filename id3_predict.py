#! /usr/bin/env python

import pickle
from id3_node import node


def predict(line, root_node, feature_labels):
    #takes a data point and classifies it.

    if (root_node == None):
        #Data not present in training set.
        return 1 #biased towards positive class

    if (root_node.is_pure):
        return root_node.class_prediction

    split_feature = root_node.feature_label
    split_index = feature_labels.index(split_feature)

    if line[split_index] == '0':
        return predict(line, root_node.left_node, feature_labels)
    else:
        return predict(line, root_node.right_node, feature_labels)


def find_error(data, root_node, feature_labels):

    confusion_matrix = [[0,0], [0,0]]
    errors = 0
    for line in data:
        predicted_label = predict(line, root_node, feature_labels)
        confusion_matrix[predicted_label][int(line[-1])] += 1
        if predicted_label != int(line[-1]):
            errors += 1

    print 100 - (errors/float(len(data)) * 100)
    print confusion_matrix

    return errors

        

def main(input_file, m):

    root_node = None 
    with open('root_node' + str(m), 'r') as f:
        root_node = pickle.load(f)

    if root_node == None:
        return

    raw_data = []
    with open(input_file, 'r') as f:
        raw_data = f.readlines()

    feature_labels = raw_data[0].strip().split(',')
    data = [x.strip().split(',') for x in raw_data[1:]]

    print "Unpruned tree on " + input_file
    print find_error(data, root_node, feature_labels)

    with open('pruned_root_node' + str(m), 'r') as f:
        root_node = pickle.load(f)
                                                    
    if root_node == None:
        return
                                                    
    raw_data = []
    with open(input_file, 'r') as f:
        raw_data = f.readlines()
                                                    
    feature_labels = raw_data[0].strip().split(',')
    data = [x.strip().split(',') for x in raw_data[1:]]
          
    print "Pruned Tree on " +  input_file                                         
    print find_error(data, root_node, feature_labels)


if __name__ == '__main__':
    main('Data/data_sets1/validation_set.csv', 1)
    main('Data/data_sets1/test_set.csv', 1)
    main('Data/data_sets2/validation_set.csv', 2)
    main('Data/data_sets2/test_set.csv', 2)
