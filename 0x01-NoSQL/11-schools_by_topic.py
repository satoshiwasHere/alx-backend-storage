#!/usr/bin/env python3
"""
Function returns the list of school having a specific topic
'topic' (string) will be topic searched
"""


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school having  specific 'topics'
    """
    documents = mongo_collection.find({"topics": topic})
    list_docs = [d for d in documents]
    return list_docs
