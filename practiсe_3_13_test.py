from practiсe_3_13 import *

drone_controller = DroneController()

# takeoff = Takeoff(drone_controller)
# move_forward = MoveForward(drone_controller, 100)
# takeoff.execute()
# move_forward.execute()

# commands = [
#     Takeoff(drone_controller),
#     MoveForward(drone_controller, 100),
#     MoveForward(drone_controller, -100)
# ]
#
# strategy = ReconMissionStrategy()
# strategy.execute(commands)

context = DroneContext()
context.set_strategy(ReconMissionStrategy())

context.add_command(Takeoff(drone_controller))
context.add_command(MoveForward(drone_controller, 100))
context.add_command(MoveForward(drone_controller, 20))

context.execute()

context.set_strategy(PatrolMissionStrategy(n_patrols=3))
for _ in range(4):
    context.add_command(MoveForward(drone_controller, 50))
    context.add_command(Turn(drone_controller, 90))

context.execute()




