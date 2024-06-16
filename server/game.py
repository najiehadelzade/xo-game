import json
class Game:

    def __init__(self, game_id, player1, player2):
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        player1.ready = False
        player2.ready = False
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.turn = 1
        self.winner = 0

    def play(self):
        state_game={'board':self.board ,'your_turn':self.turn==1, 'result':0}
        data=json.dumps(state_game).encode()
        self.player1.connection.sendall(data)
        
    
        state_game={'board':self.board ,'your_turn':self.turn==2, 'result':0}
        data=json.dumps(state_game).encode()
        self.player2.connection.sendall(data)
        
        for i in range(9):
            if self.turn== 1:
                data=self.player1.connection.recv(1024).decode()
            else:
                data=self.player2.connection.recv(1024).decode()
            dic=json.loads(data)
            row=dic['row']
            col=dic['col']
            self.board[row][col]=self.turn
            result= self.has_won(self.turn)
            state_game={'board':self.board ,'your_turn':self.turn!=1}
            if result==True and self.turn==1:
                state_game['result']=1
                self.winner = 1
            elif result==True and self.turn==2:
                state_game['result']=2
                self.winner = 2
            elif result==False and i == 8:
                state_game['result']=3
                self.winner = 3
            elif result==False:
                state_game['result']=0 
            
            data=json.dumps(state_game).encode()
            self.player1.connection.sendall(data)
            state_game={'board':self.board ,'your_turn':self.turn!=2}
            if result==True and self.turn==1:
                state_game['result']=2
            elif result==True and self.turn==2:
                state_game['result']=1
            elif result==False and i == 8:
                state_game['result']=3
            elif result==False:
                state_game['result']=0
            
            data=json.dumps(state_game).encode()
            self.player2.connection.sendall(data)
            if result==True:
                break
            self.turn = self.turn % 2 + 1



    def __str__(self):
        return f"Game({self.game_id}, {self.player1}, {self.player2})"

    def __repr__(self):
        return f"Game({self.game_id}, {self.player1}, {self.player2})"
    
    def has_won(self, symbol):
        def is_all_symbol(LIST,symbol):
            for i in LIST:
                if i !=symbol:
                    return False
                
            return True


        for i in self.board:
            win=is_all_symbol(i,symbol)
            if win==True:
                return True

        Ls_col=[]
        for i in self.board:
            Ls_col.append(i[0])
        win1=is_all_symbol(Ls_col,symbol)
        if win1==True:
            return True

        if self.board[0][0]==symbol and self.board[0][0]==self.board[1][1] and self.board[0][0]==self.board[2][2]:
            return True
        
        if self.board[0][2]==symbol and self.board[0][2]==self.board[1][1] and self.board[0][2]==self.board[2][0]:
            return True 
        

        Ls_col=[]
        for i in self.board:
            Ls_col.append(i[1])
        win1=is_all_symbol(Ls_col,symbol)
        if win1==True:
            return True

        Ls_col=[]
        for i in self.board:
            Ls_col.append(i[2])
        win1=is_all_symbol(Ls_col,symbol)
        if win1==True:
            return True
        return False
