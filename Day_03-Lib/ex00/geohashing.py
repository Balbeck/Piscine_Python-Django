import sys
import antigravity

def geohash():
    """
    Geohashing function that takes latitude, longitude, Dow Jones date, and Dow Jones value
    eg: python3 geohashing.py -12.42 42.17 01-01-2021 1850.42
    Ca ne sert a rien !!! 
    """
    if len(sys.argv) != 5:
        print("Usage: python3 geohashing.py <latitude> <longitude> <dow_jones_date> <dow_jones_value>")
        print('python3 geohashing.py -12.42 42.17 01-01-2021 1850.42')
        sys.exit(1)
    try:
        lat = float(sys.argv[1])
        lon = float(sys.argv[2])
        dowDate = sys.argv[3]
        dowValue = float(sys.argv[4])
        dow = f"{dowDate}-{dowValue}".encode('utf-8')

        # result = antigravity.geohash(lat, lon, dow)
        # print(result) --> antigravity.geohash() print d'elle meme le resultat 
        
        formatedDow = "2005-05-26-10458.68".encode('utf-8')
        antigravity.geohash(lat, lon, formatedDow)
    
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == "__main__":
    geohash()
 