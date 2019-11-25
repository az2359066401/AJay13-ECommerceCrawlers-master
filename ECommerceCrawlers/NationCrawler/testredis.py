from redis import ConnectionPool, Redis
pool = ConnectionPool(host='s40', port=6379, db=0, decode_responses=True)
rdb = Redis(connection_pool=pool)

keys = rdb.keys()
print(keys)

# f = open("province.txt", "w",encoding='utf-8')
# for i in range(0,rdb.llen("province")):
# 	item = eval(rdb.lrange("province",i,i)[0])
# 	f.write('"'+item['name'] +'"'+ " "+   '"'+item['code']+ '"'+ " "+ '"'+str(item['type'])+'"' + " "+ '"'+item['parentCode']+'"\n')
# f.close()


# rdb.delete("province")
# rdb.lpush("province",str(["福建省" ,"350000000000" ,"1", "000000000000"]))


for i in range(0,rdb.llen("province")):
	# item = eval(rdb.lrange("province",i,i+1))
    # print(rdb.lrange("province",i,i+1))
    print(rdb.lrange("province",i,i))
for i in range(0, rdb.llen("city")):
#     # item = eval(rdb.lrange("city",i,i+1))
#     # print(rdb.lrange("city",i,i+1))
    print(rdb.lrange("city", i, i))
# for i in range(0, rdb.llen("county")):
#     # item = eval(rdb.lrange("county",i,i+1))
#     # print(rdb.lrange("county",i,i+1))
#     print(rdb.lrange("county", i, i))
#
# for i in range(0, rdb.llen("town")):
#     # item = eval(rdb.lrange("town",i,i+1))
#     # print(rdb.lrange("town",i,i+1))
#     print(rdb.lrange("town", i, i))
#
# for i in range(0, rdb.llen("village")):
#     # item = eval(rdb.lrange("village",i,i+1))
#     # print(rdb.lrange("village",i,i+1))
#     print(rdb.lrange("village", i, i))



#
# provinceList = rdb.lrange("province",0,-1)
# print(provinceList)
# for province in provinceList:
#     print(eval(province))
