class Board:
	def __init__(self,turn,ai):
		self.board = [0 for i in range(9)]
		self.turn = turn
		self.maximizer = ai

	def insert(self,i):
		b = Board(-1 * self.turn,self.maximizer)
		b.board = self.board[:]
		b.board[i] = self.turn
		return b

	def __lt__(self,other):
		return False

	def grow(self):
		return [self.insert(i) for i in range(9) if self.board[i] == 0]

	def minimax(self):
		val = self.value()
		if val == self.maximizer:
			return 1
		elif -val == self.maximizer:
			return -1
		elif val == 0:
			return 0
		else:
			if self.turn == self.maximizer:
				return max([l.minimax() for l in self.grow()])
			else:
				return min([l.minimax() for l in self.grow()])

	def best_step(self):
		a = [(b.minimax(), b) for b in self.grow()]
		a = sorted(a)
		return a[-1][1]

	def __str__(self):
		res = ''
		for i in range(3):
			for j in range(3):
				idx = (i*3) + j
				if self.board[idx] == 1:
					res += 'X'
				elif self.board[idx] == -1:
					res += 'O'
				else: #0
					res += '_'

				if j == 2:
					res += '\n'
				else:
					res += ' '
		return res

	def value(self):
		#0 : tie
		#1 : x win
		#-1 : o win
		#2 : not done yet
		winner = 2
		#horizontal
		for i in range(3):
			idx = i * 3
			if self.board[idx] == self.board[idx+1] == self.board[idx+2]:
				if winner == 2 and self.board[idx] != 0:
					winner = self.board[idx]

		#vertical
		for j in range(3):
			if self.board[j] == self.board[j+3] == self.board[j+6]:
				if winner == 2 and self.board[j+3] != 0:
					winner = self.board[j+3]

		#diagonal
		if self.board[0] == self.board[4] == self.board[8] or self.board[2] == self.board[4] == self.board[6]:
			if winner == 2 and self.board[4] != 0:
				winner = self.board[4]

		#tie
		if 0 not in self.board:
			if winner == 2:
				winner = 0

		#no one win == 2
		return winner

if __name__ == '__main__':
	player = input('Enter 1 if you want move first (X),\npress other key if you want move second : ')
	ai = -1 if player == '1' else 1
	b = Board(1,ai)
	while b.value() == 2:
		print(b)
		if b.turn == ai:
			b = b.best_step()
		else:
			b = b.insert(int(input('which box do you want to fill?')))
	print(b)
	res = b.value()
	if res == ai:
		print("ai win")
	elif res == -ai:
		print('you win')
	else:
		print('tie')