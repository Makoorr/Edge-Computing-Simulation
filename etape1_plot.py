import matplotlib.pyplot as plt
from utils.simulator import Simulator

seed = 12345
mean = 20
standard_deviation = 5
simulator = Simulator(seed, mean, standard_deviation)

data_set = [simulator.calculate_next_value() for _ in range(100000)]

plt.figure(figsize=(12, 6))
plt.plot(data_set, color='blue', linewidth=0.5)
plt.title("Simulator Generated Values")
plt.xlabel("Iteration")
plt.ylabel("Value")
plt.show()
