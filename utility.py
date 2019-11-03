"""
Created on 3 Nov 2019
@author: Jay Zern Ng, Amaury Sudrie

Utility functions to extract data from the json files
"""

import json
import os

# Tiny dataset
#BASE_DIR = './example_tiny_data/'

# Actual dataset
BASE_DIR = '../data'
PHOTOS_DIR = '../photos'

def get_business_list():
    file_dir = os.path.join(BASE_DIR, 'business.json')
    data = []
    with open(file_dir) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_yelp_user_list():
    file_dir = os.path.join(BASE_DIR, 'user_tiny.json')
    data = []
    with open(file_dir) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_reviews_list():
    file_dir = os.path.join(BASE_DIR, 'review_tiny.json')
    data = []
    with open(file_dir) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_tips_list():
    file_dir = os.path.join(BASE_DIR, 'tip_tiny.json')
    data = []
    with open(file_dir) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_checkins_list():
    file_dir = os.path.join(BASE_DIR, 'checkin_tiny.json')
    data = []
    with open(file_dir) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_photos_list():
    file_dir = os.path.join(PHOTOS_DIR, 'photo_tiny.json')
    data = []
    with open(file_dir) as f:
        for line in f:
            data.append(json.loads(line))
    return data

print(get_business_list())
