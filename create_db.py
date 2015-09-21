from werkzeug.security import generate_password_hash, check_password_hash
import fizz_buzz
from flask import g
import sqlite3 as lite
import sys


# |___Users_____|  |___Posts____| |_Comments__|
# |_____id______|  |____id______| |__post id__|
# |__username___|  |___title____| |_nickname__|
# |____email____|  |____body____| |_comment___|
# |____hash_____|  |__timestamp_| |_timestamp_|
# |_permissions_|  |___user id__| |__email____|
# |___open id___|  |__comments__| |_Gravatar__|
#							  


if __name__ == '__main__':
	#pass
	try:
		con = lite.connect('fizz_buzz.db')
		cur = con.cursor()
		hash = generate_password_hash('achtungu206')
		cur.executescript(\
			"""
			DROP TABLE IF EXISTS Users;
			CREATE TABLE Users(id INTEGER PRIMARY KEY, username TEXT, email TEXT, hash TEXT, permissions INT, openid TEXT);
			""")
		cur.execute("INSERT INTO Users(username, email, hash, permissions, openid) \
			VALUES('Sam', 'clarke.sam1@gmail.com', '"+hash+"', 255, '')")
		con.commit()

		cur.executescript(\
			"""
			DROP TABLE IF EXISTS Posts;
			CREATE TABLE Posts(id INTEGER PRIMARY KEY, title TEXT, short TEXT, body TEXT, time TEXT, userid INT);
			""")
		cur.execute("INSERT INTO Posts(title, short, body, time, userid) \
			VALUES('The eagle has landed!', 'The state of affairs is being questioned by significant authorities.', '\
				This is the body of the post, get markup!', '28/2/2015 13:50pm', 1)")
		cur.execute("INSERT INTO Posts(title, short, body, time, userid) \
			VALUES('The eagle has landed!', 'The state of affairs is being questioned by significant authorities.', '\
				This is the body of the post, get markup!', '28/2/2015 13:50pm', 1)")
		cur.execute("INSERT INTO Posts(title, short, body, time, userid) \
			VALUES('The eagle has landed!', 'The state of affairs is being questioned by significant authorities.', '\
				This is the body of the post, get markup!', '28/2/2015 13:50pm', 1)")
		cur.execute("INSERT INTO Posts(title, short, body, time, userid) \
			VALUES('The eagle has landed!', 'The state of affairs is being questioned by significant authorities.', '\
				This is the body of the post, get markup!', '28/2/2015 13:50pm', 1)")
		cur.execute("INSERT INTO Posts(title, short, body, time, userid) \
			VALUES('The eagle has landed!', 'The state of affairs is being questioned by significant authorities.', '\
				This is the body of the post, get markup!', '28/2/2015 13:50pm', 1)")
		con.commit()


	except lite.Error, e:

		if con: con.rollback()
		print 'Error %s' % e.args[0]
		sys.exit(1)

	finally:
		if con:
			con.close()