from bs4 import BeautifulSoup
from fastapi import FastAPI
from requests import get

class News:
    def __init__(self):
        #Define a timeout variable to prevent slow api response
       self.t = 5

    #These functions include distinct fetching methods for each website.
    #------------------------
    def haberturk(self):
        l = []
        url = "https://www.haberturk.com/"
        try:
            r = get(url, timeout=self.t)
            soup = BeautifulSoup(r.text, "html.parser")
            for i in range(4):
                l.append(
                    url[:-1] + soup.find("div", attrs={"id": f"topHeadlinesOfDay{i}"}).find("a")["href"])
        except:
            pass
        temp = []
        if l:
            for j,i in enumerate(l):
                try:
                    r = get(i, timeout=self.t)
                    soup = BeautifulSoup(r.text, "html.parser").find("div", attrs={"class": "featured"})
                    title = soup.find("h1").text
                    summary = soup.find("h2").text
                    temp.append({"id": f"new{j+1}", "title": title, "summary": summary})
                except:
                    pass
        return {"source": "haberturk.com", "data": temp}



    def milliyet(self):
        l = []
        url = "https://www.milliyet.com.tr/"
        try:
            r = get(url, timeout=self.t)
            soup = BeautifulSoup(r.text, "html.parser")
            divs = soup.find_all("div", attrs={"class": "col-lg-3 col-md-6 col-sm-12 col-xs-12"})[:4]
            for i in divs:
                l.append(url+i.find("a")["href"][1:])
        except:
            pass
        temp = []
        if l:
            for j,i in enumerate(l):
                try:
                    r = get(i, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.t)
                    soup = BeautifulSoup(r.content, "html.parser")
                    title = soup.find("h1", attrs={"class":"news-detail-title"}).text
                    summary = soup.find("div", attrs={"class": "news-media"}).find("h2").text
                    temp.append({"id": f"new{j+1}", "title": title, "summary": summary})
                except:
                    pass
        return {"source": "milliyet.com", "data": temp}


    def sozcu(self):
        l = []
        url = "https://www.sozcu.com.tr/"
        try:
            r = get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=self.t)
            soup = BeautifulSoup(r.content, "html.parser")
            div = soup.find_all("div", attrs={"class": "row"})[1]
            divs = div.find_all("div")
            for i in range(1,8,2):
                l.append(url[:-1]+divs[i].find("a")["href"])
        except:
            pass
        temp = []
        if l:
            for j,i in enumerate(l):
                try:
                    r = get(i, headers={"user-agent": "Mozilla/5.0"}, timeout=self.t)
                    soup = BeautifulSoup(r.content, "html.parser")
                    title = soup.find("h1").text
                    summary = soup.find("h2").text
                    temp.append({"id": f"new{j+1}", "title": title, "summary": summary})
                except:
                    pass

        return {"source": "sozcu.com.tr", "data": temp}

    def birgun(self):
        l = []
        url = "https://www.birgun.net/"
        try:
            r = get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=self.t)
            soup = BeautifulSoup(r.content, "html.parser")
            divs = soup.find_all("div", attrs={"class": "swiper-slide"})[:4]
            for i in divs:
                l.append(url[:-1]+i.find("a")["href"])
        except:
            pass
        temp = []
        if l:
            for j,i in enumerate(l):
                try:
                    r = get(i, headers={"user-agent": "Mozilla/5.0"}, timeout=self.t)
                    soup = BeautifulSoup(r.content, "html.parser")
                    title = soup.find("h1").text
                    summary = soup.find("h2").text
                    temp.append({"id": f"new{j+1}", "title": title, "summary": summary})
                except:
                    pass
        return {"source": "birgun.net", "data": temp}

    def ntv(self):
        l = []
        url = "https://www.ntv.com.tr/"
        try:
            r = get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=self.t)
            soup = BeautifulSoup(r.content, "html.parser")
            divs = soup.find_all("div", attrs={"class": "col-span-1"})
            for i in divs:
                l.append(url[:-1]+i.find("a")["href"])
        except:
            pass
        l = l[:4]
        temp = []
        if l:
            for j,i in enumerate(l):
                try:
                    r = get(i, headers={"user-agent": "Mozilla/5.0"}, timeout=self.t)
                    soup = BeautifulSoup(r.content, "html.parser")
                    title = soup.find("h1").text
                    summary = soup.find("h2").text
                    temp.append({"id": f"new{j+1}", "title": title, "summary": summary})
                except:
                    pass
        return {"source": "ntv.com.tr", "data": temp}
    #------------------------

    #This function collects data from all the special functions
    def get_news(self):
        #This mechanism simplifies adding new data into api response
        #For example, when a new function is added, it automatically adds the function response.
        methods = [
            getattr(self, name)
            for name in dir(self)
            if callable(getattr(self, name))
               and not name.startswith("_")
               and name not in ("get_news",)
        ]
        return {
            "success": True,
            "data": [method() for method in methods]
        }

app = FastAPI(title="Haber API")

#Create an instance
news = News()

#Create the /news endpoint
@app.get("/news")
def get_news():
    #Return api response
    return news.get_news()

