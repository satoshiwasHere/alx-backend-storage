#!/usr/bin/env python3
"""
function that inserts a new document in a collection based on kwargs
Returns the new _id
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a document in a collection using kwargs
    """
    data = mongo_collection.insert_one(kwargs)
    return data.inserted_id
