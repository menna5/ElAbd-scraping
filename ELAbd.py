from bs4 import BeautifulSoup
import requests as re
import csv
from itertools import zip_longest

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

links = []
names = []
prices = []
descs = []
imgs = []

categories = []
url = 'https://elabdfoods.com/%D9%83%D8%AD%D9%83-%D9%88%D8%A8%D8%B3%D9%83%D9%88%D9%8A%D8%AA?pagenumber=1&orderby=5&price=7-1900'
page = re.get(url, headers=headers)
src = page.content
soup = BeautifulSoup(src, 'html.parser')
categories_data = soup.find('ul', {"class":"nav nav-list"})
categories_data = categories_data.find_all("a")
for category in categories_data:
    category = category.attrs["href"]
    categories.append(category)
print(f"Categories: {len(categories)}")

def main():
    for j in range(len(categories)):
        category = categories[j]
        url = f'https://elabdfoods.com{category}?pagenumber=1&orderby=5&price=7-1900'
        page = re.get(url, headers=headers)
        src = page.content
        soup = BeautifulSoup(src, 'html.parser')
        n = soup.find('div', {"class":"pager"}).ul
        if n is None:
            n = 1
        else:
            if n.text[-7].isdigit():
                n = int(n.text[-7])
            else:
                print(n.text)
                n = int(n.text[-14])
        print(f"No. page: {n}")
        
        for i in range(n):
            url = f'https://elabdfoods.com{category}?pagenumber={i}&orderby=5&price=29-465'
            page = re.get(url, headers=headers)
            src = page.content
            soup = BeautifulSoup(src, 'html.parser')
            data = soup.find_all('div', {"class":"thumbnail"})
            for datum in data:
                name = datum.find('h3', {"class":"product-title"}).text.strip()
                desc = datum.find('p', {"class":"description"}).text.strip()
                price_data = datum.find('div', {"class":"prices"}).text.strip().replace(',', '')[:-9]
                if price_data == '':
                    pass
                else:
                    price = int(price_data)
                img = datum.find('img', {"class":"lazyOwl"}).get('src')
                link = datum.find('h3', {"class":"product-title"}).a.attrs["href"]
            
                imgs.append(img)
                links.append(link)
                names.append(name)
                prices.append(price)
                descs.append(desc)
        print(f"Category: {j+1}")
            
    file_list = [names, descs, prices, imgs]
    exported = zip_longest(*file_list)
    with open(f"C:/Users/Menna/Desktop/ELAbd_finalall.csv", "w", newline='', encoding=('UTF-8-sig')) as file:
        wr = csv.writer(file)
        wr.writerow(["Title", "Description", "Price", "Image"])
        wr.writerows(exported)
    print("End Page")
        
    
main()






