import math
class Game:
    def __init__(self, teams, players, boards, rounds):

        self.teams = teams # all of them are integers
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
        self.teamPlayed = [[0 for i in range(teams)] for j in range(teams)]
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

        # as well as this, we need to populate the teamPlayed matrix
        # so we will just check the team index of them
        for brd in self.rep:
            for rnd in brd:
                for match in rnd:
                    white, black = match.split("/")
                    wIndex, bIndex = self.GrabIndex(white), self.GrabIndex(black)

                    wTeamIndex, bTeamIndex = wIndex // 6, bIndex // 6 # diving by 6 to make them into team indexes

                    self.played[wIndex][bIndex] += 1
                    self.played[bIndex][wIndex] -= 1

                    self.teamPlayed[wTeamIndex][bTeamIndex] += 1
                    self.teamPlayed[bTeamIndex][wTeamIndex] += 1
                    


        for row in self.played:
            print(row)

    def TeamPlayedQuota(self):
        floorVal = math.floor(self.rounds * self.boards / (self.teams - 1))
        ceilVal = math.ceil(self.rounds * self.boards / (self.teams - 1))

        return (floorVal, ceilVal)

    def checkUpfloats(self):
        upfloatCount = 0
        downfloatCount = 0
        for brdIndex in range(len(self.rep)):
            for rnd in self.rep[brdIndex]:
                for match in rnd:
                    white, black = match.split("/")
                    
                    wNumber, bNumber = int(white[-2:]), int(black[-2:]) # extracting the last 2 digits from the numbers
                    if wNumber - 2 == brdIndex: # commend & explain this later
                        upfloatCount += 1
                    if bNumber - 2 == brdIndex:
                        # upfloats CAN'T be black. Therefore, we can just return false return now
                        return False
                    
                    # now let's handle downfloats

                    if wNumber + 2 == brdIndex or bNumber + 2 == brdIndex:
                        downfloatCount += 1

            if upfloatCount > 1:
                return False
            
            if downfloatCount > 1:
                return False 

        return True



    def CheckValidPlayed(self):
        # note: the notation [0]*len just means an array filled with 0s, len times
        allPlayed = [0]*self.teams # initialises an array filled with the number of times a team has played.
        upfloats = [0]*self.rounds
        
        for brd in self.rep:
            for rnd in brd:
                for match in rnd:
                    white, black = match.split("/")
                    if white[0] == black[0]:
                        return False
                    wIndex, bIndex = self.GrabIndex(white), self.grabIndex(black)
                    wTeamIndex, bTeamIndex = wIndex // 6, bIndex // 6

                    allPlayed[wTeamIndex] += 1
                    allPlayed[bTeamIndex] += 1

                    if self.played[wIndex][bIndex] not in ("0", "1", "-1"):
                        return False
                        
                roundIndex += 1
                    
        # now we have to check if they've hit the quota for team games played.

        quota = self.TeamPlayedQuota()

        for gamesPlayed in allPlayed:
            if gamesPlayed not in quota:
                return False
        
        # now we will check the amounts of upfloats per round.
        # so we have to do something similar, with an array with the length of round called upfloats
        # this will be done in a seperate function - it will return true if all the upfloats/downfloats are valid.

        # the logic for this is in the conditions           

            

                    
        

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