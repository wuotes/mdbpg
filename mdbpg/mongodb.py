#######################################################################
# Copyright (c) 2022 Jordan Schaffrin                                 #
#                                                                     #
# This Source Code Form is subject to the terms of the Mozilla Public #
# License, v. 2.0. If a copy of the MPL was not distributed with this #
# file, You can obtain one at http://mozilla.org/MPL/2.0/.            #
#######################################################################

#######################################################################
#                                                                     #
#         IMPORTS                                                     #
#                                                                     #
#######################################################################
from datetime import datetime
from pymongo import MongoClient
from sys import stderr

import mtoml
import os

#######################################################################
#                                                                     #
#         MONGODB                                                     #
#                                                                     #
#######################################################################
class mongodb():
    ###################################################################
    #     CONSTRUCTOR, INSTANCE VARIABLES                             #
    ###################################################################
    def __init__(self: r'mongodb', use_env_vars: bool = False) -> None:
        if use_env_vars is True:
            self.username: str = os.getenv(r'MONGODB_USERNAME')
            self.password: str = os.getenv(r'MONGODB_PASSWORD')
            self.hostname: str = os.getenv(r'MONGODB_HOSTNAME')
            self.authsrc: str = r''
            self.dbname: str = os.getenv(r'MONGODB_DBNAME')

        else:
            if mtoml.is_loaded(r'database') is False:
                if mtoml.load(r'database') is False:
                    print('[{0}] Failed to load the \'database\' configuration.'.format(datetime.now().strftime('%m/%d %I:%M %p')), file=stderr)

            self.username: str = mtoml.get(r'database', r'mongodb_username')
            self.password: str = mtoml.get(r'database', r'mongodb_password')
            self.hostname: str = mtoml.get(r'database', r'mongodb_hostname')
            self.authsrc: str = mtoml.get(r'database', r'mongodb_authsrc')
            self.dbname: str = mtoml.get(r'database', r'mongodb_dbname')

        if self.username is None or self.password is None or self.hostname is None or self.authsrc is None or self.dbname is None:
            self.connstr = r''

            print('[{0}] Failed to load the configuration for MongoDB.'.format(datetime.now().strftime('%m/%d %I:%M %p')), file=stderr)

        else:
            self.connstr = r'mongodb+srv://' + str(self.username) + r':' + str(self.password) + r'@' + str(self.hostname) + r'/?retryWrites=true&w=majority'

            if 0 < len(str(self.authsrc)):
                self.connstr += r'&authSource=' + str(self.authsrc)

    ###################################################################
    #     FIND                                                        #
    ###################################################################
    def find(self: r'mongodb', collection: str, criteria: dict) -> list:
        dbresult: list = None

        if r'' == self.connstr:
            return dbresult

        try:
            dbresult = list(MongoClient(self.connstr)[str(self.dbname)][collection].find(criteria))

        except Exception as mongodb_exception:
            print('[{0}] An exception was thrown while trying to find a document from the collection \'{1}\' using MongoDB: {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), collection, str(mongodb_exception)), file=stderr)

        return dbresult

    ###################################################################
    #     INSERT                                                      #
    ###################################################################
    def insert(self: r'mongodb', collection: str, document: dict) -> bool:
        result: bool = True

        if r'' == self.connstr:
            return False

        try:
            MongoClient(self.connstr)[str(self.dbname)][collection].insert_one(document)

        except Exception as mongodb_exception:
            result = False

            print('[{0}] An exception was thrown while trying to insert a document from the collection \'{1}\' using MongoDB: {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), collection, str(mongodb_exception)), file=stderr)

        return result

    ###################################################################
    #     UPDATE                                                      #
    ###################################################################
    def update(self: r'mongodb', collection: str, criteria: dict, changes: dict) -> bool:
        result: bool = True

        if r'' == self.connstr:
            return False

        try:
            MongoClient(self.connstr)[str(self.dbname)][collection].update_many(criteria, { r'$set': changes })

        except Exception as mongodb_exception:
            result = False

            print('[{0}] An exception was thrown while trying to update a document from the collection \'{1}\' using MongoDB: {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), collection, str(mongodb_exception)), file=stderr)

        return result

    ###################################################################
    #     DELETE                                                      #
    ###################################################################
    def delete(self: r'mongodb', collection: str, criteria: dict) -> bool:
        result: bool = True

        if r'' == self.connstr:
            return False

        try:
            MongoClient(self.connstr)[str(self.dbname)][collection].delete_many(criteria)

        except Exception as mongodb_exception:
            result = False

            print('[{0}] An exception was thrown while trying to delete a document from the collection \'{1}\' using MongoDB: {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), collection, str(mongodb_exception)), file=stderr)

        return result
