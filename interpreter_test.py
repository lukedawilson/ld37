from time import sleep
from robot import Robot
from robot_algorithm import RobotAlgorithm

input = """
if el
    rl
    if ef
        sh
    end
    fd
end
if er
    rr
    sh
end
if ef
    sh
end
fd
"""

robot = Robot()
algo = RobotAlgorithm(robot, input)

for _ in range(20):
    algo.run_next_command()
    sleep(0.3)
    