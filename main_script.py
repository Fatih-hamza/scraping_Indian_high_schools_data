# bismillah
import pandas as pd 
# pandas is used to organize, manipulate and analyse data, we will use it to use its DataFrame Class to organize data in a tabular form and them saving it to en Excel sheet
from bs4 import BeautifulSoup 
# bs4 enables us to take the HTML file and retrive its data with the use of elements tags 
import requests 
# requests allows us to send HTTP requests and recieve them using python



print('begin')

# we want to retrieve data about indian schools from a website
def retrieve_data(my_url):
    url = my_url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'} 
    page = requests.get(url, headers=headers) 
    # request.get sends a get HTTP request to the specified url and retur the response
    # the headers parameter is optional, but it may solve some permission and access related problems
    # it simply gives additional info (metadata) about the request 
    # the page variable contains the response to our GET request (200 Ok, forbidden, ...)
    source = page.content 
    # source contains the content of the http response, in bytes format
    soup = BeautifulSoup(source, 'lxml') 
    # soup is an instance of bs4.BeautifulSoup. With the help of a parser (in this case I chose the lxml parser), I can take the parts of the HTML code I'm intersted in 
    schools_cards = soup.find_all('div', {"class":"col-12"}) 
    
    schools_names = []
    schools_locations = []
    schools_phones = []
    schools_fax = []
    schools_websites = []
    schools_detail1 = []
    schools_detail2 = []
    schools_detail3 = []
    schools_detail4 = []
    schools_detail5 = []
    
    for card in schools_cards: 
        if card.find("ul") is not None: 

            school_location_phone = card.find("p") 
            my_string = school_location_phone.get_text()
            my_string = my_string.split("phone")
            phone = my_string[-1].strip()
            link = card.find('a')
            url = link.get('href')
            page = requests.get(url, headers=headers) 
            source = page.content 
            soup = BeautifulSoup(source, 'lxml') 
            website = soup.find('a', {"class":"pmd-list-title h5"})
            fax = "None"
            location = my_string[0][13:]
            if "Fax" in phone:
                phone, fax = phone.split("Fax : ")[0].strip(), phone.split("Fax : ")[1].strip()

            schools_names.append(card.find("h4").text) 
            schools_phones.append(phone)
            schools_fax.append(fax)
            schools_locations.append(location)
            site = "None"
            if website != None:
                site = website.get('href')
            schools_details = ["None"]*5
            details = card.find("ul").find_all("li") 


            for i in range(len(details)):
                schools_details[i] = details[i].text

            schools_detail1.append(schools_details[0])
            schools_detail2.append(schools_details[1])
            schools_detail3.append(schools_details[2])
            schools_detail4.append(schools_details[3])
            schools_detail5.append(schools_details[4])
            schools_websites.append(site)

    return schools_names,schools_locations,schools_phones,schools_fax,schools_websites,schools_detail1,schools_detail2,schools_detail3,schools_detail4,schools_detail5

page1_url = "https://targetstudy.com/school/high-secondary-schools-in-manipur.html#:~:text=%20High%20Secondary%20Schools%20in%20Manipur%20%201,13%20Little%20Rose%20Higher%20Secondary%20School%20More%20" 
schools_names,schools_locations,schools_phones,schools_fax,schools_websites,schools_detail1,schools_detail2,schools_detail3,schools_detail4,schools_detail5 = retrieve_data(page1_url)

page2_url = "https://targetstudy.com/school/high-secondary-schools-in-manipur.html?recNo=25"
schools_names2,schools_locations2,schools_phones2,schools_fax2,schools_websites2,schools_detail12,schools_detail22,schools_detail32,schools_detail42,schools_detail52 = retrieve_data(page2_url)

data = {
    'name': schools_names+schools_names2,
    'location': schools_locations + schools_locations2,
    'phone': schools_phones + schools_phones2,
    'fax': schools_fax+schools_fax2,
    'website': schools_websites+schools_websites2,
    'detail 1': schools_detail1+schools_detail12,
    'detail 2': schools_detail2+schools_detail22,
    'detail 3': schools_detail3+schools_detail32,
    'detail 4': schools_detail4+schools_detail42,
    'detail 5': schools_detail5+schools_detail52
    }

# I added the data of the second page to the previous one
to_save = pd.DataFrame(data)
# I created a pandas dataframe upon this data

writer = pd.ExcelWriter('output.xlsx')
to_save.to_excel(writer, 'schools')
writer.save()
# I write the content of the dataframe into an Excel file
print('DATA is written successfully to the Excel Sheet')
