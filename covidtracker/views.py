from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from matplotlib.style import context
import requests

from  bs4 import BeautifulSoup
import requests

# def covidnews():



#     return datadict
# import pandas as pd
# Create your views here.


URL = "https://api.covid19api.com/summary"
IndiaURL = "https://data.covid19india.org/state_district_wise.json"
# NewsURL="https://newsapi.org/v2/top-headlines?country=in&apiKey=cb0df83fd349468fa616de52f03a6cef&category=health"
NewsURL="https://newsapi.org/v2/top-headlines?country=in&apiKey=cb0df83fd349468fa616de52f03a6cef"
covidURL="https://timesofindia.indiatimes.com/coronavirus"


################################################################################


def index(request):
    labels = []
    labeldata = []
    response = requests.get(URL).json()
    news=requests.get(NewsURL).json()



    page = requests.get(covidURL).text
    doc = BeautifulSoup(page, "html.parser")
    datadict={}

    url2 = "https://www.indiatvnews.com/topic/coronavirus"
    page = requests.get(url2).text
    doc = BeautifulSoup(page, "html.parser")
    div=doc.find("ul",class_="newsListfull").find_all("li")
    
    for i in div:
        linksrc=(i.a.img.get("data-original"))
        title=(i.find("a").get("title"))
        link=(i.find("a").get("href"))
        datadict[title]={'href':link,'src':linksrc}

    # print(datadict,'--------------------------------------')
    print(response)
    summary = response["Global"]
    for i, j in summary.items():
        labels.append(i)
        labeldata.append(j)
    # print(labels, '*******************')
    header = response["Countries"][0]
    data = response["Countries"]
    # print(news,'---------------------------')
    return render(request, 'covidtracker/index.html', {'global': summary,'news':news,'datadict':datadict, 'header': header, 'rows': data, 'labels': labels, 'labeldata': labeldata})


###############################################################################
def country(request, country):
    labels = []
    labeldata = []

    response = requests.get(URL).json()
    countryresponse = requests.get(
        'https://api.covid19api.com/live/country/'+country+'/status/confirmed').json()
    summary = response["Global"]
    for i, j in summary.items():
        labels.append(i)
        labeldata.append(j)
    # print(labels, '*******************')
    data = countryresponse
    header1 = countryresponse[0]

    # print("44",data)
    newlist = []
    l = []
    for i in data:
        state = i.get("Province")
        if state not in l:
            l.append(state)
            newlist.append(i)
    country = country
    # print(country, '------------------------')
    return render(request, 'covidtracker/index.html', {'global': summary, 'header1': header1, 'country': country, 'rows': newlist, 'labels': labels, 'labeldata': labeldata})


###############################################################
def india(request):
    if request.method == "POST":
        indiadatadict = {}
        response = requests.get(URL).json()
        summary = response["Global"]
        indiadata = response["Countries"]
        indiadata = response["Countries"]
        Indiaresponse = requests.get(IndiaURL).json()
        for i in indiadata:
            if i['Country'] == "India":
                for key, value in i.items():
                    indiadatadict[key] = value
        print(indiadatadict, '************************************************')
        searchstate = request.POST.get('statename')
        dst_data = dict_sm = Indiaresponse[searchstate]["districtData"]
        return render(request, 'covidtracker/india.html', {'statelist': Indiaresponse, 'global': summary, 'indiadatadict': indiadatadict, 'indiadata': indiadata, 'searchstate': searchstate, "dst_data": dst_data})

    else:
        indiadatadict = {}
        response = requests.get(URL).json()
        summary = response["Global"]
        indiadata = response["Countries"]
        Indiaresponse = requests.get(IndiaURL).json()
        for i in indiadata:
            if i['Country'] == "India":
                for key, value in i.items():
                    indiadatadict[key] = value
        print(indiadatadict, '************************************************')
        return render(request, 'covidtracker/india.html', {'statelist': Indiaresponse, 'indiadatadict': indiadatadict, 'global': summary, })


###################################################################
def indian_state(request, state):
    indiadatadict = {}
    response = requests.get(URL).json()
    if request.method == "GET":
        indiadata = response["Countries"]
        Indiaresponse = requests.get(IndiaURL).json()
        for i in indiadata:
            if i['Country'] == "India":
                for key, value in i.items():
                    indiadatadict[key] = value
        response = requests.get(URL).json()
        summary = response["Global"]
        Indiaresponse = requests.get(IndiaURL).json()
        searchstate = state
        dst_data = dict_sm = Indiaresponse[searchstate]["districtData"]
        print(searchstate, '****************************')
        return render(request, 'covidtracker/india.html', {'statelist': Indiaresponse, 'indiadatadict': indiadatadict, 'global': summary, 'searchstate': searchstate, "dst_data": dst_data})

    else:
        indiadata = response["Countries"]
        Indiaresponse = requests.get(IndiaURL).json()
        for i in indiadata:
            if i['Country'] == "India":
                for key, value in i.items():
                    indiadatadict[key] = value
        response = requests.get(URL).json()
        summary = response["Global"]
        Indiaresponse = requests.get(IndiaURL).json()
        searchstate = request.POST.get('statename')
        dst_data = dict_sm = Indiaresponse[searchstate]["districtData"]
        print(searchstate, '****************************')
        news=requests.get(NewsURL).json()
        return render(request, 'covidtracker/india.html', {'news':news,'statelist': Indiaresponse, 'indiadatadict': indiadatadict, 'global': summary, 'searchstate': searchstate, "dst_data": dst_data})




def news(request):
    news=requests.get(NewsURL).json()
    return render(request, 'covidtracker/generalnews.html', {'news':news})


def covidnews(request):
    datadict={}

    url2 = "https://www.indiatvnews.com/topic/coronavirus"
    page = requests.get(url2).text
    doc = BeautifulSoup(page, "html.parser")
    div=doc.find("ul",class_="newsListfull").find_all("li")
  
    for i in div:
        linksrc=(i.a.img.get("data-original"))
        title=(i.find("a").get("title"))
        link=(i.find("a").get("href"))
        datadict[title]={'href':link,'src':linksrc}

    return render(request, 'covidtracker/covidnews.html', {'datadict':datadict})

def mynews(request):
   
    URL=request.GET.get('url')
    page = requests.get(URL).text
    doc = BeautifulSoup(page, "html.parser")
    heading = doc.find("h1",class_="arttitle").string
    lhs = doc.find("figure",class_="artbigimg row")
    image=lhs.find("img").get("data-original")
    data=doc.find_all("p")
    print(data)
    print(heading)
    print(image)
    datadict=[]
    for i in data[1]:
        newdata=i.text
        datadict.append(newdata)


    datadict1={}

    url2 = "https://www.indiatvnews.com/topic/coronavirus"
    page1 = requests.get(url2).text
    doc1 = BeautifulSoup(page1, "html.parser")
    div1=doc1.find("ul",class_="newsListfull").find_all("li")
  
    for i in div1:
        linksrc=(i.a.img.get("data-original"))
        title=(i.find("a").get("title"))
        link=(i.find("a").get("href"))
        datadict1[title]={'href':link,'src':linksrc}
    return render(request,'covidtracker/mynews.html',{'heading':heading,'image':image,'data':datadict,'datadict':datadict1})


def allnews(request):
    url=request.GET.get("url")
    page = requests.get(url).text
    data=BeautifulSoup(page,"html.parser")
    context_data={}

    if "https://timesofindia.indiatimes.com/" in url:   
        heading = data.find("h1",class_="sp-ttl").text
        articledata=data.find("div",class_="sp-cn ins_storybody")
        image=articledata.find("img").get("src")
        p=articledata.find_all("p")
        context_data['heading']=heading
        context_data['image']=image
        for i in p:
            print(i.text)
            
    if "https://indianexpress.com/" in url:
        paragraph=[]
        heading = data.find("h1",class_="native_story_title").text
        articledata=data.find("div",class_="full-details")
        image = articledata.find_all("img")
        image=image[4].get("src")
        context_data['heading']=heading
        context_data['image']=image
        pdata=articledata.find_all("p")
        print(image,heading,'******************************************')
        for i in pdata:
            print(i.text)
            paragraph.append(i.text)
        context_data['text']=paragraph
        print(context_data)

    elif "/timesofindia.indiatimes.com/" in URL:
        page = requests.get(url).text
        data=BeautifulSoup(page,"html.parser")
        head = data.find("div",class_="photostory_heading")
        heading=head.find("h1").text
        imagediv=data.find("div",class_="imagebox_bg")
        image=imagediv.find_all("img")
        image=image[2].get("data-src-new")
        context_data['heading']=heading
        context_data['image']=image
        readmore=data.find_all("span",class_="readmore_span")
        print(image,heading,'******************************************')
        for i in readmore:
            print(i.text)
        print(context_data)



    return render(request,"covidtracker/allnews.html",context_data)








def monkeypox(request):
    datadict={}
    url = "https://www.who.int/health-topics/monkeypox#tab=tab_1"
    page1 = requests.get(url).text
    doc1 = BeautifulSoup(page1, "html.parser")
    div=doc1.find_all("div",class_="arrowed-link")
    for i in div:
        title=i.string
        href=i.find("a").get("href")   
        datadict[title]=href 
        print(title)
        print('---------------------------')
    return render(request,'covidtracker/monkey.html',{"data":datadict})
  