from bs4 import BeautifulSoup
from datetime import date, timedelta
import matplotlib.pyplot as plt

plt.xticks(rotation=60)

TEST_DOC = """
<head>
    <style type="text/css">
        .auto-style1 {
            height: 19px;
        }
    </style>
</head>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="initial-scale=1">
<meta name="description" content="UC Berkeley's official ID, debit, and access card." />
<title>Cal 1 Card: View Current Transactions</title>
<!-- Le styles -->

<link href="https://cal1card.berkeley.edu/sites/default/files/d.css" rel="stylesheet">

<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
var pageTracker = _gat._getTracker("UA-3211473-1");
pageTracker._initData();
pageTracker._trackPageview();
</script>

</head>

<body class="html">

<div class="background-with-image clearfix">


    <div class="clearfix header_wrapper">
    	<div class="header_top_container container">
      		<div class="header_top clearfix">
				<div class="logo">
                	<a href="https://cal1card.berkeley.edu" title="Home" rel="home">
                    	<img src="https://cal1card.berkeley.edu/sites/default/files/cal_1_card_logo.png" alt="Home"></a>
					<img src="https://cal1card.berkeley.edu/sites/default/files/bar.png">
				</div>

        		<div class="logo">
                	<a href="http://www.berkeley.edu/" title="Home" rel="home">
                    	<img src="https://cal1card.berkeley.edu/sites/default/files/ucberkeley_logo.png" alt="Home"></a>
                </div>

      </div>
    </div>

    <div class="header_bottom">
		<div class="container">
			<div class="header_bottom-inner clearfix">
				<div class="main_menu">
					<div class="menu-block-wrapper menu-block-2 menu-name-main-menu parent-mlid-0 menu-level-1">
						<ul class="menu">
                        	<li class="dummy">&nbsp;</li>



                    	</ul>
               		</div>
				</div>
			</div>
		</div>
    </div>
  </div>


  <div class="container">
	<div class="header_bar">
	<h1>View Current Transactions</h1>
		</div>
	</div>

	<div class="container clearfix">
		<div class="content_main_bg">
     		<div class="node node-landing-page-type-1">
				<div class="cols4 clearfix">
					<div class="col2">

						<div class="content_main">


<div class="blue"><a class="top2" href="login.asp">Main Menu</a></div>


<div class="blue"><a class="top2" href="https://csweb.housing.berkeley.edu/login">Laundry Web</a>
</div>
<div class="blue"><a class="top2" href="balance.asp">View Balances</a>
</div>
<div class="blue"><a class="top2" href="lostnew.asp">Deactivate Lost Card</a></div>


<div class="blue"><a class="top2" href="quit.asp">Calnet Logout</a>
</div>


						</div>
						</div>
                        <div class="col3">
                        <div class="content_main">
<p></p>


<table width="96%" border="0" cellpadding="0" cellspacing="0" bordercolor="#eeeeee" align="center" valign="top" class="bodytext">



<TR>
<th colspan=4><B>On-Campus Meal Plan Flex Dollars Activity</B></th>
</tr>

<TR>
<th align="left">Posted</th>
<th align="left">Amount</th>
<th align="left">New Balance</th>
<th align="left">Location</th>
</tr>


<tr>
<td>11/26/2019 5:03:19 PM</td>
<td>$3.95</td>
<td>$24.80</td>
<td>RSF Pro Shop</td>

</tr>

<tr>
<td>11/20/2019 4:18:01 PM</td>
<td>$14.05</td>
<td>$28.75</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>11/16/2019 9:41:02 AM</td>
<td>$8.25</td>
<td>$42.80</td>
<td>The Den</td>

</tr>

<tr>
<td>11/14/2019 3:25:40 PM</td>
<td>$3.95</td>
<td>$51.05</td>
<td>RSF Pro Shop</td>

</tr>

<tr>
<td>11/7/2019 5:00:31 PM</td>
<td>$3.95</td>
<td>$55.00</td>
<td>RSF Pro Shop</td>

</tr>

<tr>
<td>11/5/2019 6:14:09 PM</td>
<td>$4.80</td>
<td>$58.95</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>11/2/2019 5:02:04 PM</td>
<td>$7.00</td>
<td>$63.75</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>11/2/2019 12:08:37 PM</td>
<td>$6.00</td>
<td>$70.75</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/31/2019 5:08:07 PM</td>
<td>$3.95</td>
<td>$76.75</td>
<td>RSF Pro Shop</td>

</tr>

<tr>
<td>10/29/2019 3:17:49 PM</td>
<td>$4.90</td>
<td>$80.70</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>10/26/2019 7:28:54 PM</td>
<td>$7.00</td>
<td>$85.60</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/26/2019 11:54:00 AM</td>
<td>$6.00</td>
<td>$92.60</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/25/2019 4:12:42 PM</td>
<td>$4.80</td>
<td>$98.60</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>10/19/2019 5:27:02 PM</td>
<td>$7.00</td>
<td>$103.40</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/19/2019 10:38:09 AM</td>
<td>$6.00</td>
<td>$110.40</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/17/2019 4:20:16 PM</td>
<td>$8.50</td>
<td>$116.40</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>10/17/2019 4:14:14 PM</td>
<td>$4.30</td>
<td>$124.90</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>10/16/2019 4:18:07 PM</td>
<td>$4.90</td>
<td>$129.20</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>10/15/2019 5:08:39 PM</td>
<td>$3.95</td>
<td>$134.10</td>
<td>RSF Pro Shop</td>

</tr>

<tr>
<td>10/12/2019 12:11:28 PM</td>
<td>$6.00</td>
<td>$138.05</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/5/2019 7:00:00 PM</td>
<td>$9.00</td>
<td>$144.05</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/5/2019 6:59:54 PM</td>
<td>$7.00</td>
<td>$153.05</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/5/2019 1:19:09 PM</td>
<td>$6.00</td>
<td>$160.05</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>10/4/2019 4:19:34 PM</td>
<td>$10.75</td>
<td>$166.05</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/28/2019 9:25:43 AM</td>
<td>$8.25</td>
<td>$176.80</td>
<td>The Den</td>

</tr>

<tr>
<td>9/26/2019 4:34:57 PM</td>
<td>$13.30</td>
<td>$185.05</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/25/2019 4:31:30 PM</td>
<td>$4.30</td>
<td>$198.35</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/25/2019 4:14:56 PM</td>
<td>$10.75</td>
<td>$202.65</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/23/2019 1:21:38 PM</td>
<td>$7.95</td>
<td>$213.40</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/21/2019 6:37:19 PM</td>
<td>$7.00</td>
<td>$221.35</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>9/21/2019 12:02:55 PM</td>
<td>$6.00</td>
<td>$228.35</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>9/20/2019 6:40:57 PM</td>
<td>$7.00</td>
<td>$234.35</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>9/20/2019 12:49:16 PM</td>
<td>$6.00</td>
<td>$241.35</td>
<td>Crossroads</td>

</tr>

<tr>
<td>9/19/2019 3:00:58 PM</td>
<td>$4.80</td>
<td>$247.35</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/19/2019 2:07:48 PM</td>
<td>$8.25</td>
<td>$252.15</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/17/2019 2:12:07 PM</td>
<td>$7.95</td>
<td>$260.40</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/17/2019 12:02:56 PM</td>
<td>$5.25</td>
<td>$268.35</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/14/2019 12:54:56 PM</td>
<td>$6.00</td>
<td>$273.60</td>
<td>Clark Kerr</td>

</tr>

<tr>
<td>9/13/2019 2:04:50 PM</td>
<td>$7.95</td>
<td>$279.60</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/13/2019 10:47:30 AM</td>
<td>$7.35</td>
<td>$287.55</td>
<td>Golden Bear</td>

</tr>

<tr>
<td>9/11/2019 9:24:53 PM</td>
<td>$5.10</td>
<td>$294.90</td>
<td>The Den</td>

</tr>


</table>


</div>

</div>
</div>
</div>
</div>
</div>
<div class="footer">
    	<div class="container">
			<div class="footer_inner clearfix">
				<div class="cols4 clearfix">
                <div class="footer_fourth_bottom">
						<p>Copyright <script>document.write(new Date().getFullYear())</script> UC Regents; All Rights Reserved</p>
            		</div>
					<div class="col2 footer_social_links">

						<div style="height: 1px;">&nbsp;</div>

                    </div>
					<div class="col footer_menu">
					<div style="height: 1px;">&nbsp;</div>
				</div>
				<div class="col">

          		</div>
        	</div>
      		</div>
		</div>
	</div>

<!-- END page -->

</div>
</body>
</html>
"""


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


soup = make_parser(TEST_DOC)
plot_expenses(get_all_tags(soup))
