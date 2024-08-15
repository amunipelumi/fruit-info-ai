from fruit_info.settings import MRC as cache
from .agent import health_benefits
import time
import json


def cached_(func): 
    def wrapper(*args):
        # start_time = time.time()
        benefits = None
        fruit_n = args[0]
        data = cache.get(fruit_n)

        if data:
            try:
                benefits = json.loads(data)
                # print('from redis')
            except (ValueError, UnicodeDecodeError):
                 pass
        
        if not benefits:
            benefits = func(fruit_n)
            cache.set(fruit_n, json.dumps(benefits), 43200)
            # print('not from redis')

        context = {'fruit': fruit_n, 'benefits': benefits}
        # end_time = time.time()
        # print('\n', end_time - start_time, '\n')
        return context
    
    return wrapper


@cached_
def get_benefits(f_name):
    return health_benefits(f_name)
