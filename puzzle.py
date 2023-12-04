
NAME_TO_TABLE = {'t': [[1,1,1],[0,1,0]], 
                 'T': [[1,1,1],[0,1,0],[0,1,0]], 
                 'z': [[1,1,0],[0,1,1]],
                 'c': [[1,1],[1,0],[1,1]],
                 'f': [[1,1],[1,0],[1,1], [1,0]],
                 'L': [[1,0,0],[1,1,1]],
                 'l':[[1,0], [1,1]]}
EMPTY_SPOT = '-'
BLOCKER_SPOT = 'o'

def transpose(M):
    return [[ M[col][row] for col in range(len(M))] for row in range(len(M[0]))]

def reverse_row(M):
    return M[::-1]

def reverse_col(M):
    return [M[row][::-1] for row in range(len(M)) ]

def help_message():
    print("- 'help' to display commands")
    print("- 'quit' to quit the game" )
    print("- 'a <piece name> <row> <col>' to add a piece to the board at the position ") 
    print("- 'r <piece name>' to remove a piece")
    
class Shape:
    __slots__ = ['__table', '__position'] 
    
    def __init__(self, table, position = None):
        self.__table = table
        self.__position = position

    def __eq__(self,other):
        return self.__table == other.__table  
    
    def __hash__(self):
        return hash(repr(self.__table))    
    
    def __repr__(self):
        return str(self.__table) + " " + str(self.__position)
    
    def __update_board(self, board, symbol):
        row, col = self.__position
        for i in range(len(self.__table)):
            for j in range(len(self.__table[0])):
                if self.__table[i][j] == 1:
                    board[i+row][j+col] = symbol

    def add(self, board, position, symbol):
        self.__position = position
        self.__update_board(board, symbol)

    def remove(self, board):
        self.__update_board(board,"-")

    def fit(self, board, position):
        row, col = position
        for i in range(len(self.__table)):
            for j in range(len(self.__table[0])):
                if self.__table[i][j] == 1 and board[i + row][j+col] != '-':
                    return False
        return True

    def get_table(self):
        return self.__table      
          
class Piece:
    def __init__(self, name):     
        self.name = name
        self.current_shape = None
        self.shape_table = NAME_TO_TABLE[name]
        self.possible_shapes = [Shape(self.shape_table)]

        l1 = reverse_row(self.shape_table)
        l2 = reverse_col(self.shape_table)
        l3 = transpose(self.shape_table)
        l4 = transpose(l1)
        l5 = reverse_row(l2)
        l6 = reverse_row(l3)
        l7 = transpose(l5)

        a_list = [l1,l2,l3,l4,l5,l6,l7]
        for table in a_list:
            self.possible_shapes.append(Shape(table))
        
        self.fit_shapes = []
        self.n = -1
        self.position = None

    def get_name(self):
        return self.name
    
    def get_current_shape(self):
        return self.current_shape
    
    def set_fit_shapes(self,board,position):
        for shape in self.possible_shapes:
            if shape.fit(board,position):
                self.fit_shapes.append(shape)
   
    def get_fit_shapes(self):
        return self.fit_shapes
    
    def get_fit_shape(self):
        self.n += 1
        if self.n == len(self.fit_shapes):
            self.n = 0
        if self.fit_shapes == []:
            return None
        return self.fit_shapes[self.n]
    
    def add(self,board,shape,c_position):
        self.position = c_position
        self.current_shape = shape
        shape.add(board,c_position,self.name)

    def remove(self,board):
        self.current_shape.remove(board)
        self.current_shape = None

class Puzzle:
    __slots__ = ['__board', '__pieces', '__pieces_on_board', '__game_over']
    
    def __init__(self, blockers):
        self.__board = [[EMPTY_SPOT for _ in range(6)] for _ in range(6)]
        for r, c in blockers:
            self.__board[r][c] = BLOCKER_SPOT
        
        self.__pieces = {}

        for key in NAME_TO_TABLE:
            self.__pieces[key] = Piece(key)
        self.__pieces_on_board = set()
    
        self.__game_over = False

    def game_over_helper(self):
        if self.__pieces_on_board == self.__pieces:
            self.__game_over = True
            return self.__game_over
        else: 
            return False
        
    def addPiece(self,name,position):
        piece = self.__pieces[name] # retrieves the Piece object

        piece.set_fit_shapes(self.__board, position)

        current_shape = piece.get_fit_shape() # get the current shape that fits
        if current_shape is None:
            print("No valid shape at the position")
            return None
        piece.add(self.__board,current_shape,position) # call the add method on piece object using current shape
        print(self)
        ask = input(f"{name}: like this?  (y/n): ")
        
        while ask == "n":
            piece.remove(self.__board)
            current_shape = piece.get_fit_shape() # get the current shape that fits
            piece.add(self.__board,current_shape,position) 
            print(self)
            ask = input(f"{name}: like this?  Y/N: ")
        self.__pieces_on_board.add(piece)

                
    def removePiece(self,name):
        piece = self.__pieces[name]
        if piece in self.__pieces_on_board:
            piece.remove(self.__board)
            self.__pieces_on_board.remove(piece)

    def play(self):
        print(self)
        while True:
            response = input("Enter a command or 'help': ")
            if response == "quit":
                print("Bye!")
                break
            elif response == "help":
                help_message()
            else:
                x = response.split(" ")
                if x[0] == "a":
                    self.addPiece(x[1],( int(x[2]) ,int(x[3]) ))
                if x[0] == "r":
                    self.removePiece(x[1])
                print(self)
    
    def __str__(self):
        s = '    0 1 2 3 4 5\n'
        s +='   ------------\n'
        for index in range(len(self.__board)):
            s += str(index) + " | "
            for elt in self.__board[index]:
                s += elt + " "
            s += "\n"
        return s

def main(): 
    # blocker_locations = ((0,1), (0,5), (2,0), (5,1), (5,4))
    # blocker_locations = ((0,0), (0,1), (3,4), (4,0), (5,5))
    blocker_locations = ((0,1), (0,3), (4,3), (5,3), (5,5)) 
    a_puzzle = Puzzle(blocker_locations)
    a_puzzle.play()

if __name__ == '__main__':     

    BOARD1 = [['o','o','-','-','-','-'],
         ['t','t','t','-','-','-'],
         ['-','t','-','-','-','-'],
         ['-','L','L','z','o','-'],
         ['o','L','z','z','-','-'],
         ['-','L','z','-','-','o']]
    shape = Shape([[0,1], [1,1]])
    fitted = shape.fit(BOARD1, (1,2))
    main()
    # The command work in ‘a/r <name> <row> <col>' style