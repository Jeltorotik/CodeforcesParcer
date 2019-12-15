import mechanize
import http.cookiejar
from bs4 import BeautifulSoup
import html2text


class Codeforces_Parser():
    def __init__(self, group_url, username, password):
        self.URL = group_url
        # authorization
        
        self.br = mechanize.Browser()
        cj = http.cookiejar.LWPCookieJar()
        self.br.set_cookiejar(cj)

        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        self.br.addheaders = [('User-agent', 'Chrome')]

        # The site we will navigate into, handling it's session
        self.br.open('https://codeforces.com/enter')

        # Select the second (index one) form (the first form is a search query box)
        self.br.select_form(nr=1)

        # User credentials
        self.br.form['handleOrEmail'] = username
        self.br.form['password'] = password

        # Login
        self.br.submit()
    
    
    def parse_members(self):
        url = self.URL + '/members'
        parsed = self.br.open(url).read()
        soup = BeautifulSoup(parsed, 'lxml')
        members = []
        for i in soup.findAll('tr'):
            if i.find('a'):
                info = i.find('a')['href'].split('/')
                if info[1] == 'profile':
                    members.append(info[2])
        return members
    
    
    def parse_contests(self):
        url = self.URL + '/contests'
        parsed = self.br.open(url).read()
        soup = BeautifulSoup(parsed, 'lxml')
        contests = []
        for x in soup.findAll('td'):
            if x.find('br'):
                contestId = x.find('a')['href'].split('/')[4]
                title = x.text.split()
                title = ' '.join(title[:(title.index('Enter'))])
                contests.append([contestId, title])

        return contests
        
        
    def parse_standings(self, url):
        parsed = self.br.open(url).read()
        soup = BeautifulSoup(parsed, 'lxml')

        #Problems info
        problems_info = soup.find('tr').findAll('a')
        num_pro = 0
        titles = []
        for problem in problems_info:
            titles.append(problem['title'])
        
        members = self.parse_members()
        participants = dict((m,[0]*len(titles)) for m in members)
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
    
    
    def full_parse_CF(self):
        result = []
        contests = self.parse_contests()
        for contestId, title in contests:
            contest_url = self.URL + '/contest/' + contestId + '/standings'
            problems, participants = self.parse_standings(contest_url)
            contest_info = {'Title' : title, 'Problems' : problems, 'Participants' : participants}
            result.append(contest_info)
        return result