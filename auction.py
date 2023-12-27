# Author:   Evan Samano
# Date:     December 8th, 2022
# Version:  1.0
# Desc:     A playable version of the card game 'Auction,' created by Alex Kutsenok
#           https://www.pagat.com/invented/auction.html


from random import shuffle


money_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]


class Player:
    current_artifact = None

    def __init__(self, _name='DEFAULT NAME'):
        self.name = _name
        self.money = money_list[:] # assign a copy of the list, NOT a reference, to self.money using [:]
        self.artifacts_won = []
        self.score = 0.0
        self.bid = 0
        self.bids = []
    
    def set_name(self, _name):
        self.name = _name[:16] # limit name to 16 characters

    def add_artifact(self, artifact):
        self.artifacts_won.append(artifact)
        self.score += artifact

    def bid_in_auction(self, _bid=None):
        if _bid is None:
            print(f'{self.name} has the following money available: \n', self.money)
            _bid = int(input(f'What is {self.name}\'s bid on {str(Player.current_artifact)}? '))
        self.bid = _bid
        try:
            self.bids.append(_bid)
            self.money.remove(_bid)
        except:
            print('You don\'t have that money. Choose something else.')
            self.bids.remove(_bid) # make sure that incorrect bids don't get added back to player's money later.
            self.bid_in_auction(None) # TODO: might need to remove this line for the networked version

    def get_total_money(self):
        total = 0
        for cash in self.money:
            total += cash
        return total

    def leftovers(self):
        # add leftover money to this player's score to settle ties
        total = self.get_total_money()
        self.score += total/100


def get_artifacts():
    art = [1, 2, 3, 4, 1, 2, 3, 4, 0]
    shuffle(art)
    return art # 1, 2, 3, 4, 0,   ==   J, Q, K, A, Joker


def bid_match(players, match_value):
    # key -> value concept
    for k in players:
        if k.bid == match_value:
            return k


def score_match(players, match_value):
    # key -> value concept
    for k in players:
        if k.score == match_value:
            return k


def tie_helper(things):
    '''
    Returns True if there is a tie present in `things` list.
    Returns the highest number in `things` if there is not a tie in the top two things.
    '''
    things.sort()
    if things[-1] == things[-2]:
        return True
    else:
        return things[-1]


def play(players):
    game_artifacts = get_artifacts()


    def determine_who_tied(remaining_players, sel_players):
        for i, p in enumerate(sel_players, 0):
            if i == len(sel_players) - 1: # if we are at the final player
                first_player = sel_players[0]
                if p.bid > first_player.bid:
                    remaining_players.remove(first_player)
                    return (False, remaining_players[:]) # we return rem_players in order to assign rem_players to sel_players on the outside
            else:
                next_player = sel_players[i + 1]
                if p.bid > next_player.bid:
                    remaining_players.remove(next_player)
                    return (False, remaining_players[:])
        return (True, remaining_players[:]) # if we checked all the players through without removing any, then return True and end recursion :)


    def bidding_round(sel_players): # sel_players -> selected players (the players who will be bidding).
        '''
        Handles players bidding on an artifact.
        Recursively calls itself again if there is a tie in the bidding.
        Returns the auction winner (Player object) when found.
        '''
        # each player bids
        bids = []
        for p in sel_players:
            p.bid_in_auction()
            bids.append(p.bid)

        # determine the winner
        th_result = tie_helper(bids)
        if type(th_result) is int: # there is no tie, and there is a winner
            return bid_match(sel_players, th_result)
        elif type(th_result) is bool: # there is a tie, and we now must determine who is tied to the highest bid
            remaining_players = sel_players[:]
            all_checked = False # have we succesfully checked that all remaining players are tied?
            while not all_checked:
                all_checked, temp_players = determine_who_tied(remaining_players, sel_players)
                sel_players = temp_players
            # do another round of bidding with the remaining players
            return bidding_round(remaining_players)
        else:
            raise TypeError('The wrong type was returned by the tie_helper() function.')


    while len(game_artifacts) != 0:
        print('\n')
        Player.current_artifact = game_artifacts.pop() # this sets the class attribute so all Players know what they are bidding on
        # reset player bids
        for p in players:
            p.bids = []
        auction_winner = bidding_round(players)
        if Player.current_artifact != 0:
            auction_winner.add_artifact(Player.current_artifact)
        else: # if the current_artifact is the joker (0), then
            Player.current_artifact = game_artifacts.pop() # get the next artifact
            print(f'Winning player won {Player.current_artifact}')
            auction_winner.add_artifact(Player.current_artifact)
        # return bids to players that lost the auction
        losers = [p for p in players if p != auction_winner]
        for p in losers:
            for cash in p.bids:
                p.money.append(cash)
            p.money.sort()
    
    # add leftover money to each player's score
    for p in players:
        p.leftovers()

    # get the player object of the player with the highest score (doesn't account for ties currently, but are ties possible?)
    print('\n', 'Determining the winner now...')
    scores = []
    for p in players:
        print(p.name, p.score)
        scores.append(p.score)
    th_result = tie_helper(scores)
    return score_match(players, th_result)


if __name__ == '__main__':
    players = [Player('X'), Player('Gamer'), Player('Evan'), Player('Four'), Player('Five')]
    the_winner_yippee = play(players)
    print(f'The winner of the game is {the_winner_yippee.name}! \nYippee!')