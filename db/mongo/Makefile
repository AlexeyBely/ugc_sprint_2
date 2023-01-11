all: config_mongo

config_mongo: config_servers shard_1 shard_2 collection

config_servers:
	docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
	sleep 2
	docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'

shard_1:
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
	sleep 2
	docker exec -it mongors1n1 bash -c 'echo "rs.status()" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
	sleep 2

shard_2:
	docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh' 
	sleep 2
	docker exec -it mongors2n1 bash -c 'echo "rs.status()" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
	sleep 2

collection:
	docker exec -it mongors1n1 bash -c 'echo "use actionsDb" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"actionsDb\")" | mongosh'
	docker exec -it mongos1 bash -c 'echo "db.createCollection(\"actionsDb.likes\")" | mongosh' 
	docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"actionsDb.likes\", {\"user_id\": \"hashed\"})" | mongosh'
	docker exec -it mongos1 bash -c 'echo "db.createCollection(\"actionsDb.reviews\")" | mongosh' 
	docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"actionsDb.reviews\", {\"user_id\": \"hashed\"})" | mongosh'
	docker exec -it mongos1 bash -c 'echo "db.createCollection(\"actionsDb.bookmarks\")" | mongosh' 
	docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"actionsDb.bookmarks\", {\"user_id\": \"hashed\"})" | mongosh' 



 