class Game:
    def __init__(self, teams, players, boards, rounds):

        self.teams = teams
        self.players = players
        self.boards = boards
        self.rounds = rounds

        self.rep = [[[] for j in range(rounds)] for i in range(boards)]

        self.valid = True

        # now we are going to create a 2d array of the matches
        # it will be teams*players wide, and teams*players long
        # to index a particular match, we will feed the indexes of the players through.
        # we can use the function GrabIndex to get the index of a particular player

        totalPeople = teams * players
        self.played = [[0 for i in range(totalPeople)] for j in range(totalPeople)]

        # self.played[0][6] gets the status for A.01 playing B.01
        # we can represent the colour of their matches using this system
        # 0 = not played, 1 = played as white, 2 = played as black
        # with the example set out above, if self.played[0][6] == 1, then A.01 (with white) has played B.01 (as black)   

    def GrabIndex(self, playerCode):
        teamCode = ord(playerCode[0]) - ord("A") # e.g. like A and it would be stored as 0 (first index)
        teamIndex = int(playerCode.split(".")[-1]) - 1 # e.g. like 03 and it would be stored as 2 (second index) 

        # now we can use arithmetic to find out the index of the player in a lexiographically sorted array

        index = teamCode * self.teams + teamIndex
        return index

    def GrabCode(self, playerIndex):
        teamCode = playerIndex // self.teams
        teamIndex = playerIndex % self.teams

        return chr(ord("A") + teamCode) + "." + str(teamIndex+1).rjust(2, "0")

    def Populate(self, rep):
        self.rep = rep

    def Display(self):
        for brd in self.rep:
            print(brd)

            # the below code is for displaying all the individual pairs (and their indexes)
            # for rnd in brd:
            #     for match in rnd:
            #         white, black = match.split("/")
            #         print(white, black, self.GrabCode(self.GrabIndex(white)),self.GrabCode(self.GrabIndex(black)))
    
    def PopulatePlayed(self):
        # this goes through every board and populate of who has played who.
        # since there can be upfloats and downfloats, we need to check every single game
        # this is stored in the main "played" array using indexing.
        for brd in self.rep:
            for rnd in brd:
                for match in rnd:
                    white, black = match.split("/")
                    wIndex, bIndex = self.GrabIndex(white), self.GrabIndex(black)

                    if self.played[wIndex][bIndex] == self.played[bIndex][wIndex] == 0:
                        self.played[wIndex][bIndex] += 1
                        self.played[bIndex][wIndex] -= 1
                    else:
                        print("This is an INVALID arrangement.")
                        print("People are playing each other more than once.")
                        self.valid = False

        for row in self.played:
            print(row)

        

game = Game(6, 6, 3, 4)
game.Populate([
    [["D.01/C.01", "A.01/B.01", "F.01/E.01"],
     ["E.01/A.01", "C.01/F.01", "B.01/D.01"],
     ["B.01/E.01", "D.01/F.01", "C.01/A.01"]],
    [["C.02/B.02", "F.02/A.01", "E.02/D.02"],
     ["A.02/E.02", "B.02/D.02", "F.02/C.02"],
     ["A.02/C.02", "E.02/B.02", "D.02/F.02"]],
    [["E.03/A.03", "C.03/F.03", "B.03/D.03"],
     ["F.03/D.03", "B.03/E.03", "A.03/C.03"],
     ["F.03/B.03", "D.03/A.03", "C.03/E.03"]],
    [["D.04/A.04", "F.04/B.04", "C.04/E.04"],
     ["D.04/C.04", "E.04/F.04", "A.04/B.04"],
     ["A.04/F.04", "E.04/D.04", "B.04/C.04"]],
])
game.PopulatePlayed()

# game.Display()