import numpy as np
import matplotlib.pyplot as plt

class RainTyrePerformance:
    def __init__(self, config):
        self.compounds = config.get("compounds", [])
        self.track_wetness = config.get("track_wetness", 0.5)  # 0 (dry) to 1 (fully wet)
        self.race_distance = config.get("race_distance", 50)  # laps
        self.base_temperature = config.get("base_temperature", 20)  # degrees Celsius
        self.load_per_lap = config.get("load_per_lap", 1500)  # Load in Newtons

    def simulate_compound(self, compound):
        grip = compound["base_grip"]
        wear_rate = compound["wear_rate"]
        water_displacement = compound["water_displacement"]

        remaining_grip = []
        temperatures = []
        performance = []

        current_grip = grip
        current_temp = self.base_temperature

        for lap in range(1, self.race_distance + 1):
            # Adjust grip based on wetness and water displacement
            wetness_factor = max(0, self.track_wetness - water_displacement)
            current_grip -= (wear_rate + wetness_factor * 0.1)
            current_grip = max(0, current_grip)

            # Adjust temperature
            temp_increase = self.load_per_lap * 0.0001
            current_temp += temp_increase - ((current_temp - self.base_temperature) * 0.05)  # cooling

            # Calculate performance
            lap_performance = current_grip * (1 - wetness_factor)

            # Append results
            remaining_grip.append(current_grip)
            temperatures.append(current_temp)
            performance.append(lap_performance)

        return {
            "remaining_grip": remaining_grip,
            "temperatures": temperatures,
            "performance": performance
        }

    def analyse_compounds(self):
        results = {}

        for compound in self.compounds:
            name = compound["name"]
            print(f"Simulating {name} rain tyre...")
            results[name] = self.simulate_compound(compound)

        return results

    def plot_results(self, results):
        laps = range(1, self.race_distance + 1)

        plt.figure(figsize=(14, 10))

        # Plot remaining grip
        plt.subplot(3, 1, 1)
        for compound, data in results.items():
            plt.plot(laps, data["remaining_grip"], label=f"{compound} Grip")
        plt.title("Rain Tyre Grip Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Grip Level")
        plt.legend()
        plt.grid(True)

        # Plot temperatures
        plt.subplot(3, 1, 2)
        for compound, data in results.items():
            plt.plot(laps, data["temperatures"], label=f"{compound} Temperature")
        plt.title("Rain Tyre Temperature Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Temperature (°C)")
        plt.legend()
        plt.grid(True)

        # Plot performance
        plt.subplot(3, 1, 3)
        for compound, data in results.items():
            plt.plot(laps, data["performance"], label=f"{compound} Performance")
        plt.title("Rain Tyre Performance Over Race Distance")
        plt.xlabel("Lap")
        plt.ylabel("Performance Metric")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    compounds = [
        {
            "name": "Intermediate",
            "base_grip": 0.8,
            "wear_rate": 0.01,
            "water_displacement": 0.6
        },
        {
            "name": "Full Wet",
            "base_grip": 1.0,
            "wear_rate": 0.015,
            "water_displacement": 0.8
        }
    ]

    config = {
        "compounds": compounds,
        "track_wetness": 0.7,
        "race_distance": 50,
        "base_temperature": 15,
        "load_per_lap": 1500
    }

    analysis = RainTyrePerformance(config)
    results = analysis.analyse_compounds()
    analysis.plot_results(results)