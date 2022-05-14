import json


def read_user_parameters():
    """
    Read use chosen parameters
    @return:
    """
    try:
        with open("../helpers/probability_parameters.json") as file:
            probabilities = json.load(file)
        return probabilities
    except FileNotFoundError:
        print("Could not find probability_parameters.json")
    except Exception as e:
        print(e)
