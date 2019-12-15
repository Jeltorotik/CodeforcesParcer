import pandas as pd

class Finals_table:
    def __init__(self):
        self.table_parts = []
        
        
    def prettify(self, table):
        
        total = table[table > 0].T.count()
        adjust = lambda x: '+' if x == 1 else ('+' + str(x) if x > 1 else str(x))
        table = table.applymap(adjust)
        table.insert(0, 'Всего', total)
        table = table.sort_values(by = 'Всего', ascending=False)
        return table
        
        
    def add_contest(self, contest_info):
        
        sub_columns = [[contest_info['Title']]*len(contest_info['Problems']), contest_info['Problems']]        
        tuples = list(zip(*sub_columns))
        index = pd.MultiIndex.from_tuples(tuples, names = ['Контест', 'Задачи'])
        contest_table = pd.DataFrame(contest_info['Participants'], index = index)
        contest_table = contest_table.T
        
        self.table_parts.append(contest_table)
        
        
    def concat_and_return_table(self):
        
        Main_table = pd.concat(self.table_parts, axis=1)
        Main_table = self.prettify(Main_table)
        return Main_table
