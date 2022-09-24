def Timerfuntion(Timer,start_time):
    import time
    """Starting a timer"""

    if Timer ==  "start game":
        start = time.time()
        return start
    elif Timer == "end game":
        Total = time.time() - start_time
        return f"Congratulations you finnished in {int(Total)} seconds"

# import pandas as pd
# import os
# path = os.path.dirname(__file__)
# df = pd.read_csv(f'{path}/highscores.csv')
# print(df)
# df.loc[len(df.index)] = ["João", 2000]
# print(df)
# print(df.sort_values(by=["Score"], ascending=False))
 
# start_time = Timerfuntion("start game")
# print(start_time)
# time.sleep(5)

# print(Timerfuntion("end game"))
# print(time.time())
