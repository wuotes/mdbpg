# mdbpq
A Python module that can handle both Postgres and MongoDB queries in an interchangable manner.

`pip install mdbpg`

[![codefactor](https://www.codefactor.io/repository/github/wuotes/mdbpg/badge?style=plastic)](https://www.codefactor.io/repository/github/wuotes/mdbpg/) [![circleci](https://circleci.com/gh/wuotes/mdbpg.svg?style=shield)](https://app.circleci.com/pipelines/github/wuotes/mdbpg) [![codecov](https://codecov.io/gh/wuotes/mdbpg/branch/main/graph/badge.svg)](https://codecov.io/gh/wuotes/mdbpg)

```
import mdbpg

# create an instance for Postgres or MongoDB through mdbpg
# max_conns and use_env_vars are both optional parameters
# max_conns defaults to 10 and use_env_vars defaults to False
# mdbpg will try to load a toml config named 'database.toml'
# with the relevant fields using mtoml
pgdb = mdbpg.postgres(max_conns=5, use_env_vars=True)
mdb = mdbpg.mongodb(max_conns=50, use_env_vars=True)

# both methods work in the same manner, you specify the
# table/collection with the first parameter and then pass
# a dict containing the parameters and values you want
# the function then returns either None if something went
# wrong or a list of dict results
result_list = pgdb.find('dogs', { 'color': 'black' })
result_list = mdb.find('dogs', { 'color': 'black' })
# the benefit of this is that you can build queries in the
# same manner for both databases and expect it to just work

# again these are equivalent, though there are differences
# between how Postgres and MongoDB will view these calls
# for MongoDB this is the entire object, where as with Postgres
# this may only be a few columns and so when setting up your
# table in Postgres it would be ideal to set default values
pgdb.insert('dogs', { 'breed': 'pitbull', 'color': 'white', 'cuteness': 9000.01 })
mdb.insert('dogs', { 'breed': 'pitbull', 'color': 'white', 'cuteness': 9000.01 })
# both Postgres and MongoDB contain the same methods:
# find, insert, update, delete
# though postgres.insert() is the only method with a gotcha like that

# Postgres has two additional methods which handle SQL queries
# both methods can be used to run any valid SQL query except that
# postgres.fetch() expects a result to be returned from the query
# where as postgres.commit() does not
result_list = pgdb.fetch("SELECT * FROM 'dogs' WHERE breed = 'hound'")
pgdb.commit("DELETE FROM 'dogs' WHERE breed = 'hound'")
```