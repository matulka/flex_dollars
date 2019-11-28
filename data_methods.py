from bs4 import BeautifulSoup
from datetime import date, timedelta
import matplotlib.pyplot as plt

plt.xticks(rotation=60)


def make_parser(html_doc):
    """
    Take in an html string and return a BeautifulSoup parser
    """
    parser = BeautifulSoup(html_doc, 'html.parser')
    return parser

def get_tag_info(tag):
    """
    Take in a <tr> tag and return a tuple of the form:
    (date, expense, new_balance, location)
    """
    tags = tag.find_all('td')
    time_tag = tags[0]
    tag_text = time_tag.text
    month, day, year = tuple(tag_text.split()[0].split('/'))
    this_date = date(year=int(year), month=int(month), day=int(day))
    expense = float(tags[1].text[1:])
    new_balance = float(tags[2].text[1:])
    location = tags[3].text
    return (this_date, expense, new_balance, location)

def get_all_tags(parser):
    """
    Take in a parser with the flex dollar expenses page and return a list of
    infos for each tag (see get_tag_info for more reference)
    """
    infos = list()
    tags = parser.find_all('tr')[2:]
    for tag in tags:
        infos.append(get_tag_info(tag))
    return infos

def plot_expenses(tags_info):
    """
    Gets information about flex dollars expenses for each date and plots them
    using matplotlib.pyplot
    """
    expenses = dict()
    for tag_info in tags_info:
        date, expense, new_balance, locations = tag_info
        if date not in expenses:
            expenses[date] = 0
        expenses[date] += expense
    x, y = [], []
    all_dates = list(expenses.keys())
    min_date, max_date = min(all_dates), max(all_dates)
    curr_date = min_date
    while curr_date <= max_date:
        x.append(curr_date)
        y.append(expenses.get(curr_date, 0))
        curr_date = curr_date + timedelta(days=1)
    plt.plot(x, y)
    plt.show()
