#Email Content Download Automation
#
A simple script I built to step through an email inbox and the different parts of each email to strip out what you want, then save it wherever. You can specify if you want to save the body, an attachment with a particular name, any attachment from a particular address, any email as a whole from any address, you get the idea.

I made it to work with outlook so it may need some tinkering to work with other providers. It polls the email server(default is every 30 seconds) via whichever account you set up under connection() and works with a file in the same directory called mlist. mlist is a simple csv of email IDs of the emails already scanned. Once an email is scanned it's email ID is appended to mlist. Since mlist is NV it gives the operator an easy way to manage where the scanning should occur. For instance if you want the scanner to pick apart a few emails from a couple years ago simply put the email ID in mlist of the email that is just chronologically before where you'd like to start scanning. Emailgrab.py will load the last entry in mlist into memory then step backwards through the inbox until it finds a matching email ID. It'll then crawl forward scanning and stripping each email according to the parseit() functions specified in the main() loop. Every time it's done scanning an email it'll append the email ID to mlist. Once it's caught up to the present it'll poll the email server every 30 seconds(obviously adjustable) looking for a new email.

emailgrab.py doesn't create the mlist file, so you'll have to create an empty file and simply enter the email ID where you'd like it to start scanning from followed by a comma(since it's treated a csv, although without using the csv library).

If used properly the mlist file becomes a handy chronological record of all email IDs for a particular inbox and a nice tool to position the scanner in a particular location without having to mess with any code(since when emailgrab.py runs it grabs the last email ID in mlist and starts stepping backwards through the inbox looking for a match).

Three log files are created, logReconnect() to record every time the email server can't be reached, logCorruption() to record an email that can't be decoded, and emailgrab.log will have a general info type log of what the scanner is currently up to.

If there's no connection to the email server emailgrab.py will simply log the disconnect and keep polling every 30 seconds by default. Upon reconnection it'll continue where it left off.

At this point it should go without saying but if emailgrab.py is killed or crashes it'll start off at the last email ID in mlist when it's started back up. If you feel there's some sort of error or bad loop the first thing to try is to erase a few email IDs in mlist and restart emailgrab.py then watch the logs.

This can be refactored to use logger and csv libs, if you do so let me know!
