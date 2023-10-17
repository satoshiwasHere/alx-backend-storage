#!/usr/bin/env python3
"""
Python function listing all documents in a collection
Return an empty list if no document in the collection
"""


def list_all(mongo_collection):
    """
    List all docs in a collection
    """
    documents = mongo_collection.find()

    if documents.count() == 0:
        return []

    return documents
