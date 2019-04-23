# parser.py
import requests
from bs4 import BeautifulSoup as bs

# 로그인할 유저정보를 넣어주자 (모두 문자열)
LOGIN_INFO = {
    'userId': 'myidid',
    'userPassword': 'mypassword123'
}

# Session 생성, with 구문 안에서 유지
with requests.Session() as s:
    # 우선 클리앙 홈페이제 들어간다.
    first_page = s.get('https://www.clien.net/service/')
    html = first_page.text
    soup = bs(html, 'html.parser')
    csrf = soup.find('input', { 'name': '_csrf'}) # input태그 중에서 name이 _csrf인 것을 찾습니다.
    print(csrf['value'])

    # 이제 LOGIN_INFO에 csrf값을 넣어줍시다.
    # (p.s.)Python3에서 두 dict를 합치는 방법은 { **dict1, **dict2} 으로 dict들을 unpacking하는 것
    LOGIN_INFO = { **LOGIN_INFO, **{'_csrf': csrf['value']}}
    print(LOGIN_INFO)

    # 이제 다시 로그인
    login_req = s.post('https://www.clien.net/service/login', data=LOGIN_INFO)
    #결과 200이면 성공
    print(login_req.status_code)

    #로그인이 되지 않으면 경고를 띄움
    if login_req.status_code != 200:
        raise Exception('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요')

# -- 로그인 된 세션이 유지됩니다 --
# 이제 장터의 게시글 하나를 가져온다.  중고장터 공지글 예제
post_one = s.get('https://www.clien.net/service/board/rule/10707408')
soup = bs(post_one.text, 'html.parser') 

# 아래 CSS Selector는 공지글 제목
title = soup.select('#div_content > div.post_title.symph_row > h3 > span')
contents = soup.select('#div_content > div.post_view > div.post_content > article > div')

# HTML을 제대로 파싱한 뒤에는 .text속성을 이용합니다.
print(title[0].text) # 글제목의 문자만을 가져와 봅니다
# [0]을 하는 이유는 select로 하나만 가져와도 title 자체는 리스트이기 떄문
# 즉, 제목 글자는 title이라는 리스트의 0번쨰에 들어가 있다.
print(contents[0].text)
