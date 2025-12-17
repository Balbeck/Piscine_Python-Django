import sys

def get_state():
    states = {
        "Oregon" : "OR",
        "Alabama" : "AL",
        "New Jersey": "NJ",
        "Colorado" : "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    if len(sys.argv) != 2:
        return 
    
    city = sys.argv[1]
    # capitals = {state: capital_cities[abbreviation] for state, abbreviation in states.items()}
    state_capitals = {capital_cities[abbr]: state for state, abbr in states.items()}


    if (city not in state_capitals):
        return print("Unknown capital city")
    print(state_capitals[city])

if __name__ == '__main__':
    get_state()
