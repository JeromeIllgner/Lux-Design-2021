from utils import turn_updates
from observation import Observation
from agent import agent


if __name__ == "__main__":
    observation = Observation()
    observation["step"] = 0
    step = observation["step"]

    for update in turn_updates():
        observation["updates"] = update

        if step == 0:
            observation.player = int(observation["updates"][0])

        actions = agent(observation, None)
        observation["updates"] = []
        step += 1
        observation["step"] = step
        print(",".join(actions))
        print("D_FINISH")

