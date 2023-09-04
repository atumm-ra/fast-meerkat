#!/bin/bash

echo '################ MONGO ENTRYPOINT START ################';


ls -la /var/log/
# Start MongoDB with authentication enabled
mongod --auth --logpath /var/log/mongodb.log

# Initialize databases and users
mongo -- "$MONGO_INITDB_DATABASE" <<"EOF"
db.auth(getenv("MONGO_INITDB_ROOT_USERNAME"), getenv("MONGO_INITDB_ROOT_PASSWORD"))

db = db.getSiblingDB(getenv("MONGO_DB"));
db.createUser(
  {
    user: getenv("MONGO_USER"),
    pwd: getenv("MONGO_PASS"),
    roles: [{ role: 'readWrite', db: getenv("MONGO_DB") }],
  },
);
db.createCollection('tmp');

db = db.getSiblingDB(getenv("MONGO_TEST_DB"));
db.createUser(
  {
    user: getenv("MONGO_TEST_USER"),
    pwd: getenv("MONGO_TEST_PASS"),
    roles: [
      { role: 'readWrite', db: getenv("MONGO_TEST_DB") },
      { role: 'dbAdmin', db: getenv("MONGO_TEST_DB") }
    ],
  },
);
db.createCollection('tmp');
EOF

# Keep MongoDB running
mongod --shutdown
exec mongod
