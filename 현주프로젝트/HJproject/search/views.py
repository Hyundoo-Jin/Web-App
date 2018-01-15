from django.shortcuts import render
from search.models import history
import requests
from bs4 import BeautifulSoup
# Create your views here.
def index(request) :
    return render(request, 'index.html')

def take_history(request) :
    try :
        user = request.session['user']
    except KeyError :
        user = 'Unknown'
    histories = history.objects.filter(search_user=user)
    return render(request, 'history.html', {'user' : user, 'histories' : histories})

def search(request) :
    keyword = request.POST['keyword']
    url = 'https://search.shopping.naver.com/search/all.nhn?origQuery=' + keyword + '&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query=' + keyword
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    goods_area = soup.find('ul', {'class': 'goods_list'})
    goods_list = goods_area.find_all('li', {'class': '_itemSection'})
    goods = goods_list[0:5]
    imglist = []
    namelist = []
    pricelist = []
    shoplist = []
    linklist = []
    for good in goods:
        imglist.append(good.find('img').attrs['data-original'])
        namelist.append(good.find('a', {'class': 'tit'}).text.strip())
        pricelist.append(good.find('span', {'class': 'num _price_reload'}).text)
        if good.find('a', {'class': 'mall_img'}).text:
            shoplist.append(good.find('a', {'class': 'mall_img'}).text)
        else:
            shoplist.append(good.find('a', {'class': 'mall_img'}).find('img').attrs['alt'])
        linklist.append(good.find('div', {'class': 'info'}).find('a').attrs['href'])
    result = [good for good in zip(*[imglist, namelist, pricelist, shoplist, linklist])]
    print(result)
    return render(request, 'index.html')