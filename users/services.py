from .decorators import display_running_time
from .memcache_helpers import get_key, set_key, get_client


@display_running_time
def get_user_profile_from_cache(
    username, always_recalculate=False
):
    cache_key = username

    if not always_recalculate:
        if profile_data := get_key(cache_key):
            return profile_data
        else:
            return None
