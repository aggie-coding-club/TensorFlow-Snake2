"""
test if speed lost from exception is worth it. it is.
"""

import time

def excepting():
    """2.1053500175476074 seconds"""
    for _ in range(10000000):
        try:
            raise Exception("lol")
        except:
            pass

def lining():
    """0.22040939331054688 seconds"""
    for _ in range(10000000):
        pass

start = time.time()

lining()

end = time.time()

print(end-start,"seconds")