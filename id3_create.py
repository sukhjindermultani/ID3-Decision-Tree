#! /usr/bin/env python

import math

import pickle
from id3_node import node


def find_majority_label(data):
    #Find majority label, biased towards positive data
    pos_count = 0

    for element in data:
        pos_count += int(element[-1])

    neg_count = len(data) - pos_count

    if (neg_count > pos_count):
        return 0

    return 1 

def is_pure_data(data):
    label = data[0][-1]
    for element in data:
        if element[-1] != label:
            return False, None

    return True, int(label)

def split_data(data, feature_index):
    #returns two datasets which are classified based on the feature sets
    pos_set = list()
    neg_set = list()
    for element in data:
        if element[feature_index] == '1':
            pos_set.append(element)
        else:
            neg_set.append(element)

    return neg_set, pos_set

def find_entropy(data):
    #Finds entropy on a list of data based on the class values
    if len(data) == 0:
        return 0

    pos_count = 0

    for element in data:
        if element[-1] == '1':
            pos_count += 1 

    total_count = len(data)
    neg_count = total_count - pos_count

    p_pos = pos_count/float(total_count)
    p_neg = neg_count/float(total_count)
    
    if p_pos == 0.0 or p_neg == 0.0:
        return 0

    entropy = ( -1 * p_pos * math.log(p_pos)) + ( -1 * p_neg * math.log(p_neg))

    return entropy


def find_conditional_entropy(data, feature_index):
    #Finds the conditional entropy on the given dataset with all the features in the list of features
    if len(data) == 0:
        return 0

    neg_set, pos_set = split_data(data, feature_index)
    total_count = len(data)
    pos_count = len(pos_set)
    neg_count = len(neg_set)
    
    pos_entropy = find_entropy(pos_set)
    neg_entropy = find_entropy(neg_set)

    conditional_entropy = ( (pos_count/float(total_count)) * pos_entropy ) + ( (neg_count/float(total_count)) * neg_entropy )
    return conditional_entropy 



def create_tree(data, feature_labels):
    #Creates a tree given data set and features.
    #First check if this node is a leaf
    is_pure, label = is_pure_data(data)
    if (is_pure):
        leaf_node = node(None, None, None)
        leaf_node.is_pure = True
        leaf_node.class_prediction = label
        return leaf_node

    #If no more features left, return an impure node with majority label
    if feature_labels.count(None) == len(feature_labels):
        leaf_node = node(None, None, None)
        leaf_node.is_pure = True
        leaf_node.class_prediction = find_majority_label(data)

        return leaf_node 

    #Find the feature to split on
    conditional_entropy = 1
    split_feature_index = 0

    current_entropy = find_entropy(data)
    for feature in feature_labels:
        if feature == None:
            continue
        feature_index = feature_labels.index(feature)
        feature_conditional_entropy = find_conditional_entropy(data, feature_index)
        if feature_conditional_entropy <= conditional_entropy:
            conditional_entropy = feature_conditional_entropy
            split_feature_index = feature_index
   
    split_feature_label = feature_labels[split_feature_index]
    print "splitting using " +  split_feature_label 
    feature_labels[split_feature_index] = None

    neg_set, pos_set = split_data(data, split_feature_index) 

    root_node = node(split_feature_label, neg_set, pos_set)
    if (len(root_node.left_data) > 0):
        root_node.left_node = create_tree(root_node.left_data, feature_labels[:])
        root_node.left_node.parent = root_node
    if (len(root_node.right_data) > 0):
        root_node.right_node = create_tree(root_node.right_data, feature_labels[:])
        root_node.right_node.parent = root_node

    root_node.class_prediction = find_majority_label(data)
    return root_node


def main(n):
    with open("Data/data_sets" + str(n) + "/training_set.csv", 'r') as f:
        raw_data = f.readlines()

    feature_labels = raw_data[0].strip().split(',')[:-1]
    data = [x.strip().split(',') for x in raw_data[1:]] #Data contains all the training data

    remaining_features = feature_labels[:]
    root_node = create_tree(data, remaining_features)
    traverse_node = root_node
    while(traverse_node.feature_label != None):
        print traverse_node.feature_label
        traverse_node = traverse_node.left_node
    print root_node.left_node.feature_label

    with open('root_node' + str(n), 'w') as f:
        pickle.dump(root_node, f)


if __name__ == '__main__':
    main(1)
    main(2)
