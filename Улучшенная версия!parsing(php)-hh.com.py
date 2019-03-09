import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
base_url = 'https://tambov.hh.ru/search/vacancy?search_period=7&clusters=true&area=1&text=PHP+программист&enable_snippets=true'

out = 'parser_php.txt'


def hh_parse(base_url, headers):
    urls = []
    urls.append(base_url)
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all("a", attrs={"data-qa": "pager-page"})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f"https://tambov.hh.ru/search/vacancy?search_period=7&clusters=true&area=1&text=PHP+программист&1&page={i}"
                if url not in urls:
                    urls.append(url)

        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        parser_php_file = open(out, 'a')
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                compensation = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                if compensation == None:
                    compensation = 'Не указанно'
                else:
                    compensation = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                content = 'Условия:\n' + text1 + '\nТребования к кандидату:\n' + text2
                all = title + '\n' + compensation + '\n' + href + '\n' + company + '\n' + content + '\n\n\n\n\n'
                parser_php_file.write(all)
                print(len(all))
            except:
                pass
        parser_php_file.close()

    else:
        print('Парсинг окончен')


hh_parse(base_url, headers)
