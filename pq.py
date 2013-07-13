# Priority queue for messages
# Zach Hall, 2013

PQ_IMM  = 4 # immediate
PQ_HIGH = 3 # high priority
PQ_MED  = 2 # normal priority
PQ_LOW  = 1 # low priority
PQ_SUB  = 0 # lower than low priority

class PriorityQueue:
	def __init__(self, maxQueueSize):
		self.messages = []		 # list of messages
		self.maxQueueSize = maxQueueSize # maximum size of message list before replacements start occurring
		self.time = 0			 # order of when messages are submitted. goes up with each message
	
	def lowestPriorityIndex(self, lowest):
		"""Returns the index of the message with lowest priority"""
		lowestIndex = None
		
		for i in range(len(self.messages)):
			message = self.messages[i]
			
			if (message[1] < lowest[1]) or (message[1] == lowest[1] and message[2] > lowest[2]):
				# if message has lower priority or both have same priority but message was posted later
				lowest = message
				lowestIndex = i # new lowest message index is i
		return lowestIndex
	
	def hasNext(self):
		"""If there is another message in the queue, return True"""
		return bool(len(self.messages) != 0)
	
	def next(self):
		"""Pops the highest priority message from the list and returns it"""
		if len(self.messages) == 0:
			return None # the queue is empty, don't return anything
		
		highest = ['', float("-inf"), -1] # obviously this will be replaced
		highestIndex = len(self.messages) + 1
		
		for i in range(len(self.messages)):
			message = self.messages[i]
			if (message[1] > highest[1]) or (message[1] == highest[1] and message[2] < highest[2]):
				# if message has higher priority or is older and both messages have same priority
				highest = message
				highestIndex = i # new highest message index is i
		
		return self.messages.pop(highestIndex)
	
	def addMessage(self, priority, message):
		# timestamp (milliseconds) of when message was added. older messages have higher priority.
		timeAdded = self.time
		self.time += 1
		newMessage = [message, priority, timeAdded]
		
		if len(self.messages) < self.maxQueueSize:
			# we can add a message without pruning the list
			self.messages.append(newMessage)
		else:
			# pruning might occur, and we'll replace the lowest priority message
			# don't prune if the message is lower priority than the lowest messages in the queue already
			lowestIndex = self.lowestPriorityIndex(newMessage)
			if lowestIndex is not None:
				self.messages[lowestIndex] = newMessage

if __name__ == '__main__':
	q = PriorityQueue(10)
	q.addMessage(PQ_HIGH, '1')
	q.addMessage(PQ_LOW, '5')
	q.addMessage(PQ_IMM, 'This will be run first, and the next 6 messages will be in numerical order according to the rules above.')
	q.addMessage(PQ_LOW, '6')
	q.addMessage(PQ_MED, '3')
	q.addMessage(PQ_MED, '4')
	q.addMessage(PQ_HIGH,'2')
	
	while q.hasNext():
		print q.next()[0]
	print ''
	
	# overflow test
	q = PriorityQueue(3)
	q.addMessage(PQ_MED, 'chat1')
	q.addMessage(PQ_LOW, 'join1')
	q.addMessage(PQ_HIGH,'kill1')
	q.addMessage(PQ_HIGH,'kill2')
	q.addMessage(PQ_LOW, 'join2')
	
	# remember, older messages should be served first to maintain chronological order
	while q.hasNext():
		print q.next()[0]
