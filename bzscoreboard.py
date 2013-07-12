# BZFlag Scoreboard
# Zach Hall, 2013

import subprocess
import re
import sys

# Uses monitor process code from
# http://stackoverflow.com/questions/5173945/python-monitoring-stderr-and-stdout-of-a-subprocess

# Uses bzadmin

# pro-lite templates
inactive = [
	'<ID01><PI><FU><SD>BZFlag       <FZ>W',
	'<ID01><PW><FU>NOT CONNECTED TO SERVER.             <FZ>X',
	'<ID01><PX><FN><FZ>J'
]

active = {
	'title': '<ID01><PI><FU><SD>BZFlag       <FZ>K',
	'serverinfo': '<ID01><PK><FC><CB>Hostname: <CM>%s              <FK><CB>Port: <CG>%s             <FZ>I',
	'chat': '<ID01><PL><CP>%s says: <CG>%s             <FZ>M',
	'join': '<ID01><PO><CM>%s <CD>joined the game.              <FZ>I',
	'leave': '<ID01><PP><CB>%s <CD>left the game.              <FZ>Y',
	'kill': '<ID01><PQ><FI><CM>%s <SE><BJ> <SA><CB>%s<FP><FH><FZ>I',
	'death': '<ID01><PR><FJ><SE><BA> <SA><CB>%s<FP><FH><FZ>I'
}

def sendToSign(cmd):
	subprocess.call(["./sign.sh", cmd])

def runPage(page):
	subprocess.call(["./sign.sh", "<ID01><RP%s>" % page])

def Run(command):
	proc = subprocess.Popen(command, bufsize=1,
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		universal_newlines=True)
	return proc

def Trace(proc):
	while proc.poll() is None:
		line = proc.stdout.readline()
		if line:
			print line
			# We are looking for a few things...
			# server name and port
			l = line.split(' ')
			if len(l) < 2:
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
					sendToSign(active['join'] % (user))
					runPage('O')
				except IndexError:
					pass
			elif "left the game." in line:
				try:
					user = re.search("'.*'", line).group(0).strip("'")
					sendToSign(active['leave'] % (user))
					runPage('P')
				except IndexError:
					pass
			# shot messages
			elif "destroyed by" in line:
				try:
					m = re.match("\*\*\* \'(.*)\' destroyed by \'(.*)\'\.", line)
					killed = m.group(1).strip("'")
					killer = m.group(2).strip("'")
					sendToSign(active['kill'] % (killer, killed))
					runPage('Q')
				except IndexError:
					pass
			# chat messages
			elif "    " in line.split(":")[0]:
				try:
					l = line.split(":")
					sender = l[0].strip()
					message = l[1].strip()
					sendToSign(active['chat'] % (sender, message))
					runPage('L')
				except IndexError:
					pass
if __name__ == '__main__':
	if len(sys.argv) > 1:
		# first argument is callsign@hostname
		address = sys.argv[1]
	else:
		address = 'scoreboard@127.0.0.1'
	proc = Run(['bzadmin', '-ui', 'stdout', address])
	Trace(proc)
