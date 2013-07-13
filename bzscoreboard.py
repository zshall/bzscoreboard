# BZFlag Scoreboard
# Zach Hall, 2013

import subprocess
import re
import sys
import time
import pq

# Uses monitor process code from
# http://stackoverflow.com/questions/5173945/python-monitoring-stderr-and-stdout-of-a-subprocess

# Uses bzadmin

# Pro-Lite TruColorXP (rom 6) templates
inactive = [
	'<ID01><PJ><FU><SD>BZFlag       <FZ>W',
	'<ID01><PW><FU>NOT CONNECTED TO SERVER.             <FZ>X',
	'<ID01><PX><FN><FZ>J'
]

active = {
	'title': '<FU><SD>BZFlag',
	'serverinfo': '<ID01><PK><FC><CB>Hostname: <CM>%s              <FK><CB>Port: <CG>%s             <FZ>I',
	'chat': '<CP>%s says: <CG>%s',
	'join': '<CM>%s <CD>joined the game.',
	'leave': '<CB>%s <CD>left the game.',
	'kill': '<FI><CM>%s <SE><BJ> <SA><CB>%s<FP><FH>',
	'death': '<FJ><SE><BA> <SA><CB>%s<FP><FH>'
}

link = '<ID01><P%s>%s             <FZ>%s'

q = pq.PriorityQueue(3) # the message queue, for sending messages one at a time.
last = 0 # the timestamp of the last message sent
waitingTime = 5

def chain(pages):
	global waitingTime
	waitingTime = 0
	endPage = 'I' # the final page is the title page by default
	nextPages = ['V', 'U', 'T']
	nextPage = ''
	currentPage = 'S'
	firstPage = currentPage
	for i in range(len(pages)):
		message = pages[i][0]
		if i == len(pages) - 1:
			nextPage = endPage # last page
		else:
			nextPage = nextPages.pop()
		sendToSign(link % (currentPage, message, nextPage)) # daisy chain pages together
		print link % (currentPage, message, nextPage)
		time.sleep(0.3) # and prevent sign from crashing by waiting
		waitingTime += 5
		currentPage = nextPage
	time.sleep(0.3)
	runPage(firstPage) # now start the chain

def sendToSign(cmd):
	"""Send a message to the sign right away."""
	subprocess.call(["./sign.sh", cmd])

def runPage(page):
	"""Send a run page command to the sign right away."""
	subprocess.call(["./sign.sh", "<ID01><RP%s>" % page])

def Run(command):
	proc = subprocess.Popen(command, bufsize=1,
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		universal_newlines=True)
	return proc

def Trace(proc):
	global q
	global last
	global link
	global active
	global waitingTime
	
	while proc.poll() is None:
		line = proc.stdout.readline()
		if line:
			print line
			# We are looking for a few things...
			# server name and port
			l = line.split(' ')
			if len(l) < 2 or '[SERVER->]' in line:
				pass
			elif l[0] == 'Connecting':
				parts = l[2].split('@')
				parts = parts[1].split(':')
				hostname = parts[0].strip()
				port = parts[1].strip()
				sendToSign(active['serverinfo'] % (hostname, port))
				runPage('K')
			# joined and left
			elif "joined the game as" in line:
				try:
					user = re.search("'.*'", line).group(0).strip("'")
					q.addMessage(pq.PQ_LOW, active['join'] % (user))
				except IndexError:
					pass
			elif "left the game." in line:
				try:
					user = re.search("'.*'", line).group(0).strip("'")
					q.addMessage(pq.PQ_LOW, active['leave'] % (user))
				except IndexError:
					pass
			# shot messages
			elif "destroyed by" in line:
				try:
					m = re.match("\*\*\* \'(.*)\' destroyed by \'(.*)\'\.", line)
					if m is not None:
						killed = m.group(1).strip("'")
						killer = m.group(2).strip("'")
						q.addMessage(pq.PQ_HIGH, active['kill'] % (killer, killed))
				except IndexError:
					pass
			elif "blew myself up" in line:
				try:
					user = re.search("'.*'", line).group(0).strip("'")
					q.addMessage(pq.PQ_HIGH, active['death'] % (user))
				except IndexError:
					pass
			# chat messages
			elif "    " in line.split(":")[0]:
				try:
					l = line.split(":")
					sender = l[0].strip()
					message = l[1].strip()
					q.addMessage(pq.PQ_MED, active['chat'] % (sender, message))
				except IndexError:
					pass
		# every cycle, check the queue.
		if q.hasNext() and time.time() - last >= waitingTime:
			# we reserve 5 seconds for each message to run
			messages = []
			while q.hasNext():
				messages.append(q.next())
			chain(messages)
			last = time.time()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		# first argument is callsign@hostname
		address = sys.argv[1]
	else:
		address = 'scoreboard@127.0.0.1'
	proc = Run(['bzadmin', '-ui', 'stdout', address])
	Trace(proc)
