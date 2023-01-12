PN=tests_action_

all: config_mongo

config_mongo: config_servers shard_1 shard_2 collection

config_servers:
	docker exec -i $(PN)mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"$(PN)mongocfg1\"}, {_id: 1, host: \"$(PN)mongocfg2\"}, {_id: 2, host: \"$(PN)mongocfg3\"}]})" | mongosh'
	sleep 2
	docker exec -i $(PN)mongocfg1 bash -c 'echo "rs.status()" | mongosh'

shard_1:
	docker exec -i $(PN)mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"$(PN)mongors1n1\"}, {_id: 1, host: \"$(PN)mongors1n2\"}, {_id: 2, host: \"$(PN)mongors1n3\"}]})" | mongosh'
	sleep 2
	docker exec -i $(PN)mongors1n1 bash -c 'echo "rs.status()" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "sh.addShard(\"mongors1/$(PN)mongors1n1\")" | mongosh'
	sleep 2

shard_2:
	docker exec -i $(PN)mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"$(PN)mongors2n1\"}, {_id: 1, host: \"$(PN)mongors2n2\"}, {_id: 2, host: \"$(PN)mongors2n3\"}]})" | mongosh'
	sleep 2
	docker exec -i $(PN)mongors2n1 bash -c 'echo "rs.status()" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "sh.addShard(\"mongors2/$(PN)mongors2n1\")" | mongosh'
	sleep 2

collection:
	docker exec -i $(PN)mongors1n1 bash -c 'echo "use actionsDb" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "sh.enableSharding(\"actionsDb\")" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "db.createCollection(\"actionsDb.likes\")" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "sh.shardCollection(\"actionsDb.likes\", {\"user_id\": \"hashed\"})" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "db.createCollection(\"actionsDb.reviews\")" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "sh.shardCollection(\"actionsDb.reviews\", {\"user_id\": \"hashed\"})" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "db.createCollection(\"actionsDb.bookmarks\")" | mongosh'
	docker exec -i $(PN)mongos1 bash -c 'echo "sh.shardCollection(\"actionsDb.bookmarks\", {\"user_id\": \"hashed\"})" | mongosh'



 
