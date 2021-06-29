class NotOneOrMinusOneError(Exception):
	pass

class T3Node:
	def __init__(self,ai,step=None):
		if (ai != 1) and (ai != -1):
			raise NotOneOrMinusOneError()
		self.board = [[0 for i in range(3)] for j in range(3)]
		self.ai = ai #1 == X, -1 == O, maximizer
		self.turn = 1
		self.player = (-1)*ai
		self.step = step

	def available(self):
		res = []
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == 0:
					res.append((i,j))
		return res

	def __str__(self):
		res = ''
		for row in self.board:
			for icol in range(3):
				if row[icol] == 1:
					res += 'X'
				elif row[icol] == -1:
					res += 'O'
				else:
					res += '_'

				if icol == 2:
					res += '\n'
				else:
					res += ' '
		return res

	def insertX(self,row,column):
		self.board[row][column] = 1

	def insertO(self,row,column):
		self.board[row][column] = -1

	def value(self):
		#check horizontal win
		for row in self.board:
			if row[0] == row[1] == row[2]:
				if row[0] == self.ai:
					return 1
				elif row[0] == self.player:
					return -1

		#check vertical win
		for icol in range(3):
			if self.board[0][icol] == self.board[1][icol] == self.board[2][icol]:
				if self.board[0][icol] == self.ai:
					return 1
				elif self.board[0][icol] == self.player:
					return -1

		#check diagonal win
		diagonal1 = self.board[0][0] == self.board[1][1] == self.board[2][2]
		diagonal2 = self.board[0][2] == self.board[1][1] == self.board[2][0]
		if diagonal1 or diagonal2:
			if self.board[1][1] == self.ai:
				return 1
			elif self.board[1][1] == self.player:
				return -1

		if len(self.available()) == 0:
			return 0 #tie

		return None

	def clone(self,step=None):
		res = T3Node(self.ai,step)
		res.board = []
		for row in self.board:
			res.board.append(row[:])
		res.turn = self.turn
		return res

class T3Tree:
	def __init__(self, root):
		self.root = root
		self.leaves = []
		self.value = self.root.value()
		self.optimalStep = None
		self.branch = 0
		self.grow()

	def __str__(self):
		return self.root.__str__()

	def grow(self):
		if self.value == None:
			ava = self.root.available()
			for i in ava:
				newboard = self.root.clone(i)
				if newboard.turn == 1:
					newboard.insertX(i[0], i[1])
					newboard.turn = -1
				elif newboard.turn == -1:
					newboard.insertO(i[0], i[1])
					newboard.turn = 1
				self.branch += 1
				newleaf = T3Tree(newboard)
				self.branch += newleaf.branch
				self.leaves.append(newleaf)

	def minimax(self):
		#game over
		if self.value != None:
			return self.value,self.optimalStep

		#else if not game over
		#if maximize
		if self.root.turn == self.root.ai:
			branchIndicator = self.branch
			for ileaf in self.leaves:
				a = ileaf.minimax()[0]
				if self.value != None:
					if a > self.value:
						self.value = a
						self.optimalStep = ileaf.root.step
					elif a == self.value:
						if branchIndicator > ileaf.branch:
							branchIndicator = ileaf.branch
							self.optimalStep = ileaf.root.step
				else:
					self.value = a
					self.optimalStep = ileaf.root.step
			return self.value,self.optimalStep
		if self.root.turn == self.root.player:
			branchIndicator = self.branch
			for ileaf in self.leaves:
				a = ileaf.minimax()[0]
				if self.value != None:
					if a < self.value:
						self.value = a
						self.optimalStep = ileaf.root.step
					elif a == self.value:
						if branchIndicator > ileaf.branch:
							branchIndicator = ileaf.branch
							self.optimalStep = ileaf.root.step
				else:
					self.value = a
					self.optimalStep = ileaf.root.step
			return self.value,self.optimalStep
if __name__ == '__main__':
	a = input("choose o or x:")
	ai = 1 if a == 'o' else -1
	player = ai*-1
	board = T3Node(ai)
	# board.insertX(1,1)
	# board.insertO(0,0)
	tree = T3Tree(board)
	# print(tree)
	while tree.root.value() == None:
		print(tree)
		if tree.root.turn == player:
			print('your turn:')
			fill1 = int(input('choose row:'))
			fill2 = int(input('choose col:'))
			for ileaf in tree.leaves:
				if ileaf.root.step == (fill1,fill2):
					tree = ileaf
		elif tree.root.turn == ai:
			print('comp turn:')
			optimalStep = tree.minimax()[1]
			for ileaf in tree.leaves:
				if ileaf.root.step == optimalStep:
					tree = ileaf
	print(tree)