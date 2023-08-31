import pandas as pd
def parse_csv():
    pipls = pd.read_csv('Контакты учеников.tsv', delimiter='\t', encoding='utf-8')
    teachers = pd.read_csv('Контакты учителей.tsv', delimiter='\t', encoding='utf-8')
    emails = list(pipls['e-mail ребенка']) + list(teachers['Email'])
    for i in range(len(emails)):
        try:
            emails[i] = str(emails[i]).lower()
            if (str(emails[i]).find('@') == -1):
                del emails[i]
        except:
            break
    print(emails)
    return emails
