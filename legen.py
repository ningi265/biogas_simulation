import simpy
import numpy as np
import matplotlib.pyplot as plt

class BiogasDigester:
    def __init__(self, initial_pH, retention_time):
        # Initialize the digester's state or parameters
        self.organic_acids = 0
        self.methane_production = 0.0
        self.pH = initial_pH
        self.retention_time = retention_time

# Constants and parameters
MAX_ORGANIC_ACIDS_PRODUCTION = 0.5
TEMPERATURE_OPTIMAL = 35.0
MAX_METHANE_PRODUCTION = 0.8
PH_OPTIMAL = 7.0

def calculate_organic_acids_production(organic_matter, temperature, pH):
    # Model for organic acids production during anaerobic digestion
    temperature_influence = np.exp(-(temperature - TEMPERATURE_OPTIMAL) ** 2 / (2 * 5.0 ** 2))
    pH_influence = np.exp(-(pH - PH_OPTIMAL) ** 2 / (2 * 1.0 ** 2))
    organic_acids_production = MAX_ORGANIC_ACIDS_PRODUCTION * temperature_influence * pH_influence * (organic_matter ** 0.5)
    return organic_acids_production

def calculate_methane_production(organic_matter, temperature, pH, retention_time):
    # Model for methane production during anaerobic digestion
    temperature_influence = np.exp(-(temperature - TEMPERATURE_OPTIMAL) ** 2 / (2 * 5.0 ** 2))
    pH_influence = np.exp(-(pH - PH_OPTIMAL) ** 2 / (2 * 1.0 ** 2))
    retention_time_factor = 1 / retention_time  # Adjust the factor based on your requirements
    methane_production = MAX_METHANE_PRODUCTION * temperature_influence * pH_influence * retention_time_factor * (organic_matter ** 0.7)
    return methane_production

def update_digester_state(digester, organic_matter, temperature):
    # Update digester state based on digestion process
    digester.organic_acids += calculate_organic_acids_production(organic_matter, temperature, digester.pH)
    digester.methane_production += calculate_methane_production(organic_matter, temperature, digester.pH, digester.retention_time)

def feedstock_process(env, digester, organic_acids_data, methane_data):
    while True:
        yield env.timeout(1)  # Simulate decomposition over time
        # Update digester state based on decomposition process
        # ...

        # Example usage
        initial_organic_matter = 100.0
        temperature = 35.0
        update_digester_state(digester, initial_organic_matter, temperature)

        # Record data for plotting
        organic_acids_data.append(digester.organic_acids)
        methane_data.append(digester.methane_production)

def reactor_process(env, digester):
    while True:
        yield env.timeout(digester.retention_time)  # Simulate digestion over time
        # Update digester state based on digestion process
        # ...

def gas_storage_process(env, digester):
    while True:
        yield env.timeout(1)  # Simulate gas storage over time
        # Update digester state based on gas storage process
        # ...

def plot_results(time, organic_acids_data, methane_data, pH_data):
    plt.figure(figsize=(10, 6))

    plt.subplot(3, 1, 1)
    plt.plot(time, organic_acids_data, label='Organic Acids')
    plt.xlabel('Time')
    plt.ylabel('Organic Acids Production')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(time, methane_data, label='Methane')
    plt.xlabel('Time')
    plt.ylabel('Methane Production')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(time, pH_data, label='pH')
    plt.xlabel('Time')
    plt.ylabel('pH')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Usage
initial_pH = 7.0
retention_time = 5  # Adjust retention time based on your units
env = simpy.Environment()
digester = BiogasDigester(initial_pH, retention_time)

# Data recording for plotting
time_points = []
organic_acids_data_points = []
methane_data_points = []
pH_data_points = []

# Add feedstock_process to the environment
env.process(feedstock_process(env, digester, organic_acids_data_points, methane_data_points))
env.process(reactor_process(env, digester))
env.process(gas_storage_process(env, digester))

# Record time points for plotting
endpoint = 100  # Set the endpoint for the simulation
for time_point in range(endpoint):
    time_points.append(time_point)
    env.run(until=time_point + 1)  # Run until the next time point
    pH_data_points.append(digester.pH)  # Record pH data

# Plot the results
plot_results()
