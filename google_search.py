from googlesearch import search

def search_google(query):
    try:
        search_results = search(query, num_results=1, lang='en')
        first_link = next(search_results)
        return first_link
    except StopIteration:
        return None


if __name__ == '__main__':
    s = "Baswood---https://baswood.webflow.io/"
    di = {}
    di[s.split("---")[0]] = s.split("---")[1]

    print(search_google("esusu image"))