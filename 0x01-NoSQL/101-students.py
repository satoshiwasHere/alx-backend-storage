#!/usr/bin/env python3
"""
Function returns all students sorted by average score
average score returns with key = 'averageScore'
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """

    top_st = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_st
