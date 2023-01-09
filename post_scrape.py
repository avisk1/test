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

import sqlite3
db = sqlite3.connect("/home/aris/Documents/DMOJComments/data.db")
cursor = db.cursor()

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--no-sandbox")  # Last I checked this was necessary.
driver = webdriver.Chrome("/home/aris/Documents/DMOJComments/chromedriver", chrome_options=options)

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
			comment_text = comment_text + "\n(" + ",".join(new_links) + ")"
# print("frewak you python")

			# comment_text = comment_text + "\n(" + ",".join(new_links) + ")"



        # if "<img" in comment_html:
            #only works for one image, update this change it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! HERE!!!!
            #Also fix the older messages with only "" that have an image, and put this code in rss.py too
            # img = comment_html.split("<img")
            # comment_text = comment_text + img.split("src=\"")[1].split("\"")[0]
			# print(comment_text)
            # img.split("src=\"")[1].split("\"")[0]
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
			#remove this soon
            #Updates it, should I have this? Prob not
			# cursor.execute("SELECT Upvotes FROM DMOJComments WHERE CommentID == (?)", (comment_id,))
			print(url + "#" + comment_id) #up 1
			# print(comment_score) #down 1
			# cursor.execute("UPDATE DMOJComments SET Upvotes = (?) WHERE CommentID == (?)", (comment_score, comment_id))
			# db.commit()
			# cursor.execute("SELECT Upvotes FROM DMOJComments WHERE CommentID == (?)", (comment_id,))
			# print(cursor.fetchall()) #down 1
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
	# print("Total comments added: " + str(comments_added))
	return comments_added

#Problem - images are not included in innerText :(
#codeforces next: https://codeforces.com/blog/entry/107932
# x = 10 #next one is 8!
for x in range(8, 99):
    print("================================== " + str(x) + " ================================")
    driver.get("https://dmoj.ca/blog/" + str(x))
    contest_links = driver.find_elements(By.CLASS_NAME, "title")
    for i in range(len(contest_links)):
        actual_link = contest_links[i].find_element(By.TAG_NAME, "a")
        link = actual_link.get_attribute("href")
        contest_links[i] = link

    total = 0
    for i in contest_links:
        total += get_all_comments(i, True)
    print("Total comments added: " + str(total))

#Start at 8!!!