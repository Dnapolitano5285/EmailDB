import sqlite3

# open connection to dbfile
conn = sqlite3.connect('emaildb1.sqlite')
cur = conn.cursor()

# execute a command to drop table if need be
cur.execute('''
DROP TABLE IF EXISTS Counts''')

# create the table from scratch
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

# open connection to file we want to read and parse the strings with splits
fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    org = pieces[1].split('@')
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org[1],))
    # fetchone is the default way to return the next row from cursor
    row = cur.fetchone()
    # here we protect against getting a blank row back, where is the row
    # is blank we then add the row, if not we increment
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org[1],))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org[1],))
    # we have to commit the changes to the db for it to be written to disk
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

# this is an example of iteration in SQL file, we created the select string and then
# we step through the resultant cursor one line at a time
# we get back list which is why we use [0] and [1]
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

# do not forget to close cursor
cur.close()
