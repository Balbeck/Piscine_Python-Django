import os
import sys
import re
import settings

def render():
    regexFileExtension = re.compile(r".+\.template$")

    if (len(sys.argv)) != 2:
        print("Usage: python3 render.py 'file.template'")
        sys.exit(1)

    if not regexFileExtension.match(sys.argv[1]):
        print("Error: File must have a '.template' extension.")
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f"Error: File '{sys.argv[1]}' not found.")
        sys.exit(1)

    try:
        settingsVars = vars(settings)  # import des vars de settings.py dans un dict
        # print(settingsVars)
        
        with open(sys.argv[1], 'r') as f:
            templateContent = f.read()
            # print(templateContent)
            renderedContent = templateContent.format(**settingsVars)
            # print(renderedContent)
            f.close()

        with open("result.html", 'w') as f:
            f.write(renderedContent)
            f.close()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    render()
