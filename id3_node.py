#! /usr/bin/env python

class node:
    feature_label = None
    left_node = None
    right_node = None
    left_data = None
    right_data = None
    is_pure = False
    class_prediction = None
    parent = None

    def __init__(self, feature_label, left_data, right_data):
        if (feature_label != None):
            self.feature_label = feature_label
            self.left_data = left_data
            self.right_data = right_data

