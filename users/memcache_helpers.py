from pymemcache.client.base import Client
from pymemcache import serde


def get_client():
    return Client(("memcached", 11211), serde=serde.pickle_serde)


def set_key(key, value, expire=0):
    """
    expire - "optional int, number of seconds until the item is
              expired from the cache, or zero for no expiry (the default)."
    """
    try:
        client = get_client()
        return client.set(key, value, expire=expire)
    except Exception as e:
        print("Error in memcache set function:", e)


def get_key(key):
    try:
        client = get_client()
        return client.get(key)
    except Exception as e:
        print("Error in memcache get function:", e)
