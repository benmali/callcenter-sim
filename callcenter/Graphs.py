import matplotlib.pyplot as plt
import numpy as np

plt.rc('xtick', labelsize=6)    # fontsize of the tick labels

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
        ax.set_yticks(ticks=np.arange(0, 1000, 50))
        ax.hist(arrival_histogram)
        plt.bar(arrival_histogram.keys(), arrival_histogram.values())
        plt.savefig('../flask/static/images/arrivals.png')
        plt.show()

    @staticmethod
    def plot_rest_wait_histogram(wait_histogram):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Wait time (minutes) vs Number of Restaurants')
        ax.set_xlabel('Wait time [Minutes]')
        ax.set_ylabel('Number of Restaurants')
        ax.set_yticks(ticks=np.arange(0, 25, 2))
        plt.bar(wait_histogram.keys(), wait_histogram.values())
        plt.savefig('../flask/static/images/rest_wait.png')
        plt.show()

    @staticmethod
    def plot_call_wait_histogram(wait_histogram):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Wait time (minutes) vs Number of calls')
        ax.set_xlabel('Wait time [Minutes]')
        ax.set_ylabel('Number of calls')
        ax.set_yticks(ticks=np.arange(0, 1000, 50))
        plt.bar(wait_histogram.keys(), wait_histogram.values())
        plt.savefig('../flask/static/images/call_wait.png')
        plt.show()

    @staticmethod
    def plot_chat_wait_histogram(wait_histogram):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Wait time (minutes) vs Number of chats')
        ax.set_xlabel('Wait time [Minutes]')
        ax.set_ylabel('Number of chats')
        ax.set_yticks(ticks=np.arange(0, 1000, 50))
        plt.bar(wait_histogram.keys(), wait_histogram.values())
        plt.savefig('../flask/static/images/chat_wait.png')
        plt.show()

    @staticmethod
    def plot_system_hist_calls(clients, hours):
        # bins = np.linspace(8,23, 160)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hours of the day vs Calls in service')
        ax.set_xlabel('Hours of the day')
        ax.set_ylabel('Number of calls in service')
        ax.set_yticks(ticks=np.arange(0, 100, 2))
        plt.stairs(clients, hours)
        plt.savefig('../flask/static/images/calls.png')
        plt.show()


    @staticmethod
    def plot_system_hist_chats(clients, hours):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hours of the day vs Chats in service')
        ax.set_xlabel('Hours of the day')
        ax.set_ylabel('Number of chats in service')
        ax.set_yticks(ticks=np.arange(0, 100, 5))
        plt.stairs(clients, hours)
        plt.savefig('../flask/static/images/chats.png')
        plt.show()


    @staticmethod
    def plot_queue_chats(clients, hours):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hours of the day vs Chats in queue')
        ax.set_xlabel('Hours of the day')
        ax.set_ylabel('Number of Chats in the queue')
        ax.set_yticks(ticks=np.arange(0, 100, 5))
        plt.stairs(clients, hours)
        plt.savefig('../flask/static/images/chats_queue.png')
        plt.show()

    @staticmethod
    def plot_queue_calls(clients, hours):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hours of the day vs Calls in queue')
        ax.set_xlabel('Hours of the day')
        ax.set_ylabel('Number of Calls in the queue')
        ax.set_yticks(ticks=np.arange(0, 100, 5))
        plt.stairs(clients, hours)
        plt.savefig('../flask/static/images/calls_queue.png')
        plt.show()


    @staticmethod
    def plot_call_abandon_times(abandon_histogram):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hours of the day vs Calls abandoned')
        ax.set_xlabel('Hours of the day')
        ax.set_ylabel('Number of calls abandoned')
        ax.set_yticks(ticks=np.arange(0, 200, 10))
        # ax.hist(wait_histogram, bins=10)
        plt.bar(abandon_histogram.keys(), abandon_histogram.values())
        plt.savefig('../flask/static/images/call_abandon.png')

    @staticmethod
    def plot_chat_abandon_times(abandon_histogram):
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.set_title('Hours of the day vs Chats abandoned')
        ax.set_xlabel('Hours of the day')
        ax.set_ylabel('Number of chats abandoned')
        ax.set_yticks(ticks=np.arange(0, 200, 10))
        # ax.hist(wait_histogram, bins=10)
        plt.bar(abandon_histogram.keys(), abandon_histogram.values())
        plt.savefig('../flask/static/images/chat_abandon.png')