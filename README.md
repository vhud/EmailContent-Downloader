<b>About</b>
<hr>

Email Content Download is simple script to step through an email inbox and through the various parts of each email. The script can strip any field, then save it to a directory of your choice. 

It's made to work with outlook out of the box so it will need some tinkering to work with other providers. 

mlist is a file expected to be in the same directory. Input the email ID of where you'd like the script to start working forward in time, picking through emails. Email IDs are added to the mlist file in chronological order.

Three log files are created, 
serverdrop.log to record every time the email server can't be reached, 
corrupt.log to record an email that can't be decoded, and 
emailgrab.log will have a general info type log of what the scanner is currently up to.

If there's no connection to the email server emailgrab.py will simply log the disconnect and keep polling every 30 seconds by default. Upon reconnection it'll continue at the last entry in mlist.
