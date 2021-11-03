import os
import sys
from agent import agent
from utilities import read_turn_updates
from io import StringIO
from kaggle_environments import make

if __name__ == "__main__":
    env = make("lux_ai_2021", configuration={"seed": 562124210, "loglevel": 2, "annotations": True}, debug=True)
    steps = env.run(["agent.py", "agent.py"])
    html = env.render(mode="html")
    with open("out.html", "w") as out:
        out.write(html)


    # turn_updates = read_turn_updates()
    # initial_game_state = next(turn_updates)
    # agent = Agent(initial_game_state)
    # agent.take_turn()
    #
    # for update in turn_updates:
    #     agent.take_turn(turn_data=update)
