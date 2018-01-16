from django.shortcuts import render
from search.models import history
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from search.models import userhint
from django.shortcuts import redirect

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

def search_process(request) :
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
    result = [{'img' : imglist[i], 'name' : namelist[i], 'price' : pricelist[i], 'shop' : shoplist[i], 'link' : linklist[i]} for i in range(len(goods))]
    return render(request, 'search_result.html', {'result' : result, 'keyword' : keyword})

def check_login(request) :
    if request.method == 'POST' :
        id = request.POST['id']
        password = request.POST['password']

        try :
            user = User.objects.get(username=id)
            if user.check_password(password) :
                request.session['login_id'] = id
                return render(request, 'index.html', {'login_id' : id})
            else :
                status = 'Password가 틀렸습니다.'
                return render(request, 'index.html', {'status' : status})
        except User.DoesNotExist :
            status = '존재하지 않는 ID입니다.'
            return render(request, 'index.html', {'status' : status})

def registration_process(request) :
    if request.method == 'POST':
        id = request.POST["id"]
        try:
            User.objects.get(username=id)
            status = "이미 존재하는 아이디입니다"
            return render(request, 'index.html', {"status": status})
        except User.DoesNotExist:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            password = request.POST["confirm_password"]
            email = request.POST['email']
            hint = request.POST['hint']
            id = request.POST['id']
            new_user = User.objects.create_user(
                username=id, email = email, password= password,
                first_name=first_name, last_name=last_name
            )
            new_user.save()
            uh = userhint.objects.create(user_id=User.objects.get(username=id), user_hint=hint)
            uh.save()
            request.session['login_id'] = id
            print(new_user)
            print(userhint)
            return render(request, 'index.html', {"login_id": id})

def registration(request) :
    return render(request, 'registration.html')