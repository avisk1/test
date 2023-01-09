from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))
display.start()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException

from os.path import expanduser
import datetime

#Now, just check the database if it exists, not comments.txt. The comments file is effectively useless

file = open(expanduser("~") + '/Desktop/TADAH.txt', 'w')
file.write("It worked!\n" + str(datetime.datetime.now()))
file.close()


options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--no-sandbox")  # Last I checked this was necessary.
driver = webdriver.Chrome("/home/aris/Documents/DMOJComments/chromedriver", chrome_options=options)
# driver = webdriver.Chrome("/home/aris/Documents/chromedriver")

driver.get("https://dmoj.ca/feed/comment/rss/")

text = driver.find_element(By.TAG_NAME, "pre").get_attribute("innerText")
items = text.split("<item>")
items.pop(0)
items = "".join(items).split("</item>")
items.pop()

#forgot to login ever since ~Oct 15 so go over everything and downvote and login and get new downvotes
logged_in = False

#Function to login
def login():
	#Goes to that URL
	driver.get("https://dmoj.ca/accounts/login/?next=")
	#Finding elements with Selenium
	driver.find_element(By.ID, "id_username").send_keys("YouGotBamboozled")
	driver.find_element(By.ID, "id_password").send_keys("idontgetpointers")
	driver.find_element(By.TAG_NAME, "button").click()
	#Accessing the global variable
	global logged_in
	logged_in = True

# comments_file = open("comments.txt", "w")

# comments_file.write("First Line\n")
# comments_file.write("Second Line\n")
# comments_file = open("/home/aris/Documents/comments.txt")
# content = comments_file.read()

# comments_list = content.split("[placeholderhereyay]")
# comments_list.pop()

# new_comments = []
#
# for i in items:
#     exit = False
#     prev = 0
#     for j in comments_list:
#         if j == i:
#             exit = True
#             break
#         prev = j
#         # print("-->" + j + "<--")
#         # print("-->" + i + "<--")
#     if exit == True:
#         continue
#     # print("-->" + prev + "<--")
#     # print("-->" + i + "<--")
#     new_comments.append(i)
#

# print("new comments:")
# print(str(len(new_comments)) + "/" + str(len(items)))
#
# append_me = ""
# for i in new_comments:
#     append_me += i + "[placeholderhereyay]"

# comments_file = open("/home/aris/Documents/comments.txt", "w")
# comments_file.write(content + append_me) #might need a "\n" here?

def get_tag(body, tag):
    return body.split("<" + tag + ">")[1].split("</" + tag + ">")[0]

def format(comment):
    title = get_tag(comment, "title")
    title = title.replace("&gt;", "")
    link = get_tag(comment, "link")
    description = get_tag(comment, "description").replace("&lt;/p&gt;", "").replace("&lt;p&gt;", "")
    # description = get_tag(comment, "description").split("&lt;p&gt;")
    # description = description[len(description) - 1].split("&lt;/p&gt;")[0]
    date = get_tag(comment, "pubDate")
    print(title + "\n" + link + "\n" + description + "\n" + date)

#do more DMOJ

import sqlite3
db = sqlite3.connect("/home/aris/Documents/DMOJComments/data.db")
cursor = db.cursor()

# tupy = ("test", "te", "d", "url" + "#" + "comment_id", "time_rel", 3, "comment_id", "str(datetime.datetime.now())", "header", "reply_id")
#
# cursor.execute("INSERT INTO DMOJComments VALUES (?,?,?,?,?,?,?,?,?,?)", tupy)
# db.commit()
#
# cursor.execute("SELECT * FROM DMOJComments WHERE CommentID == 'comment-18982'")
# print(cursor.fetchall())
# cursor.execute()


cursor.execute("SELECT CommentURL FROM DMOJComments WHERE Comment == ''")
links = cursor.fetchall()

# for i in links:
# 	driver.get(i[0])
# 	c = driver.find_element(By.ID, i[0][(i[0].index("#") + 1):])
# 	comment_container = c.find_element(By.CLASS_NAME, "comment-body")
# 	comment_text = comment_container.get_attribute("innerText")
# 	comment_html = comment_container.get_attribute("innerHTML")
# 	new_links = []
# 	if "src=" in comment_html:
# 		substr = "src="
# 		index = 0
# 		for d in range(len(comment_html)):
# 			if comment_html[d] == substr[index]:
# 				index += 1
# 			else:
# 				index = 0
# 			if index == len(substr):
# 				index = 0
# 				#comment_html[c] == "="
# 				for q in range(d + 2, len(comment_html)):
# 					if comment_html[q] == "\"":
# 						link = comment_html[(d+2):q]
# 						if link not in new_links:
# 							new_links.append(link)
# 						break
# 	comment_text = comment_text + "\n(" + ",".join(new_links) + ")"
# 	# print(comment_text)
# 	cursor.execute("UPDATE DMOJComments SET Comment = (?) WHERE CommentID == (?)", (comment_text, i[0][(i[0].index("#") + 1):]))
# 	db.commit()
# 	cursor.execute("SELECT Comment FROM DMOJComments WHERE CommentID == (?)", (i[0][(i[0].index("#") + 1):],))
# 	print(cursor.fetchall())


new_comments = []
for i in items:
    link = get_tag(i, "link")
    id = link[link.index("#") + 1:]
    cursor.execute("SELECT * FROM DMOJComments WHERE CommentID == (?)", (id,))
    if (len(cursor.fetchall()) == 0):
        new_comments.append(i)

print("New comments:")
print(str(len(new_comments)) + "/" + str(len(items)))


for i in new_comments:
    format(i)
    print("\n")

unique_links = []
for i in new_comments:
    link = get_tag(i, "link")
    core_link = link[:link.index("#")]
    if core_link not in unique_links: #I love you python
        unique_links.append(core_link)

print("=====================================================================================================================")
print("=====================================================================================================================")
print("\n")

#Though I guess I could get rid of comments.txt and just use the database. Actually yes, I should do this.
#Never mind, I was wrong
#Now all that needs to be done is make the below function take values from the RSS file instead of the 10 newest comments
def get_all_comments(url, logs = False):
	if logged_in == False: login()
	driver.get(url)
	comments_added = 0
	comment_list = driver.find_elements(By.CLASS_NAME, "comment")
	header = driver.find_element(By.TAG_NAME, "h2").get_attribute("innerText")
	for c in comment_list:
		comment_id = c.get_attribute("id")
		reply_id = c.find_element("xpath", "..").get_attribute("id")
		if ("-children" in reply_id):
			reply_id = reply_id[:reply_id.index("-children")]
		reply_id = c.find_element("xpath", "..").get_attribute("id")
		if ("-children" in reply_id):
			reply_id = reply_id[:reply_id.index("-children")]
		#reply_id is "" if it doesn't have an id
		comment_container = c.find_element(By.CLASS_NAME, "comment-body")
		comment_text = comment_container.get_attribute("innerText")
		comment_html = comment_container.get_attribute("innerHTML")
		new_links = []
		if "src=" in comment_html:
			substr = "src="
			index = 0
			for d in range(len(comment_html)):
				if comment_html[d] == substr[index]:
					index += 1
				else:
					index = 0
				if index == len(substr):
					index = 0
					#comment_html[c] == "="
					for q in range(d + 2, len(comment_html)):
						if comment_html[q] == "\"":
							link = comment_html[(d+2):q]
							if link not in new_links:
								new_links.append(link)
							break
		# print("asdfasdasd")
		#should be indented so comment_text only changes if src is in the comment
			comment_text = comment_text + "\n(" + ",".join(new_links) + ")"

		comment_score = c.find_element(By.CLASS_NAME, "comment-score").get_attribute("innerText")
		user_el = c.find_element(By.CLASS_NAME, "rating").find_element(By.TAG_NAME, "a")
		#Sometimes the following line might throw an error, I think it's on DMOJ's end
		user_url = user_el.get_attribute("href")
		username = user_el.get_attribute("innerText")
		time_rel = c.find_element(By.CLASS_NAME, "time-with-rel").get_attribute("data-iso")

		#Useful: https://pyquestions.com/concatenate-strings-in-python-in-multiline

		#Don't use f-strings, they're prone to SQL injection (even though that would never happen with a school project)

		tupy = (username, comment_text, user_url, url + "#" + comment_id, time_rel, comment_score, comment_id, str(datetime.datetime.now()), header, reply_id)

		cursor.execute("SELECT * FROM DMOJComments WHERE CommentID == (?)", (comment_id,))
		result = cursor.fetchall()
		if (len(result) == 0):
			cursor.execute("INSERT INTO DMOJComments VALUES (?,?,?,?,?,?,?,?,?,?)", tupy)
			print("New comment found. Appending...")
			comments_added += 1
			db.commit()
			if logs == True:
				print(tupy)
		#useful tool for setting new values
		elif (result[0][9] == None):
			cursor.execute("UPDATE DMOJComments SET Reply = (?) WHERE CommentID == (?)", (reply_id, comment_id))
			db.commit()
		else:
			print("Duplicate found. Ignoring...")
	info = driver.find_elements(By.CLASS_NAME, "info-float")
	if len(info) != 0:
		info = info[0]
		divs = info.find_elements(By.TAG_NAME, "div")
		for div in divs:
			a = div.find_elements(By.TAG_NAME, "a")
			if (len(a) != 0):
				url = a[0].get_attribute("href")
				if "editorial" in url:
					get_all_comments(url)
					break
	print("Total comments added: " + str(comments_added))
	return comments_added

for i in unique_links:
    get_all_comments(i, True)

# if len(new_comments) == 0:
#     driver.get("https://replit.com/@avisk/Python-SeleniumSQL-pronounced-es-queue-el#main.py")
#     # driver.get("https://replit.com/login")
#     # driver.find_element(By.CLASS_NAME, "css-o4584k").click()
#     driver.find_element("xpath", "//*[text()='Log in']").click()
#     driver.find_element(By.ID, "1val-input").send_keys("avisk")
#     driver.find_element(By.ID, "2val-input").send_keys("idontgetpointers")
#     driver.find_element(By.CLASS_NAME, "css-ifshk5").click()
