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
import os
import sys
import mtoml
from mtoml import mtoml

sys.path.append(r'.')

import mdbpq

#######################################################################
#                                                                     #
#         TESTS                                                       #
#                                                                     #
#######################################################################
mtoml.set_dir(r'./tests/')  # set mtoml's working directory

if os.path.exists(mtoml.get_dir() + r'database.toml') is True:
    pgdb = mdbpq.postgres()
    mdb = mdbpq.mongodb()

else:
    pgdb = mdbpq.postgres(use_env_vars=True)
    mdb = mdbpq.mongodb(use_env_vars=True)

def test_pgdb_commit_fetch():
    assert pgdb.commit(r'DELETE FROM TESTTBL') is True
    assert (0 == len(pgdb.fetch(r'SELECT * FROM TESTTBL'))) is True

def test_pgdb_find_insert():
    assert (0 == len(pgdb.find(r'TESTTBL', {r'testvar1': True}))) is True
    assert pgdb.insert(r'TESTTBL', [{r'testvar1': True, r'testvar2': 43, r'testvar3': r'test1'}]) is True
    assert pgdb.insert(r'TESTTBL', [{r'testvar1': False, r'testvar2': 3, r'testvar3': r'test1'}, {r'testvar1': False, r'testvar2': 7, r'testvar3': r'test1'}])
    assert (1 == len(pgdb.find(r'TESTTBL', {r'testvar1': True}))) is True
    assert (2 == len(pgdb.find(r'TESTTBL', {r'testvar1': False}))) is True

def test_pgdb_find_update():
    assert (0 == len(pgdb.find(r'TESTTBL', {r'testvar2': 13}))) is True
    assert (1 == len(pgdb.find(r'TESTTBL', {r'testvar2': 43}))) is True
    assert pgdb.update(r'TESTTBL', {r'testvar1': True}, {r'testvar2': 13})
    assert (1 == len(pgdb.find(r'TESTTBL', {r'testvar2': 13}))) is True
    assert (0 == len(pgdb.find(r'TESTTBL', {r'testvar2': 43}))) is True

def test_pgdb_find_delete():
    assert (1 == len(pgdb.find(r'TESTTBL', {r'testvar1': True}))) is True
    assert pgdb.delete(r'TESTTBL', {r'testvar3': r'test1'}) is True
    assert (0 == len(pgdb.find(r'TESTTBL', {r'testvar1': True}))) is True

def test_mdb_delete_find():
    assert mdb.delete(r'test', {}) is True
    assert (0 == len(mdb.find(r'test', {}))) is True

def test_mdb_insert_find():
    assert mdb.insert(r'test', [{r'testval1': True, r'testval2': 43, r'testval3': r'test'}]) is True
    assert mdb.insert(r'test', [{r'testval1': False, r'testval2': 3, r'testval3': r'dog'}, {r'testval1': False, r'testval2': 7, r'testval3': r'cat'}])
    assert (0 < len(mdb.find(r'test', {r'testval1': True}))) is True

def test_mdb_update_find():
    assert mdb.update(r'test', {r'testval2': 43}, {r'testval3': r'changed'}) is True
    assert (0 == len(mdb.find(r'test', {r'testval3': r'test'}))) is True
    assert (0 < len(mdb.find(r'test', {r'testval3': r'changed'}))) is True

def test_mdb_cleanup():
    assert mdb.delete(r'test', {r'testval1': True}) is True
    assert mdb.delete(r'test', {r'testval1': False}) is True
    assert (0 == len(mdb.find(r'test', {}))) is True
