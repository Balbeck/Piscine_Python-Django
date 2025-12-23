# pour installer les dependances:
# python3 -m venv venv 
# source venv/bin/activate 
# pip install -r requirements.txt

import requests, json, dewiki, sys

#  -->  Désactiver les avertissements SSL
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def write_on_file(filename, content):
    filename = filename.replace(" ", "_") + ".wiki"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def get_wiki_response():

    if len(sys.argv) != 2:
        print("Usage: python3 request_wikipedia.py <search_term>")
        sys.exit(1)

    search_term = sys.argv[1]
    wiki_endpoint = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": search_term,
        "format": "json",
        "redirects": 1,
    }
    headers = {
        "User-Agent": "MyWikipediaBot/1.0 (Educational project; toto@42.com)"
    }

    try:
        response = requests.get(wiki_endpoint, params=params, headers=headers, verify=False)

        # Check le status de la request et raise Error si besoin
        response.raise_for_status()

        json_data = response.json()
        pages = json_data.get("query", {}).get("pages", {})
        # print(pages)

        if not pages:
            print(f"No page found for the term: {search_term}")
            return

        for page_id, page_data in pages.items():
            if page_id == "-1":
                print(f"No page found for the term: {search_term}")
                return
            title = page_data.get("title")
            extract = page_data.get("extract")
            if not title or not extract:
                print(f"No valid data found for the term: {search_term}")
                return
            # print(extract)

        # clean wikipedia layout
        extract = dewiki.from_string(extract)
        # print(extract)

        write_on_file(search_term, extract)
        

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__=="__main__":
    get_wiki_response()
