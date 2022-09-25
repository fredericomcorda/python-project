import time

def Timerfuntion(Timer,start_time=time.time()):
    """Starting a timer"""
    if Timer ==  "start game":
        return time.time()
    elif Timer == "end game":
        #Total = time.time() - start_time
        return int(time.time() - start_time)
        #return f"Congratulations you finnished in {int(Total)} seconds"

