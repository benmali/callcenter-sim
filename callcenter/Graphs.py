import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Graphs:
    def __init__(self):
        pass

    @staticmethod
    def plot_agents_vs_abandon():
        """
        Plot a graph of number of agents vs churn
        @return:
        """
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.set_title('Agents vs Number of clients abandoning the service')
        ax.legend(loc='upper left')
        ax.set_ylabel('Number of clients')
        ax.set_xlabel('Number of Agents')

    @staticmethod
    def plot_agents_vs_avg_queue_length():
        pass

    @staticmethod
    def plot_agents_vs_avg_wait_time():
        pass

    @staticmethod
    def plot_arrival_histogram(arrival_histogram):
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.set_title('Hour of the day vs Number of clients arrivals')
        ax.set_ylabel('Number of clients')
        ax.set_xlabel('Hour of the day')
        ax.set_xticks(ticks=list(arrival_histogram.keys()))
        ax.set_yticks(ticks=np.arange(0, 600, 50))
        ax.hist(arrival_histogram)
        plt.bar(arrival_histogram.keys(), arrival_histogram.values())
        plt.show()