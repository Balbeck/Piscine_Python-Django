import sys, requests
from bs4 import BeautifulSoup, NavigableString
import urllib3

# doit etre dans <div id= "mw-content-text"
# il faut que commence par <a href=wiki/ 



def fetch_wiki_and_get_first_link(article_title):
    try:
        article_title = article_title.strip().replace(' ', '_')
        # print(f"Fetching article: {article_title}")

        if not article_title.startswith('/wiki/'):
            article_title = "/wiki/" + article_title

        wiki_base_url = "https://en.wikipedia.org"
        headers = {
            "User-Agent": "MyWikipediaBot/1.0 (Educational project; toto@42.com)"
        }
        url = wiki_base_url + article_title.replace(' ', '_')
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # doit etre dans <div id= "mw-content-text" 
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            print("No content found.")
            return None

        content_div = content_div.find('div', {'class': 'mw-parser-output'})
    
        # [ Debug ]
        # article_title = article_title.removeprefix('/wiki/')
        # with open(f"{article_title}.html", "w", encoding='utf-8') as f:
        #     f.write(content_div.prettify())    
        # print(soup.prettify())
        # print(soup)




        # Parcour les <p> pour trouver first valid link
        for paragraph in content_div.find_all('p', recursive=False):
            parenthesis_count = 0
            
            for element in paragraph.descendants:
                # Compte pour eliminer liens dans parentheses
                if isinstance(element, NavigableString):
                    text = str(element)
                    parenthesis_count += text.count('(')
                    parenthesis_count -= text.count(')')
                
                if element.name == 'a':
                    href = element.get('href', '')
                    
                    if (href
                        and href.startswith('/wiki/') 
                        and not href.startswith("/wiki/Help:")
                        and ':' not in href 
                        and parenthesis_count == 0 
                        and not element.find_parent(['i', 'em'])):

                        name = href.removeprefix('/wiki/')
                        # print(f"First valid link found: {name}")
                        print(name)
                        return href
        return None
    
    except Exception as e:
        print(f"Error: {e}")
        exit(1)





def road_to_philo():
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 roads_to_philosophy.py <starting_article>")
            sys.exit(1)

        # Desactiver les avertissements SSL
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        start_article = sys.argv[1]
        visited = []
        current_article = start_article
        print(start_article)

        while True:
            if current_article in visited:
                print("It leads to an infinite loop !")
                break
            visited.append(current_article)

            first_link = fetch_wiki_and_get_first_link(current_article)

            if not first_link:
                print("It leads to a dead end !.")
                break

            first_link = first_link.replace('/wiki/', '')
            current_article = first_link
            if current_article == "Philosophy":
                print(f"{len(visited)} roads from {visited[0]} to Philosophy")
                break
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    road_to_philo()
