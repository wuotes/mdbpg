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
from sys import stderr
from typing import Type

import mtoml
import os
import psycopg2
import psycopg2.extras

#######################################################################
#                                                                     #
#         POSTGRES                                                    #
#                                                                     #
#######################################################################
class postgres():
    ###################################################################
    #     CONSTRUCTOR, INSTANCE VARIABLES                             #
    ###################################################################
    def __init__(self: r'postgres', use_env_vars: bool = False):
        if use_env_vars is True:
            self.username: str = os.getenv(r'POSTGRES_USERNAME')
            self.password: str = os.getenv(r'POSTGRES_PASSWORD')
            self.hostname: str = os.getenv(r'POSTGRES_HOSTNAME')
            self.hostport: str = r''
            self.dbname: str = os.getenv(r'POSTGRES_DBNAME')

        else:
            if mtoml.is_loaded(r'database') is False:
                if mtoml.load(r'database') is False:
                    print('[{0}] Failed to load the \'database\' configuration.'.format(datetime.now().strftime('%m/%d %I:%M %p')), file=stderr)

            self.username: str = mtoml.get(r'database', r'postgres_username')
            self.password: str = mtoml.get(r'database', r'postgres_password')
            self.hostname: str = mtoml.get(r'database', r'postgres_hostname')
            self.hostport: str = mtoml.get(r'database', r'postgres_hostport')
            self.dbname: str = mtoml.get(r'database', r'postgres_dbname')

        if self.username is None or self.password is None or self.hostname is None or self.hostport is None or self.dbname is None:
            self.loaded = False

            print('[{0}] Failed to load the configuration for Postgres.'.format(datetime.now().strftime('%m/%d %I:%M %p')), file=stderr)

        else:
            self.loaded = True

    ###################################################################
    #     FETCH                                                       #
    ###################################################################
    def fetch(self: r'postgres', sql_query: str) -> list:
        if self.loaded is False:
            return None

        dbconn: Type[psycopg2.connection] = None
        dbcursor: Type[psycopg2.cursor] = None
        dbresult: list = []

        try:
            if r'' == str(self.hostport):
                dbconn = psycopg2.connect(host=str(self.hostname), database=str(self.dbname), user=str(self.username), password=str(self.password))

            else:
                dbconn = psycopg2.connect(host=str(self.hostname), port=int(self.hostport), database=str(self.dbname), user=str(self.username), password=str(self.password))

            dbcursor = dbconn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            dbcursor.execute(sql_query)
            dbresult = list(dbcursor.fetchall())

        except psycopg2.ProgrammingError as sql_exception:
            dbresult = None

            print('[{0}] An exception was thrown while trying to run a fetch query on the Postgres database \'{1}\' due to a query error: {2}.'.format(datetime.now().strftime('%m/%d %I:%M %p'), self.dbname, str(sql_exception)), file=stderr)

        except Exception as sql_exception:
            dbresult = None

            print('[{0}] An exception was thrown while trying to run a fetch query on the Postgres database \'{1}\': {2}.'.format(datetime.now().strftime('%m/%d %I:%M %p'), self.dbname, str(sql_exception)), file=stderr)

        finally:
            if dbcursor:
                dbcursor.close()

            if dbconn:
                dbconn.close()

        return dbresult

    ###################################################################
    #     COMMIT                                                      #
    ###################################################################
    def commit(self: r'postgres', sql_query: str) -> bool:
        if self.loaded is False:
            return False

        dbconn: Type[psycopg2.connection] = None
        dbcursor: Type[psycopg2.cursor] = None
        dbresult: bool = True

        try:
            dbconn = psycopg2.connect(host=self.hostname, port=self.hostport, database=self.dbname, user=self.username, password=self.password)
            dbcursor = dbconn.cursor()

            dbcursor.execute(sql_query)
            dbconn.commit()

        except psycopg2.ProgrammingError as sql_exception:
            dbresult = False

            print('[{0}] An exception was thrown while trying to run an update query on the Postgres database \'{1}\' due to a query error: {2}.'.format(datetime.now().strftime('%m/%d %I:%M %p'), self.dbname, str(sql_exception)), file=stderr)

        except Exception as sql_exception:
            dbresult = False
            
            print('[{0}] An exception was thrown while trying to run an update query on the Postgres database \'{1}\': {2}.'.format(datetime.now().strftime('%m/%d %I:%M %p'), self.dbname, str(sql_exception)), file=stderr)

        finally:
            if dbcursor:
                dbcursor.close()

            if dbconn:
                dbconn.close()

        return dbresult

    ###################################################################
    #     FIND                                                        #
    ###################################################################
    def find(self: r'postgres', table: str, criteria: dict) -> list:
        sql_query: str = r'SELECT * FROM ' + table

        if criteria is None or 0 == len(criteria.keys()):
            return self.fetch(sql_query)

        sql_query += r' WHERE '

        for column in criteria.keys():
            if type(criteria[column]) is str:
                sql_query += column + r"='" + str(criteria[column]) +r"',"

            else:
                sql_query += column + r'=' + str(criteria[column]) +r','

        sql_query = sql_query[:-1] + r';'

        return self.fetch(sql_query)

    ###################################################################
    #     INSERT                                                      #
    ###################################################################
    def insert(self: r'postgres', table: str, rows: list) -> bool:
        result: bool = True

        if rows is None or 0 == len(rows):
            return False

        for row in rows:
            sql_query: str = r'INSERT INTO ' + table + r'('

            if row is None or 0 == len(row.keys()):
                result = False

                continue

            for column in row.keys():
                sql_query += column + r','

            sql_query = sql_query[:-1] + r')' + '\n' + r'VALUES('

            for column in row.keys():
                if type(row[column]) is str:
                    sql_query += r"'" + str(row[column]) + r"',"

                else:
                    sql_query += str(row[column]) + r','

            sql_query = sql_query[:-1] + r');'

            result &= self.commit(sql_query)

        return result

    ###################################################################
    #     UPDATE                                                      #
    ###################################################################
    def update(self: r'postgres', table: str, criteria: dict, changes: dict) -> bool:
        sql_query: str = r'UPDATE ' + table + '\n' + r'SET '

        if changes is None or 0 == len(changes.keys()):
            return False

        for column in changes.keys():
            if type(changes[column]) is str:
                sql_query += column + r"='" + str(changes[column]) +r"',"

            else:
                sql_query += column + r'=' + str(changes[column]) +r','

        if criteria is None or 0 == len(criteria.keys()):
            return self.commit(sql_query[:-1])

        sql_query = sql_query[:-1] + '\n' + r'WHERE '

        for column in criteria.keys():
            if type(criteria[column]) is str:
                sql_query += column + r"='" + str(criteria[column]) +r"',"

            else:
                sql_query += column + r'=' + str(criteria[column]) +r','

        sql_query = sql_query[:-1] + r';'

        return self.commit(sql_query)
    
    ###################################################################
    #     DELETE                                                      #
    ###################################################################
    def delete(self: r'postgres', table: str, criteria: dict) -> bool:
        sql_query: str = r'DELETE FROM ' + table + r' WHERE '

        if criteria is None or 0 == len(criteria.keys()):
            return False

        for column in criteria.keys():
            if type(criteria[column]) is str:
                sql_query += column + r"='" + str(criteria[column]) +r"',"

            else:
                sql_query += column + r'=' + str(criteria[column]) +r','

        sql_query = sql_query[:-1] + r';'

        return self.commit(sql_query)