from CodeforcesParser import Codeforces_Parser
from data_wrangling import Finals_table

URL = url = open('group_url.txt').read().strip()
with open('log_info.txt', 'r') as u_p:
    USERNAME, PASSWORD = u_p.read().split()
    u_p.close()
    
parser = Codeforces_Parser(URL, USERNAME, PASSWORD)   
parsed_group = parser.full_parse_CF()

t = Finals_table()
for contest in parsed_group:
    t.add_contest(contest)
table = t.concat_and_return_table()
table.to_csv('table.csv')