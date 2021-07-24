import numpy as np

class InvalidBoxException(Exception):
	pass

class Board:
	def __init__(self,turn,ai):
		self.board = [0 for i in range(9)]
		self.turn = turn
		self.maximizer = ai

	def insert(self,i):
		if i < 0 or i > 8:
			raise InvalidBoxException()

		if self.board[i] != 0:
			raise InvalidBoxException()
			
		b = Board(-1 * self.turn,self.maximizer)
		b.board = self.board[:]
		b.board[i] = self.turn
		return b

	def __lt__(self,other):
		return False

	def grow(self):
		return [self.insert(i) for i in range(9) if self.board[i] == 0]

	def minimax(self,alpha=-np.inf,beta=np.inf):
		val = self.value()
		if val == self.maximizer:
			return 1
		elif -val == self.maximizer:
			return -1
		elif val == 0:
			return 0
		else:
			if self.turn == self.maximizer:
				grow = self.grow()
				max_eval = -np.inf
				for l in grow:
					evaluate = l.minimax(alpha,beta)
					max_eval = max(max_eval,evaluate)
					alpha = max(alpha,evaluate)
					if beta <= alpha:
						break
				return max_eval

			else:
				grow = self.grow()
				min_eval = np.inf
				for l in grow:
					evaluate = l.minimax(alpha,beta)
					min_eval = min(min_eval,evaluate)
					beta = min(beta,evaluate)
					if beta <= alpha:
						break
				return min_eval

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
					res += str(i*3 + j)

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
			try:
				x = b.insert(int(input('which box do you want to fill?')))
				b = x
			except:
				print("Choose the valid box!")
	print(b)
	res = b.value()
	if res == ai:
		print("ai win")
	elif res == -ai:
		print('you win')
	else:
		print('tie')