import requests
from bs4 import BeautifulSoup
import data_methods
from urllib.parse import quote
import time
import ast
from getpass import getpass

SERVICE = 'https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F'
LOGIN_URL = 'https://auth.berkeley.edu/cas/login'

def cas_login(username, password, service=SERVICE):
    parameters = {'service': service}
    login_url = LOGIN_URL

    session = requests.session()
    #TRY:
    session.get('https://calcentral.berkeley.edu/auth/cas')
    print(session.cookies.get_dict())


    # login = session.get(login_url, params=parameters)
    login = session.get('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F')

    login_html = data_methods.make_parser(login.text)
    hidden_elements = login_html.find_all('input', type='hidden')

    form = {}
    for x in hidden_elements:
        try:
            form[x['name']] = x['value']
        except KeyError as e:
            pass

    form['username'] = username
    form['password'] = password

    for key, value in form.items():
        print('key: ', key, 'value: ', value)

    #r = session.post(login_url, data=form, params=parameters)
    r = session.post('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F', data=form, allow_redirects=True)
    return r, session

def get_hidden(response):
    html = data_methods.make_parser(response.text)
    hidden = html.find_all('input', type='hidden')
    form = {}
    for x in hidden:
        try:
            form[x['name']] = x['value']
        except KeyError as e:
            pass
    return form

def test_login(username, password, phone_no = '2'):
    s = requests.session()
    r = []
    r.append(s.get('https://calcentral.berkeley.edu/'))
    r.append(s.get('https://calcentral.berkeley.edu/api/config'))
    r.append(s.get('https://calcentral.berkeley.edu/api/my/status'))
    r.append(s.get('https://calcentral.berkeley.edu/api/service_alerts'))
    r.append(s.get('https://calcentral.berkeley.edu/api/my/academics/status_and_holds'))
    r.append(s.get('https://calcentral.berkeley.edu/api/my/am_i_logged_in'))
    r.append(s.get('https://calcentral.berkeley.edu/auth/cas'))
    r.append(s.get('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F'))

    form = {}
    form['username'] = username
    form['password'] = password
    form.update(get_hidden(r[-1]))
    form['geolocation'] = ''

    r.append(s.post('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F', data=form))

    last = r[-1]
    parser = data_methods.make_parser(last.text)
    inputs = parser.find_all('input')
    execution = [x.attrs['value'] for x in inputs if 'name' in x.attrs and x.attrs['name'] == 'execution'][0]
    div = parser.find_all(id='duo_iframe')[0]
    tx, app = tuple(div.attrs['data-sig-request'].split(':'))
    api = 'https://' + div.attrs['data-host']
    url = api + '/frame/web/v1/auth?tx=' + tx + '&parent=https%3A%2F%2Fauth.berkeley.edu%2Fcas%2Flogin%3Fservice%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252Fauth%252Fcas%252Fcallback%253Furl%253Dhttps%25253A%25252F%25252Fcalcentral.berkeley.edu%25252F&v=2.6'

    r.append(s.get(url))

    form = {}
    form.update(get_hidden(r[-1]))
    form['referer'] = 'https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F'
    form['java_version'] = ''
    form['flash_version'] = '32.0.0.0'
    form['screen_resolution_width'] = '1920'
    form['screen_resolution_height'] = '1080'
    form['color_depth'] = '24'
    form['is_cef_browser'] = 'false'
    form['is_ipad_os'] = 'false'
    tx = form['tx']
    url = api + '/frame/web/v1/auth?tx=' + tx + '&parent=https%3A%2F%2Fauth.berkeley.edu%2Fcas%2Flogin%3Fservice%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252Fauth%252Fcas%252Fcallback%253Furl%253Dhttps%25253A%25252F%25252Fcalcentral.berkeley.edu%25252F&v=2.6'

    r.append(s.post(url, data=form))

    last = r[-1]
    parser = data_methods.make_parser(last.text)
    inputs = parser.find_all('input')
    sid = [x.attrs['value'] for x in inputs if 'name' in x.attrs and x.attrs['name'] == 'sid'][0]
    url = api + '/frame/prompt?sid=' + sid
    r.append(s.get(url))

    last = r[-1]
    parser = data_methods.make_parser(last.text)
    inputs = parser.find_all('input')
    sid = [x.attrs['value'] for x in inputs if 'name' in x.attrs and x.attrs['name'] == 'sid'][0]
    url = api + '/frame/prompt'
    form = {}
    form['sid'] = sid
    form['device'] = 'phone' + phone_no
    form['factor'] = 'Phone Call'
    form['out_of_date'] = ''
    form['days_out_of_date'] = ''
    form['days_to_block'] = 'None'

    r.append(s.post(url, data=form))

    txid = ast.literal_eval(r[-1].text)['response']['txid']
    url = api + '/frame/status'
    form['sid'] = sid
    form['txid'] = txid
    r.append(s.post(url, data=form))
    last = r[-1]
    while len(last.cookies) == 0:
        time.sleep(1)
        r.append(s.post(url, data=form))
        last = r[-1]

    r.append(s.post(url + '/' + txid, data={'sid': sid}))

    auth = ast.literal_eval(r[-1].text)['response']['cookie']
    duo_sign = auth + ':' + app

    executions = []
    for i in range(len(r)):
        resp = r[i]
        if 'execution' in resp.text:
            parser = data_methods.make_parser(resp.text)
            inputs = parser.find_all('input')
            execution = [x.attrs['value'] for x in inputs if 'name' in x.attrs and x.attrs['name'] == 'execution'][0]
            executions.append(execution)
            print(i)

    form = {}
    form['username'] = username
    form['password'] = password
    form['_eventId'] = 'submit'
    form['signedDuoResponse'] = duo_sign
    form['execution'] = executions[2]
    # for execution_str in executions:
    #     form['execution'] = execution_str
    #     r.append(s.post('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F', data=form))

    r.append(s.post('https://auth.berkeley.edu/cas/login?service=https%3A%2F%2Fcalcentral.berkeley.edu%2Fauth%2Fcas%2Fcallback%3Furl%3Dhttps%253A%252F%252Fcalcentral.berkeley.edu%252F', data=form))

    last = r[-1].history[0]
    loc = last.headers['Location']

    r.append(s.get(loc))

    time.sleep(1)
    r.append(s.get('https://calcentral.berkeley.edu/dashboard'))
    time.sleep(1)
    r.append(s.get('https://services.housing.berkeley.edu/c1c/dyn/login.asp'))
    time.sleep(1)
    r.append(s.get('https://services.housing.berkeley.edu/c1c/dyn/login.asp'))
    time.sleep(1)
    r.append(s.get('https://services.housing.berkeley.edu/c1c/dyn/bals.asp?pln=onfd1'))

    return r, s

username = getpass('Type in your username: ')
password = getpass('Type in your password: ')
phone_no = input('Which phone do you want to use?: ')
r, s = test_login(username, password, phone_no)
p = data_methods.make_parser
data = p(r[-1].text)
fout = open('meal_history.txt', 'w')
fout.write(str(data))
fout.close()
data_methods.plot_expenses(data_methods.get_all_tags(data))

"""
Вроде бы двойную аутентификацию я прохожу. Осталось понять, как именно передать
эту информацию обратно в CAS, чтобы система меня авторизовала. Не очень понятно,
откуда брать новый execution. Подпись DuoRepsponse передается через auth (lines 143-148).
"""
