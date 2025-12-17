def get_element_from_line(line: str):
    element = {}
    name, raw_datas = line.split('=')
    element['name'] = name.strip()
    # print (name.strip())
    datas = raw_datas.split(',')
    for data in datas:
        key, value = data.split(':')
        element[key.strip()] = value.strip()
    # print(element)
    return element

def get_formated_elements_from_file(filename) -> list:
    elements = {}

    with open(filename, 'r') as file:
        for line in file:
            if not line :
                continue
            # print(line)
            element = get_element_from_line(line.strip())
            elements[element['number']] = element
    
    # print (elements)
    return elements


def get_body_from_elements(elements: dict) -> str:
    ELEMENT_CARD = """
      <td style="border: 1px solid black; padding:10px">
        <h4 style="text-align: center">{name}</h4>
        <ul>
          <li>No {number}</li>
          <li>{small}</li>
          <li>{molar}</li>
        </ul>
      </td>
    """

    body = ""
    actual_position = 0

    for num, element in elements.items():
        if actual_position > int(element['position']) :
            body += "   </tr>\n     <tr>"
            actual_position = 0
        for _ in range(actual_position, int(element['position']) -1):
            body += "       <td></td>\n"
        actual_position = int(element['position'])
        body += ELEMENT_CARD.format(
            name = element['name'],
            number = num,
            small = element['small'],
            molar = element['molar'],
            # electron = element['electron']
        )

    return body


def create_index_html_file(elements):
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Periodic Table</title>
</head>
<body>
    <h1>Periodic Table</h1>
    <table style="border-collapse: collapse">
        <tr>
        {body}
        </tr>
    </table>
</body>
</html>
    """
    body = get_body_from_elements(elements)
    with open('index.html', 'w') as file:
        file.write(html.format(body=body))


def periodic_table():
    elements = get_formated_elements_from_file('periodic_table.txt')
    create_index_html_file(elements) 

if __name__ == '__main__':
    periodic_table()
