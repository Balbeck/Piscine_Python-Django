import sys

def capital_city():
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
    
    capitals = {state: capital_cities[abbreviation] for state, abbreviation in states.items()}
    # print (capitals)

    city = sys.argv[1]
    if (city not in capitals):
        return print("Unknown state")
    print(capitals[city])

if __name__ == '__main__':
    capital_city()
