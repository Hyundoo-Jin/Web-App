from django.shortcuts import render
from search.models import history
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from search.models import userhint
from django.shortcuts import redirect

# Create your views here.
def index(request) :
    try :
        login_id = request.session['login_id']
    except :
        login_id = 'Anonymous'
    return render(request, 'index.html', {'login_id': login_id})

def take_history(request) :
    try:
        login_id = request.session['login_id']
    except:
        login_id = 'Anonymous'
    histories = history.objects.filter(search_user=login_id)
    result = [{'keyword' : item.search_keyword,
               'user' : item.search_user,
               'time' : item.search_time,
               'list' : zip([link for link in item.search_linklist.split(', ')],
                            [name for name in item.search_namelist.split(', ')])}
              for item in histories]
    return render(request, 'history.html', {'login_id' : login_id, 'result' : result})

def search_process(request) :
    keyword = request.POST['keyword']
    if keyword == '사랑해요 팀랩' :
        return redirect('/admin')
    return redirect('/result/'+keyword)

def search_result(request, keyword) :
    try :
        login_id = request.session['login_id']
    except :
        login_id = 'Anonymous'
    url = 'https://search.shopping.naver.com/search/all.nhn?origQuery=' + keyword + '&pagingIndex=1&pagingSize=40&viewType=list&sort=price_asc&frm=NVSHATC&query=' + keyword
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    try:
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
        result = [{'img' : imglist[i], 'name' : namelist[i], 'price' : pricelist[i], 'shop' : shoplist[i], 'link' : linklist[i]} for i in range(5)]
        if request.session['login_id'] :
            searchlog = history.objects.create(search_keyword=keyword, search_user=login_id,
                                               search_imagelist=', '.join(imglist), search_namelist=', '.join(namelist),
                                               search_pricelist=', '.join(pricelist), search_shoplist=', '.join(shoplist),
                                               search_linklist=', '.join(linklist))
        else :
            searchlog = history.objects.create(search_keyword=keyword, search_user='Anonymous',
                                               search_imagelist=', '.join(imglist), search_namelist=', '.join(namelist),
                                               search_pricelist=', '.join(pricelist), search_shoplist=', '.join(shoplist),
                                               search_linklist=', '.join(linklist))
        searchlog.save()
    except:
        result = 'Error'
        searchlog = history.objects.create(search_keyword=keyword, search_user=login_id)
        searchlog.save()
    return render(request, 'search_result.html', {'result' : result, 'keyword' : keyword, 'login_id' : login_id})

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
                username = id, email = email, password = password,
                first_name = first_name, last_name = last_name
            )
            new_user.save()
            uh = userhint.objects.create(user_id=User.objects.get(username=id), user_hint=hint)
            uh.save()
            request.session['login_id'] = id
            return render(request, 'index.html', {"login_id": id})

def registration(request) :
        return render(request, 'registration.html', {'login_id': 'Anonymous'})

def account_info(request) :
    if request.session['login_id'] :
        login_id = request.session['login_id']
        account = User.objects.get(username=login_id)
        first_name = account.first_name
        last_name = account.last_name
        email = account.email
        user_hint = userhint.objects.get(user_id=User.objects.get(username=login_id)).user_hint
        return render(request, 'account_info.html', {'account' : account, 'login_id' : login_id,
                                                     'first_name' : first_name, 'last_name' : last_name,
                                                     'email' : email, 'user_hint' : user_hint})
    else :
        return render(request, 'index.html', {'login_id' : 'Anonymous'})

def logout(request) :
    request.session['login_id'] = 'Anonymous'
    return render(request, 'index.html', {'login_id' : 'Anonymous'})