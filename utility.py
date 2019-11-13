"""
Created on 3 Nov 2019
@author: Jay Zern Ng, Amaury Sudrie

Utility functions to extract data from the json files
"""

import json
import os

#BASE_DIR = './example_tiny_data/'
BASE_DIR = './down_sample/'

def get_business():
    file_dir = os.path.join(BASE_DIR, 'business.json')
    with open(file_dir, 'r') as f:
        data = []
        for line in f:
            row = json.loads(line)
            # Initialize
            to_go = wifi = ambience = parking = price_range = hours = None
            # Handle attributes here
            # Get following attributes if they exists
            # Coerce them into bool and str for now
            if row['attributes']:
                if "RestaurantsTakeOut" in row['attributes']:
                    to_go = bool(row['attributes']['RestaurantsTakeOut'])
                if "WiFi" in row['attributes']:
                    wifi = bool(row['attributes']["WiFi"])
                if "Ambience" in row['attributes']:
                    ambience = str(row['attributes']["Ambience"])
                if "BusinessParking" in row['attributes']:
                    parking = bool(row['attributes']["BusinessParking"])
                if "RestaurantsPriceRange2" in row['attributes']:
                    price_range = str(
                        row['attributes']["RestaurantsPriceRange2"])
            hours = str(row['hours'])
            insert = [
                row['business_id'],
                row['name'],
                row['address'],
                row['city'],
                row['state'],
                row['postal_code'],
                row['review_count'],
                row['categories'],
                row['stars'],
                to_go,
                wifi,
                ambience,
                parking,
                price_range,
                hours
            ]
            data.append(insert)
        return data


def get_yelp_user():
    file_dir = os.path.join(BASE_DIR, 'user.json')
    with open(file_dir, 'r') as f:
        data = []
        for line in f:
            row = json.loads(line)
            insert = [
                row['user_id'],
                row['name'],
                row['yelping_since'],
                row['fans'],
                row['average_stars'],
                row['review_count']
            ]
            data.append(insert)
        return data


def get_reviews():
    file_dir = os.path.join(BASE_DIR, 'review.json')
    with open(file_dir, 'r') as f:
        data = []
        for line in f:
            row = json.loads(line)
            insert = [
                row['review_id'],
                row['business_id'],
                row['user_id'],
                row['date'],
                row['stars'],
                row['text'],
                row['useful']
            ]
            data.append(insert)
        return data


def get_tips():
    file_dir = os.path.join(BASE_DIR, 'tip.json')
    with open(file_dir, 'r') as f:
        data = []
        for line in f:
            row = json.loads(line)
            insert = [
                row['business_id'],
                row['user_id'],
                row['compliment_count'],
                row['date'],
                row['text']
            ]
            data.append(insert)
        return data


def get_checkins():
    """Rearrange dates to pairs here"""
    file_dir = os.path.join(BASE_DIR, 'checkin.json')
    with open(file_dir, 'r') as f:
        data = []
        for line in f:
            row = json.loads(line)
            data.append(row)

        # Rearrange data
        rearranged_data = []
        for i in range(len(data)):
            date_list = [x.strip() for x in data[i]['date'].split(',')]
            business_id_list = [
                data[i]['business_id'] for x in data[i]['date'].split(',')]
            business_checkins = list(zip(business_id_list, date_list))
            rearranged_data = rearranged_data + business_checkins
        data = rearranged_data
        return data


def get_media():
    file_dir = os.path.join(BASE_DIR, 'photo.json')
    with open(file_dir, 'r') as f:
        data = []
        for line in f:
            row = json.loads(line)

            # TODO: get blob data
            blob = None

            insert = [
                row['photo_id'],
                row['business_id'],
                blob,
                row['caption']
            ]
            data.append(insert)
        return data
