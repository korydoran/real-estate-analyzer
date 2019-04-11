from bs4 import BeautifulSoup
import requests
import pandas as pd


## Required Headers must be passed to zillow so that it thinks we are a web browser

req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

### Make HTTP Request to Zillow

with requests.Session() as s:
    url = 'https://www.zillow.com/homes/Eugene-OR_rb/'
    r = s.get(url, headers=req_headers)

### Parse the HTML results
soup = BeautifulSoup(r.content, 'lxml')
#next_button = soup.find_all("a", class_ = 'on')
#print(next_button)
#resultpagesol = soup.find("ol", {"class": 'zsg-pagination'})
#links = soup.find_all("li", {"class": 'zsg-pagination'})
#print(links)


#for li in links:
 #   print (li.a.get('href'))
#urlsuffixes = resultpagesa.find("href")
#print(urlsuffixes)

#resultcountdiv = soup.find("div", {"class": 'search-title-container zsg-content-item'})
#print (resultcountdiv.contents)

#resultcountdiv = soup.find("div", {"id":'map-result-count-message'})
#print (resultcountdiv)

#print(soup.h1)
#print(h2s)


### Use Beautiful Soup to finnd all of the spans in a class that holds all the prices
pricespans = soup.find_all('span', {'class': 'zsg-photo-card-price'})
#print(pricespans)

### Extract out the text (price data) from those spans
prices = [span.get_text() for span in pricespans]
#print (prices)

### Find all of the spans in a class that holds all the house info
infospans = soup.find_all('span', {'class': 'zsg-photo-card-info'})

### Extract out the text (house info) from those spans
infos = [span.get_text() for span in infospans]
#print (infos)


### Find all of the spans in a class that holds all the address info
addressspans = soup.find_all('span', {'itemprop': 'address'})
addresses = [span.get_text() for span in addressspans]

### zip all of the extractred data together into a list
data = [list(a) for a in zip(prices,infos,addresses)]
#print (data)

### Convert zipped list to Pandas DataFrame for ease of use
df = pd.DataFrame(data)
#print (df)

#df.to_csv('eugene_02282019_01.csv', index=False)




#print (price)

### repeat above for pages 2-20 of zillow results . Zillow will only return 20 results per page.
### Sort of a janky way of constructing the urls starting with page 20 counting down to page 2

###Need to improve - Maybe start with page 2 and make the except return something and have that something that is returned break the loop
ii = 20
while ii > 1:
    ### create a string for the page number, add a '_p/' to the end so it matches the end of a zillow url
    i = str(ii)
    urlsuffix = i + '_p/'
    #url2 = url + urlsuffix

    try:
        with requests.Session() as s:
            ### dynamically generate url
            url = 'https://www.zillow.com/homes/Eugene-OR_rb/' + urlsuffix
            r = s.get(url, headers=req_headers)

        ### use beautiful soup to parse page
        soup = BeautifulSoup(r.content, 'lxml')

        ###find all of the spans with price data
        pricespans = soup.find_all('span', {'class': 'zsg-photo-card-price'})
        #print(pricespans)
        ### extract  price data from span
        prices = [span.get_text() for span in pricespans]
        #print (prices)

        ###find all of the spans with house data
        infospans = soup.find_all('span', {'class': 'zsg-photo-card-info'})
        ### extract  house data from span
        infos = [span.get_text() for span in infospans]
        #print (infos)

        ###find all of the spans with address data
        addressspans = soup.find_all('span', {'itemprop': 'address'})

        ### extract  address data from span
        addresses = [span.get_text() for span in addressspans]

        ###zip it up into a list
        data = [list(a) for a in zip(prices,infos,addresses)]
        #print (data)

        ##convert to pandas dataframe
        dfnew = pd.DataFrame(data)
        ##append to existing df on each iteration
        df = df.append(dfnew, ignore_index = True)
    except:
        pass
    ##try and except covers for case where there are not 20 pages of results

    ### iterator
    ii = ii - 1
#print (df)


#############################  THE DATA HATH BEEN SCRAPED ##########################################

### geocode address data from our collection of data from zillow
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")

###CREATE SOME EMPTY LISTS

latlongslist = []
lats = []
longs = []

#### go through every address in our address columnn in the data frame geocode it into lat and long, store the lats and longs in the lists established above
for e in df[2]:
    ## Need a try/except tp protect against bad address data or just general geocode failures
    try:
        location = geolocator.geocode(e)
        lats.append(location.latitude)
        longs.append(location.longitude)
    ### just for the lat and long if that property did ont geocode so we can preserve the row integrity when we append this n to our existing dataframe
    except:
         lats.append(0)
         longs.append(0)

#latlongs = [list(a) for a in (zip (lats,longs))]
#print (latlongs)

##add lats and longs to our df
df['lats'] =  lats
df['longs'] = longs

##export to csv
df.to_csv('eugene_02282019_all.csv', index=False)



