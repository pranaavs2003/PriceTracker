import pywintypes
from win10toast import ToastNotifier
import os
import datetime
from bs4 import BeautifulSoup
import requests
from matplotlib import pyplot as plt
import statistics
import smtplib


data=[]
URL_list=[]
toast = ToastNotifier()

#For modifying data
def makePrice(price):
    s1 = ''
    for i in price:
        if (i == ',' or i == '₹'):
            pass
        else:
            s1 = s1 + i
    return float(s1)
def makeTitle(title):
    l1 = title.split()
    s1 = ''
    for i in range(0, 3):
        s1 = s1 + ' ' + l1[i]
    return s1
def findPrice(s):
    flag=0
    p=''
    for i in s:
        if i=='>':
            flag=1
        elif i=='<':
            flag=0
        if flag==1 and i!='>' and i!='<':
            p+=i
    p=makePrice(p)
    return p

with open('data.txt','r+') as f:
    content = f.read()
    data = eval(content)
    # print(type(content))
with open('URL_list.txt', 'r+') as f:
    content = f.read()
    URL_list = eval(content)
    # print(content)


#Find Date
def findDate():
    d=datetime.datetime.now()
    day,month,year=d.day,d.month,d.year
    date=str(day)+'/'+str(month)+'/'+str(year)
    return date
#To add data to txt file
def addDatatofile(data):
    with open('data.txt','r+') as f:
        f.write(str(data))
def addProductData(data):
    for i in URL_list:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
        page = requests.get(i, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        date = findDate()
        if 'amazon' in i:
            title = soup.find(id='productTitle').text.strip()
            title = makeTitle(title)

            for j in range(len(data)):
                if data[j][0] == title:
                    indx = j
                    break

            try:
                try:
                    price = soup.find(id='priceblock_dealprice').text
                    price = makePrice(price)
                except:
                    price = soup.find(id='priceblock_ourprice').text
                    price = makePrice(price)

                data[indx][1][date] = makePrice(str(price))


            except:
                toast.show_toast("PriceTracker", title + " is Out of stock", duration=2,
                                 icon_path='icons/pricetracker_icon.ico')


        if 'flipkart' in i:
            title = soup.find(class_='B_NuCI').text
            title = makeTitle(title).strip()

            for j in range(len(data)):
                if data[j][0] == title:
                    indx = j
                    break

            try:
                try:
                    price = soup.find(class_='_30jeq3 _16Jk6d')
                    price = findPrice(str(price))
                    data[indx][1][date] = makePrice(str(price))

                except:
                    toast.show_toast("PriceTracker", title + " is Out of Stock", duration=2,
                                     icon_path='icons/pricetracker_icon.ico')
            except:
                toast.show_toast("PriceTracker", "Error (Code: 101) Price not Updated", duration=2,
                                 icon_path='icons/pricetracker_icon.ico')

    # print(data)
    toast.show_toast("PriceTracker", "Today's Price Updated", duration=2,
                     icon_path='icons/pricetracker_icon.ico')
def getPrice(price, dictionary):
    for i in dictionary:
        if i!='Out of Stock':
            price.append(i)
    return price

#For making plots
def makeArr1(mean, date):
    l1 = []
    for i in date:
        l1.append(mean)
    return l1
def plotAvg(y_list):
    sum, x_arr, y_arr = 0, [], [];
    for i in range(0, len(y_list)):
        sum += y_list[i]
    avg = sum / len(y_list)
    for i in range(0, len(y_list)):
        x_arr.append(i)
        y_arr.append(avg)
    plt.plot(x_arr, y_arr, label="Average Price", color='g', linestyle='dashed', linewidth=2)
def plotMaxMin(y_list):
    max0, min0, x_arr, y_arr_1, y_arr_2 = max(y_list), min(y_list), [], [], [];
    for i in range(0, len(y_list)):
        x_arr.append(i)
        y_arr_1.append(max0)
        y_arr_2.append(min0)
    plt.plot(x_arr, y_arr_1, label="Maximum", color='r', linestyle='dashed', linewidth=2)
    plt.plot(x_arr, y_arr_2, label="Minimum", color='y', linestyle='dashed', linewidth=2)
def makeDate1(date):
    date1 = []
    for i in date:
        s = ''
        k = 0
        count = 0
        for j in i:
            k += 1
            if j == '/':
                count += 1
            if count > 1:
                break
        s = i[0:k - 1]
        date1.append(s)
    return date1
#For making plot for a single product
def makePlotSingleProduct(data, product_name):
    date, price, avg = [], [], []
    indx = 0
    p1 = 0
    for i in range(len(data)):
        if data[i][0] == product_name:
            indx = i
            break

    dic = data[indx][1]
    #     print(dic)
    for i in dic:
        if dic[i] != 'Out of Stock':
            date.append(i)
            price.append(dic[i])
            p1 = dic[i]
        else:
            date.append(i)
            price.append(p1)

    title = product_name
    date = makeDate1(date)
    #     print(date)
    #     print('\n\n',price,'\n\n')

    mean = format(statistics.mean(price), '.2f')
    median = format(statistics.median(price), '.2f')
    sd = format(statistics.stdev(price), '.2f')

    print('Mean :               ', mean)
    print('Median :             ', median)
    print('Standard Deviation : ', sd)

    x_values = date
    y_values = price
    plt.figure(figsize=(12, 8))
    plt.plot(x_values, y_values, marker='o', label=title, ms=15, linewidth=3)

    plotAvg(y_values)
    plotMaxMin(y_values)

    plt.title("Price Tracker", size=25)
    plt.xlabel("Date", size=15)
    plt.ylabel("Price", size=15)
    plt.legend()
    plt.tight_layout()
    plt.style.use('fivethirtyeight')
    plt.show()
#For comparing the prices of two products
def comparePrices(product_name_1, product_name_2):
    date, price1, price2 = [], [], []
    indx1, indx2 = 0, 0
    p1, p2 = 0, 0
    for i in range(len(data)):
        if data[i][0] == product_name_1:
            indx1 = i
            break
    for i in range(len(data)):
        if data[i][0] == product_name_2:
            indx2 = i
            break

    dic1 = data[indx1][1]
    dic2 = data[indx2][1]
    #     print(dic)

    for i in dic1:
        if dic1[i] != 'Out of Stock':
            date.append(i)
            price1.append(dic1[i])
            p1 = dic1[i]
        else:
            date.append(i)
            price1.append(p1)
    for i in dic2:
        if dic2[i] != 'Out of Stock':
            price2.append(dic2[i])
            p2 = dic2[i]
        else:
            price2.append(p2)

    title1, title2 = product_name_1, product_name_2
    date = makeDate1(date)
    #     print(date)
    #     print('\n\n',price,'\n\n')

    mean1, mean2 = format(statistics.mean(price1), '.2f'), format(statistics.mean(price2), '.2f')
    median1, median2 = format(statistics.median(price1), '.2f'), format(statistics.median(price2), '.2f')
    sd1, sd2 = format(statistics.stdev(price1), '.2f'), format(statistics.stdev(price2), '.2f')

    print('Product-1')
    print('Mean :               ', mean1)
    print('Median :             ', median1)
    print('Standard Deviation : ', sd1)
    print('Product-2')
    print('Mean :               ', mean2)
    print('Median :             ', median2)
    print('Standard Deviation : ', sd2)

    x_values = date
    y_values_1 = price1
    y_values_2 = price2
    plt.figure(figsize=(12, 8))
    plt.plot(x_values, y_values_1, marker='o', label=title1, ms=10, linewidth=3)
    plt.plot(x_values, y_values_2, marker='o', label=title2, ms=10, linewidth=3)

    #     plotAvg(y_values)
    #     plotMaxMin(y_values)

    plt.title("Price Tracker", size=25)
    plt.xlabel("Date", size=15)
    plt.ylabel("Price", size=15)
    plt.legend()
    plt.tight_layout()
    plt.style.use('fivethirtyeight')
    plt.show()


#For sending daily report mail
def sendMail():
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("avj2512003@gmail.com","avj2501d")

    for i in range(len(data)):
        dictionary = list(data[i][1].values())
        lol = len(dictionary)
        server.sendmail("avj2512003@gmailcom","pricetracker1234@gmail.com","product name "+data[i][0]+" product price "+str(dictionary[lol-1]))
    server.quit()
    toast.show_toast("PriceTracker", "Daily Report Sent to Mail", duration=5, icon_path='icons/pricetracker_icon.ico')
#For sending remainder mail
def sendremainderMail():
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("avj2512003@gmail.com","avj2501d")
    s=""
    for i in range(len(data)):
        price =[]
        dictionary = list(data[i][1].values())
        # print(dictionary)
        price = getPrice(price,dictionary)
        print(price)
        # print(dictionary)
        lol = len(dictionary)
        previous_price=dictionary[lol-2]
        # print(previous_price)
        ########################################
        threshold_price = statistics.mean(price)
        ########################################
        # threshold_price = float(input("Enter the threshold_value for the item"+data[i][0]+": "))
        if(dictionary[lol-1]<threshold_price):
            s=s+"\n"+"PRODUCT NAME "+data[i][0]+" PRODUCT PRICE "+str(dictionary[lol-1])
        else:
            if((previous_price - ((10 * previous_price) / 100)) < dictionary[lol - 1] <= (previous_price - ((5 * previous_price) / 100))):
                s=s+"\n"+"The price of the product"+data[i][0]+"has been reduced by 5 percent"
                print("A mail has been sent to your mail id")
            if((previous_price - ((20 * previous_price) / 100)) < dictionary[lol - 1] <= (
                previous_price - ((10 * previous_price) / 100))):
                    s = s + "\n" + "The price of the product" + data[i][0] + " has been reduced by 10 percent"
                    print("A mail has been sent to your mail id")
            if(dictionary[lol - 1] <= (previous_price - ((20 * previous_price) / 100))):
                    s = s + "\n" + "The price of the product" + data[i][0] + " has been reduced by 20 percent"
                    print("A mail has been sent to your mail id")
    sub="YOUR DAILY REPORT"
    if(s!=""):
        server.sendmail("avj2512003@gmailcom","pricetracker1234@gmail.com",f'Subject:{sub}{s}')
        print("A mail has been sent to your mail id")
    server.quit()


#Calling all Functions
addProductData(data)
addDatatofile(data)

# makePlotSingleProduct(data,' Lenovo IdeaPad Slim')
# comparePrices(' Lenovo IdeaPad Slim',' Lenovo Legion Y540')

#To send mail
# sendMail()
sendremainderMail()

os.chdir("C:\\Users\LENOVO\PycharmProjects\Price_Tracker")
dt=str(datetime.datetime.now())

with open('textfile.txt','a') as f:
    f.write(dt)
    f.write('\n')

