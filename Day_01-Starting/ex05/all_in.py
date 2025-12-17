import sys

def formated_name(name: str) -> str:
    return name.title()

def get_all_in():
    states = {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    if len(sys.argv) != 2:
        return

    arg_list = [arg.strip() for arg in sys.argv[1].split(',')]
    # print(arg_list)

    capitals = {state: capital_cities[abbreviation] for state, abbreviation in states.items()}
    state_capitals = {capital_cities[abbr]: state for state, abbr in states.items()}
    # print(capitals)
    # print(state_capitals)

    for arg in arg_list:
        arg = formated_name(arg)
        if arg in capitals:
            print(f'{capitals[arg]} is the capital of {arg}')
        elif arg in state_capitals:
            print(f'{arg} is the capital of {state_capitals[arg]}')
        elif arg == '':
            continue
        else:
            print(f'{arg} is neither a capital city nor a state')

if __name__ == '__main__':
    get_all_in()
