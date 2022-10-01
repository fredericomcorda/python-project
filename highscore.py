import time
import pandas as pd


def Timerfuntion(Timer, start_time=time.time()):
    """Starting a timer"""
    if Timer == "start game":
        return time.time()
    elif Timer == "end game":
        #Total = time.time() - start_time
        return int(time.time() - start_time)
        # return f"Congratulations you finnished in {int(Total)} seconds"


def load_dataframe():
    score = pd.read_csv("Highscores.csv", delimiter=",")
    return score


def add_record(user, time):
    score = load_dataframe()
    score.loc[len(score.index)] = [user, time]
    score.sort_values(by=['points'], ascending=True, inplace=True)
    score.to_csv("Highscores.csv", index=False)
    print("\n\nless points the better")
    print(score)
