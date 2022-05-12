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
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hour of the day vs Number of clients arrivals')
        ax.set_ylabel('Number of clients')
        ax.set_xlabel('Hour of the day')
        ax.set_xticks(ticks=list(arrival_histogram.keys()))
        ax.set_yticks(ticks=np.arange(0, 600, 50))
        ax.hist(arrival_histogram)
        plt.bar(arrival_histogram.keys(), arrival_histogram.values())
        plt.savefig('../flask/static/images/arrivals.png')
        plt.show()

    @staticmethod
    def plot_rest_wait_histogram(wait_histogram):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Number of rest vs Wait time (minutes)')
        ax.set_xlabel('Wait time [Minutes]')
        ax.set_ylabel('Number of rests')
        ax.set_yticks(ticks=np.arange(0, 50, 5))
        ax.hist(wait_histogram, bins=10)
        plt.bar(wait_histogram.keys(), wait_histogram.values(),  width=0.1)
        plt.savefig('../flask/static/images/rest_wait.png')
        plt.show()

    @staticmethod
    def plot_client_wait_histogram(wait_histogram):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Wait time (minutes) vs Number of clients')
        ax.set_xlabel('Wait time [Minutes]')
        ax.set_ylabel('Number of clients')
        ax.set_yticks(ticks=np.arange(0, 1000, 50))
        ax.hist(wait_histogram, bins=10)
        plt.bar(wait_histogram.keys(), wait_histogram.values(),  width=0.1)
        plt.savefig('../flask/static/images/client_wait.png')
        plt.show()

    @staticmethod
    def plot_system_hist_calls(clients, hours):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hours of the day vs Clients in the system')
        ax.set_xlabel('Hours of the day')
        ax.set_ylabel('Number of people in the system')
        ax.set_yticks(ticks=np.arange(0, 100, 2))
        plt.stairs(clients, hours)
        plt.savefig('../flask/static/images/calls.png')
        plt.show()


    @staticmethod
    def plot_system_hist_chats(clients, hours):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hours of the day vs Chats in the system')
        ax.set_xlabel('Hours of the day')
        ax.set_ylabel('Number of chats in the system')
        ax.set_yticks(ticks=np.arange(0, 30, 5))
        plt.stairs(clients, hours)
        plt.show()