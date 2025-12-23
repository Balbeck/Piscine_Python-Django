from path import Path as path

def testPathPy():
    try:
        dir_path = path.mkdir("pathTest")
        path.touch(dir_path + "/test.txt")
        file = path(dir_path + "/test.txt")
        file.write_text('Toto From 42')
        print(file.read_text())
    
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    testPathPy()
