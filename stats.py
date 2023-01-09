import sqlite3
db = sqlite3.connect("/home/aris/Documents/DMOJComments/data.db")
cursor = db.cursor()

cursor.execute("SELECT Upvotes from DMOJComments ORDER BY Upvotes")
upvotes = cursor.fetchall()

avg = 0
for i in upvotes:
	avg += i[0]
avg /= len(upvotes)
# print("average:" + str(avg))
positive = 0
zero = 0
negative = 0
for i in upvotes:
	if i[0] > 0:
		positive += 1
	elif i[0] < 0:
		negative += 1
	else:
		zero += 1
#Applies the fetched data

output = """## I am the DMOJ Comment Guru. ##
----------------------------------------------------------------------------------

the time when I got muted was around the beginning of december+, so just go from all comments that were added in december and downvote them all with my main account

## User Stats ##\n
"""

#YouGotBamboozled -> idontgetpointers


#Gets the most downvoted comment url, username, and upvotes
cursor.execute("SELECT CommentURL,Username,Upvotes FROM DMOJComments WHERE Upvotes == (?)", (upvotes[0][0],))
most_downvoted = cursor.fetchall()[0]
output += "[Most downvoted DMOJ comment by](%s) [user:%s] (%s) (can this hit 1000 downvotes?)" % most_downvoted + "\n\n"

#Gets the most upvoted comment url, username, and upvotes
cursor.execute("SELECT CommentURL,Username,Upvotes FROM DMOJComments WHERE Upvotes == (?)", (upvotes[len(upvotes) - 1][0],))
most_upvoted = cursor.fetchall()[0]
output += "[Most upvoted DMOJ comment by](%s) [user:%s] (+%s)" % most_upvoted + "\n\n"

cursor.execute("SELECT Username FROM DMOJComments")
users = cursor.fetchall()

unique_users = []

for i in users:
	dupe = False
	for j in unique_users:
		if i[0] == j:
			dupe = True
			break
	if (dupe == False):
		unique_users.append(i[0])


users = unique_users
#Gets all comment IDs and sorts them by value

biggest = -99999
smallest = 99999
username_big = ""
username_small = ""
for i in users:
	cursor.execute("SELECT Upvotes FROM DMOJComments WHERE Username == (?)", (i,))
	votes = cursor.fetchall()
	total = 0
	for j in votes:
		total += j[0]
	if total > biggest:
		biggest = total
		username_big = i
	if total < smallest:
		smallest = total
		username_small = i

output += "Highest total comment score (+%s): [user:%s]" % (biggest, username_big) + "\n\n"

output += "Lowest total comment score (%s): [user:%s]" % (smallest, username_small) + "\n\n"

output += "## General Stats ##\n\n"

cursor.execute("SELECT ProblemName FROM DMOJComments")
problems = cursor.fetchall()

unique_problems = []

for i in problems:
	dupe = False
	for j in unique_problems:
		if i[0] == j:
			dupe = True
			break
	if (dupe == False):
		unique_problems.append(i[0])

# output += str(len(unique_problems))

output += "**%s** problems or posts have at least one comment\n\n" % (str(len(unique_problems)),)

cursor.execute("SELECT CommentID FROM DMOJComments ORDER BY CommentID")
ids1 = cursor.fetchall()

#Replace above with belo!!!
# cursor.execute("SELECT COUNT(DISTINCT ProblemName) FROM DMOJComments")
#gets how many different DMOJ problems that were scraped
# print(cursor.fetchall())

# COUNT(DISTINCT c)

#Lists the IDs by their order
id_list = []
for i in ids1:
	id = int(i[0][i[0].index("-") + 1:])
	dupe = False
	for j in id_list:
		if id == j:
			dupe = True
			break
	if (dupe == False):
		id_list.append(id)
#Gets all comment IDs and sorts them by value
id_list.sort()

cursor.execute("SELECT Comment FROM DMOJComments")
total_com = len(cursor.fetchall())

output += ("**%s** public comments\n\n" % (total_com,))

output += ("**%s** *total* comments (including deleted ones)\n\n" % (id_list[len(id_list) - 1],))

#put this all in a text document for easy pasting, and make a default document for all the titles and stuff


sum = positive + zero + negative
positive_percent = (positive / sum) * 100
zero_percent = (zero / sum) * 100
negative_percent = (negative / sum) * 100

total_upvotes = 0
for i in upvotes:
	total_upvotes += i[0]
output += ("Collective comment score of **+%s**\n\n" % (str(total_upvotes),))
#assuming it isn't negative
output += ("An average of **+%s** upvotes per comment\n\n" % (str(round(total_upvotes / sum, 3)),))
output += ("**%s** of comments are positive\n\n" % ((str(positive) + " (" + str(round(positive_percent, 3)) + "%)"),))
output += ("**%s** of comments are negative\n\n" % ((str(negative) + " (" + str(round(negative_percent, 3)) + "%)"),))
output += ("**%s** of comments are zero\n\n" % ((str(zero) + " (" + str(round(zero_percent, 3)) + "%)"),))

output += "*Last updated December 1st 2022* (will be updated at the end of each month)\n\n\n\n"

static = """## Personal Favourites ##

Best comment chains: https://dmoj.ca/problem/bts17p1#comment-6294, https://dmoj.ca/problem/tsoc15c1p5#comment-1089, https://dmoj.ca/problem/ccc22s3#comment-17405, https://dmoj.ca/problem/ccc14j2#comment-18745, https://dmoj.ca/problem/ecoo18r1p2#comment-18207

Best censored comments: "This Problem is too difficult, please consider updating the statement to improve clarity, and include a sample input. Edit - Finally AC! My spelling was incorrect, had to debug for a few minutes... :(
 Sample cases would have improved this process." - [user:jorgebean]

"Onepiece is the best anime why is it rated 8.62 it's the best there isn't any anime better it should be 10 out of 10 because it is the best anime of all time even better than naruto and bleach and gate it is just so good you have to watch it all other anime is inferior because onepiece is better it's the best." - [user:John]

"this website is bullshit, i should be able to see the input and output for the other test cases i failed. how is test case 1 is working but the other test cases is not? because i can't see the other test cases i have no idea why. don't get me wrong, you can get a clue of the problem by checking the problem statement again, but if there is no clue there, your fucked. this website has to evolve, goddamn it." - [user:farisalwany]

Best comments: https://dmoj.ca/problem/helloworld#comment-7739, https://dmoj.ca/problem/helloworld#comment-13053, https://dmoj.ca/contest/dmopc20c7#comment-15400, https://dmoj.ca/post/32-dmoj-api#comment-17508, https://dmoj.ca/problem/ecoo18r1p2#comment-18207, https://dmoj.ca/problem/ecoo18r1p2#comment-18207, https://dmoj.ca/problem/ccc14j2#comment-18769

**Note - the comment score values are static, so they are never updated

----------------------------------------------------------------------------------


People who stalk me:
[user:fbain1]


  [1]: https://dmoj.ca/problem/ccc20s5#comment-11776
  [2]: https://dmoj.ca/problem/ccoqr16p3#comment-4093
  [3]: https://dmoj.ca/problem/tsoc15c1p5#comment-1089
  [4]: https://dmoj.ca/problem/ccoqr16p3#comment-4093"""

# #Gets the most downvoted comment
# cursor.execute("SELECT CommentURL FROM DMOJComments WHERE Upvotes == (?)", (upvotes[0][0],))
# print(cursor.fetchall()[0])
# #Gets the most upvoted comment
# cursor.execute("SELECT CommentURL FROM DMOJComments WHERE Upvotes == (?)", (upvotes[len(upvotes) - 1][0],))
# print(cursor.fetchall()[0])

output += static

print(output)




"""## I am the DMOJ Comment Guru. ##
----------------------------------------------------------------------------------


## User Stats ##

[Most downvoted DMOJ comment by][1] [user:j9292002] (-145) (can this hit 1000 downvotes?)

[Most upvoted DMOJ comment by][2] [user:bruce] (+164)

Highest total comment score (+1,109): [user:Xyene]

Lowest total comment score (-139): [user:j9292002]

Most comments: 

## General Stats ##

**1,511** problems have at least one comment

**7,504** public comments

**18,900** *total* comments, most likely meaning that **11,396** comments have been removed or lie on contest pages. If there are roughly 19 * 20 = 380 contests, and if the average amount of comments per contest is roughly 1, then that is 380 extra comments, which does not make a significant impact in the leftover 11,396 comments. Therefore approximately **11,016** comments have been removed from DMOJ, or **58%**. This means that the comment survival rate on DMOJ is **42%**.

Collective comment score of **+15,503**

An average of **+2.066** upvotes per comment

**47.4%** of comments are positive

**36.2%** of comments are negative

**16.4%** of comments are zero

*Last updated October 2022* (will be updated at the end of each month)

 
 

## Personal Favourites ##

Best comment chains: https://dmoj.ca/problem/bts17p1#comment-6294, https://dmoj.ca/problem/tsoc15c1p5#comment-1089, https://dmoj.ca/problem/ccc22s3#comment-17405, https://dmoj.ca/problem/ccc14j2#comment-18745, https://dmoj.ca/problem/ecoo18r1p2#comment-18207

Best censored comments: "This Problem is too difficult, please consider updating the statement to improve clarity, and include a sample input. Edit - Finally AC! My spelling was incorrect, had to debug for a few minutes... :(
 Sample cases would have improved this process." - [user:jorgebean]

"Onepiece is the best anime why is it rated 8.62 it's the best there isn't any anime better it should be 10 out of 10 because it is the best anime of all time even better than naruto and bleach and gate it is just so good you have to watch it all other anime is inferior because onepiece is better it's the best." - [user:John]

"this website is bullshit, i should be able to see the input and output for the other test cases i failed. how is test case 1 is working but the other test cases is not? because i can't see the other test cases i have no idea why. don't get me wrong, you can get a clue of the problem by checking the problem statement again, but if there is no clue there, your fucked. this website has to evolve, goddamn it." - [user:farisalwany]

Best comments: https://dmoj.ca/problem/helloworld#comment-7739, https://dmoj.ca/problem/helloworld#comment-13053, https://dmoj.ca/contest/dmopc20c7#comment-15400, https://dmoj.ca/post/32-dmoj-api#comment-17508, https://dmoj.ca/problem/ecoo18r1p2#comment-18207, https://dmoj.ca/problem/ecoo18r1p2#comment-18207, https://dmoj.ca/problem/ccc14j2#comment-18769

Comments complaining about DMOJ:



----------------------------------------------------------------------------------


People who stalk me:
[user:fbain1]


  [1]: https://dmoj.ca/problem/ccc20s5#comment-11776
  [2]: https://dmoj.ca/problem/ccoqr16p3#comment-4093
  [3]: https://dmoj.ca/problem/tsoc15c1p5#comment-1089
  [4]: https://dmoj.ca/problem/ccoqr16p3#comment-4093"""