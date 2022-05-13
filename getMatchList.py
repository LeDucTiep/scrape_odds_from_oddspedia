import requests
start_date = "2022-04-26"
end_date = "2022-04-26"
LINK_API=r"https://oddspedia.com/api/v1/getMatchList?excludeSpecialStatus=0&sortBy=default&perPageDefault=150&startDate="+start_date+r"T00%3A00%3A00Z&endDate="+end_date+r"T23%3A59%3A59Z&geoCode=VN&status=all&sport=&popularLeaguesOnly=1&page=1&perPage=150&language=en"

proxies = {}
response = requests.get(url=LINK_API, proxies=proxies)

print(response.content)