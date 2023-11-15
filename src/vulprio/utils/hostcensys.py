"""Search hosts data set."""
from censys.search import CensysHosts

if __name__ == "__main__":
    h = CensysHosts()

    # Multiple pages of search results
    query = h.search(".go.id", per_page=100, pages=1)
    for page in query:
        for host in page:
            print(host.get("ip"))
