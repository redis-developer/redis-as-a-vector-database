import redis


r = redis.Redis()

isPosted = bool(r.get("isQOTDPosted"))

print(isPosted)
r.set("isQOTDPosted", "False")
print(isPosted)