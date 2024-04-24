#!/usr/bin/env python3
'''Task 10's module.
'''


def update_topics(mongo_collection, name, topics):
    '''Returns the list of school having a specific topic
    '''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )