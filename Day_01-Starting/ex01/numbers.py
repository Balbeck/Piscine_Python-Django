def get_numbers_from_file():
    filename = 'numbers.txt'
    numbers = []

    with open(filename, 'r') as numbersFile:
        line = numbersFile.readline()

    numbers = line.split(',')

    for num in numbers:
        print(num)

if __name__ == '__main__':
    get_numbers_from_file()
