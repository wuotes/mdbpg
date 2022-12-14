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

import mdbpg

#######################################################################
#                                                                     #
#         TESTS                                                       #
#                                                                     #
#######################################################################
mtoml.set_dir(r'./tests/')  # set mtoml's working directory

if os.path.exists(mtoml.get_dir() + r'database.toml') is True:
    # this is just so I can run tests on my local device without
    # setting up env vars
    pgdb = mdbpg.postgres(max_conns=0, use_env_vars=False)
    mdb = mdbpg.mongodb(max_conns=0, use_env_vars=False)

    bad_pgdb = mdbpg.postgres(max_conns=10)
    bad_mdb = mdbpg.mongodb(max_conns=10)

else:
    pgdb = mdbpg.postgres(max_conns=0)
    mdb = mdbpg.mongodb(max_conns=0)

    bad_pgdb = mdbpg.postgres(max_conns=10, use_env_vars=False)
    bad_mdb = mdbpg.mongodb(max_conns=10, use_env_vars=False)

def test_pgdb_commit_fetch():
    assert pgdb.commit(r'DELETE FROM TESTTBL') is True
    assert (0 == len(pgdb.fetch(r'SELECT * FROM TESTTBL'))) is True

def test_pgdb_find_insert():
    assert (0 == len(pgdb.find(r'TESTTBL', {}))) is True
    assert pgdb.insert(r'TESTTBL', {r'testvar1': True, r'testvar2': 43, r'testvar3': r'test1'}) is True
    assert (0 < len(pgdb.find(r'TESTTBL', {r'testvar1': True}))) is True
    assert (0 < len(pgdb.find(r'TESTTBL', {r'testvar3': r'test1'}))) is True

def test_pgdb_find_update():
    assert (0 == len(pgdb.find(r'TESTTBL', {r'testvar2': 13}))) is True
    assert (0 < len(pgdb.find(r'TESTTBL', {r'testvar2': 43}))) is True
    assert pgdb.update(r'TESTTBL', {r'testvar1': True}, {r'testvar2': 13}) is True
    assert pgdb.update(r'TESTTBL', {r'testvar3': r'test1'}, {r'testvar3': r'test1'}) is True
    assert pgdb.update(r'TESTTBL', {}, {r'testvar3': r'test1'}) is True
    assert pgdb.update(r'TESTTBL', {r'testvar3': r'test1'}, {}) is False
    assert (0 < len(pgdb.find(r'TESTTBL', {r'testvar2': 13}))) is True
    assert (0 == len(pgdb.find(r'TESTTBL', {r'testvar2': 43}))) is True

def test_pgdb_find_delete():
    assert (0 < len(pgdb.find(r'TESTTBL', {r'testvar1': True}))) is True
    assert pgdb.delete(r'TESTTBL', {r'testvar3': r'test1'}) is True
    assert pgdb.delete(r'TESTTBL', {r'testvar1': True}) is True
    assert pgdb.delete(r'TESTTBL', {}) is False
    assert (0 == len(pgdb.find(r'TESTTBL', {r'testvar1': True}))) is True

def test_pgdb_bad_commit_fetch():
    assert bad_pgdb.commit(r'DELETE FROM TESTTBL') is False
    assert bad_pgdb.fetch(r'SELECT * FROM TESTTBL') is None

def test_pgdb_bad_insert():
    assert bad_pgdb.insert(r'TESTTBL', {r'testvar1': True, r'testvar2': 43, r'testvar3': r'test1'}) is False
    assert bad_pgdb.insert(r'TESTTBL', {}) is False
    
def test_pgdb_bad_update():
    assert bad_pgdb.update(r'TESTTBL', {r'testvar1': True}, {r'testvar2': 13}) is False

def test_pgdb_bad_find():
    assert bad_pgdb.find(r'TESTTBL', {r'testvar1': True}) is None

def test_pgdb_bad_delete():
    assert bad_pgdb.delete(r'TESTTBL', {r'testvar3': r'test1'}) is False

def test_pgdb_fake_commit_fetch():
    bad_pgdb.loaded = True
    bad_pgdb.hostname = r'TEST-FAKE'
    assert bad_pgdb.commit(r'DELETE FROM TESTTBL') is False
    assert bad_pgdb.commit(r'TEST FAKE') is False
    assert bad_pgdb.fetch(r'SELECT * FROM TESTTBL') is None
    assert bad_pgdb.fetch(r'TEST FAKE') is None

def test_pgdb_fake_insert():
    assert bad_pgdb.insert(r'TESTTBL', {r'testvar1': True, r'testvar2': 43, r'testvar3': r'test1'}) is False
    
def test_pgdb_fake_update():
    assert bad_pgdb.update(r'TESTTBL', {r'testvar1': True}, {r'testvar2': 13}) is False

def test_pgdb_fake_find():
    assert bad_pgdb.find(r'TESTTBL', {r'testvar1': True}) is None

def test_pgdb_fake_delete():
    assert bad_pgdb.delete(r'TESTTBL', {r'testvar3': r'test1'}) is False

def test_mdb_delete_find():
    assert mdb.delete(r'test', {}) is True
    assert (0 == len(mdb.find(r'test', {}))) is True

def test_mdb_insert_find():
    assert mdb.insert(r'test', {r'testval1': True, r'testval2': 43, r'testval3': r'test'}) is True
    assert (0 < len(mdb.find(r'test', {r'testval1': True}))) is True

def test_mdb_update_find():
    assert mdb.update(r'test', {r'testval2': 43}, {r'testval3': r'changed'}) is True
    assert (0 == len(mdb.find(r'test', {r'testval3': r'test'}))) is True
    assert (0 < len(mdb.find(r'test', {r'testval3': r'changed'}))) is True

def test_mdb_cleanup():
    assert mdb.delete(r'test', {r'testval1': True}) is True
    assert (0 == len(mdb.find(r'test', {}))) is True

def test_mdb_bad_insert():
    bad_mdb.connstr = r''
    assert bad_mdb.insert(r'test', {r'testval1': True, r'testval2': 43, r'testval3': r'test'}) is False

def test_mdb_bad_find():
    assert bad_mdb.find(r'test', {}) is None

def test_mdb_bad_update():
    assert bad_mdb.update(r'test', {}, {r'testval3': r'changed'}) is False

def test_mdb_bad_delete():
    assert bad_mdb.delete(r'test', {}) is False

def test_mdb_fake_insert():
    bad_mdb.connstr = r'TEST-FAKE'
    assert bad_mdb.insert(r'test', {r'testval1': True, r'testval2': 43, r'testval3': r'test'}) is False

def test_mdb_fake_find():
    assert bad_mdb.find(r'test', {}) is None

def test_mdb_fake_update():
    assert bad_mdb.update(r'test', {}, {r'testval3': r'changed'}) is False

def test_mdb_fake_delete():
    assert bad_mdb.delete(r'test', {}) is False