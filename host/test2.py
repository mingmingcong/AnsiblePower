import redis
REDIS_URI = 'redis://sys-redis.rzwxgy.0001.cnn1.cache.amazonaws.com.cn:3807/3'
ri = redis.Redis.from_url(REDIS_URI)
ri = redis.StrictRedis(host=REDIS_URI)
print ri.echo("dsdsds")
print ri.get("gn86azx2jornynxupuffwsapf9y82gfw")