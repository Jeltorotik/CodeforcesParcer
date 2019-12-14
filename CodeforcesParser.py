import mechanize
import http.cookiejar
from bs4 import BeautifulSoup
import html2text

def parse_codeforces(url, username, password):
    
    ######Stage 1######
    ####Getting info###
    
    # Browser
    br = mechanize.Browser()
    # Cookie Jar
    cj = http.cookiejar.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Chrome')]

    # The site we will navigate into, handling it's session
    br.open('https://codeforces.com/enter')


    # Select the second (index one) form (the first form is a search query box)
    br.select_form(nr=1)

    # User credentials
    br.form['handleOrEmail'] = username
    br.form['password'] = password

    # Login
    br.submit()

    parsed = br.open(url).read()
    
    
    ####### Stage 2 #######
    ######Processing info
    soup = BeautifulSoup(parsed, 'lxml')
    
    #Problems info
    problems_info = soup.find('tr').findAll('a')
    num_pro = 0
    titles = []
    for problem in problems_info:
        titles.append(problem['title'])
    
    participants = dict()
    for x in soup.findAll('tr'):
        if x.find('a'):
            if x.find('a')['href'].split('/')[1] == 'profile':
                handle = x.find('a')['href'].split('/')[2] # Handle
                participants[handle] = [0] * len(titles)
                i = 0
                for task in x.findAll('span'):
                    if task['class'] != ['cell-time']:
                        if len(task.text) > 1 or task.text == '+': # if task was submitted
                            if task.text == '+': # if accepted on first try
                                participants[handle][i] = 1
                            else:
                                if task['class'] == ['cell-accepted']: #if task was accepted not on a first try
                                    participants[handle][i] = int(task.text) + 1
                                else: # if task still not solved
                                    participants[handle][i] = int(task.text)
                        else: # if task has never been submited
                            participants[handle][i] = 0
                        i += 1
        
    
    return titles, participants