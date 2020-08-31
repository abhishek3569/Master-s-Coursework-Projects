__author__ = 'fyt'

import socket
import random
import ClientBase
import collections

# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'Abhi and Jay'
CURRENT_HAND = []
hand=[]
cards = ""
card_list = []
suits = []
numbers = []
rank=""
Hands={1:"Straight Flush",2:"Four of a Kind",3:"Full House",4:"Flush",5:"Straight",6:"Three of a Kind",7: "Two Pair",8: "One Pair",9: "High Cards",0: "No Hand"}

class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0

'''
* Gets the name of the player.
* @return  The name of the player as a single word without space. <code>null</code> is not a valid answer.
'''
def queryPlayerName(_name):
    if _name is None:
        _name = POKER_CLIENT_NAME
    return _name

'''
* Modify queryOpenAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what open
* action to choose.
* @param minimumPotAfterOpen   the total minimum amount of chips to put into the pot if the answer action is
*                              {@link BettingAnswer#ACTION_OPEN}.
* @param playersCurrentBet     the amount of chips the player has already put into the pot (dure to the forced bet).
* @param playersRemainingChips the number of chips the player has not yet put into the pot.
* @return                      An answer to the open query. The answer action must be one of
*                              {@link BettingAnswer#ACTION_OPEN}, {@link BettingAnswer#ACTION_ALLIN} or
*                              {@link BettingAnswer#ACTION_CHECK }. If the action is open, the answers
*                              amount of chips in the anser must be between <code>minimumPotAfterOpen</code>
*                              and the players total amount of chips (the amount of chips alrady put into
*                              pot plus the remaining amount of chips).
'''
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose an opening action.")

    # Random Open Action
    def chooseOpenOrCheck():

        if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
            #return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
            return ClientBase.BettingAnswer.ACTION_OPEN,  (random.randint(0, 10)+ _minimumPotAfterOpen) if _playersCurrentBet + _playersRemainingChips + random.randint(0, 10)> _minimumPotAfterOpen else _minimumPotAfterOpen
        else:
            return ClientBase.BettingAnswer.ACTION_CHECK

    handstrength(hand)
    if (rank==Hands[1] or rank==Hands[2]):

        return {
            0: ClientBase.BettingAnswer.ACTION_CHECK,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
        }.get(1, chooseOpenOrCheck())
    else:
        return {
            0: ClientBase.BettingAnswer.ACTION_CHECK,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
        }.get(random.randint(0,1), chooseOpenOrCheck())


'''
* Modify queryCallRaiseAction() and add your strategy here
* Called during the betting phases of the game when the player needs to decide what call/raise
* action to choose.
* @param maximumBet                the maximum number of chips one player has already put into the pot.
* @param minimumAmountToRaiseTo    the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.
* @param playersCurrentBet         the number of chips the player has already put into the pot.
* @param playersRemainingChips     the number of chips the player has not yet put into the pot.
* @return                          An answer to the call or raise query. The answer action must be one of
*                                  {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
*                                  {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN }.
*                                  If the players number of remaining chips is less than the maximum bet and
*                                  the players current bet, the call action is not available. If the players
*                                  number of remaining chips plus the players current bet is less than the minimum
*                                  amount of chips to raise to, the raise action is not available. If the action
*                                  is raise, the answers amount of chips is the total amount of chips the player
*                                  puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
*                                  <code>playersCurrentBet+playersRemainingChips</code>.
'''
def queryCallRaiseAction(_maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
    print("Player requested to choose a call/raise action.")
    # Random Open Action
    def chooseRaiseOrFold():
        if  _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
            return ClientBase.BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet+ _playersRemainingChips + random.randint(0, 10) > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
        else:
            return ClientBase.BettingAnswer.ACTION_FOLD

    handstrength(hand)

    if (rank == Hands[1] or rank == Hands[2] or rank== Hands[3]):
        return {
            0: ClientBase.BettingAnswer.ACTION_FOLD,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
            2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
        }.get(random.randint(1,2), chooseRaiseOrFold())

    else:
        return {
            0: ClientBase.BettingAnswer.ACTION_FOLD,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
            2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
        }.get(random.randint(0,2), chooseRaiseOrFold())


'''
* Modify queryCardsToThrow() and add your strategy to throw cards
* Called during the draw phase of the game when the player is offered to throw away some
* (possibly all) of the cards on hand in exchange for new.
* @return  An array of the cards on hand that should be thrown away in exchange for new,
*          or <code>null</code> or an empty array to keep all cards.
* @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
'''
def queryCardsToThrow(_hand):
    print("Requested information about what cards to throw")
    print(_hand)

    handstrength(hand)
    if (rank==Hands[1] or rank==Hands[3] or rank==Hands[4] or rank==Hands[5]):
        return 0




# InfoFunction:

'''
* Called when a new round begins.
* @param round the round number (increased for each new round).
'''
def infoNewRound(_round):
    #_nrTimeRaised = 0
    print('Starting Round: ' + _round )

'''
* Called when the poker server informs that the game is completed.
'''
def infoGameOver():
    print('The game is over.')

'''
* Called when the server informs the players how many chips a player has.
* @param playerName    the name of a player.
* @param chips         the amount of chips the player has.
'''
def infoPlayerChips(_playerName, _chips):
    print('The player ' + _playerName + ' has ' + _chips + 'chips')

'''
* Called when the ante has changed.
* @param ante  the new value of the ante.
'''
def infoAnteChanged(_ante):
    print('The ante is: ' + _ante)

'''
* Called when a player had to do a forced bet (putting the ante in the pot).
* @param playerName    the name of the player forced to do the bet.
* @param forcedBet     the number of chips forced to bet.
'''
def infoForcedBet(_playerName, _forcedBet):
    print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")


'''
* Called when a player opens a betting round.
* @param playerName        the name of the player that opens.
* @param openBet           the amount of chips the player has put into the pot.
'''
def infoPlayerOpen(_playerName, _openBet):
    print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

'''
* Called when a player checks.
* @param playerName        the name of the player that checks.
'''
def infoPlayerCheck(_playerName):
    print("Player "+ _playerName +" checked.")

'''
* Called when a player raises.
* @param playerName        the name of the player that raises.
* @param amountRaisedTo    the amount of chips the player raised to.
'''
def infoPlayerRise(_playerName, _amountRaisedTo):
    print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

'''
* Called when a player calls.
* @param playerName        the name of the player that calls.
'''
def infoPlayerCall(_playerName):
    print("Player "+_playerName +" called.")

'''
* Called when a player folds.
* @param playerName        the name of the player that folds.
'''
def infoPlayerFold(_playerName):
    print("Player "+ _playerName +" folded.")

'''
* Called when a player goes all-in.
* @param playerName        the name of the player that goes all-in.
* @param allInChipCount    the amount of chips the player has in the pot and goes all-in with.
'''
def infoPlayerAllIn(_playerName, _allInChipCount):
    print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

'''
* Called when a player has exchanged (thrown away and drawn new) cards.
* @param playerName        the name of the player that has exchanged cards.
* @param cardCount         the number of cards exchanged.
'''
def infoPlayerDraw(_playerName, _cardCount):
    print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

'''
* Called during the showdown when a player shows his hand.
* @param playerName        the name of the player whose hand is shown.
* @param hand              the players hand.
'''
def infoPlayerHand(_playerName, _hand):
    global hand
    if _playerName==POKER_CLIENT_NAME:
        hand=_hand
    print("Player "+ _playerName +" hand " + str(_hand))

def handstrength(hand):
    print(hand)
    cards= ''.join(hand)
    card_list = list(cards)
    #print(card_list)
    suits = card_list[1::2]
    numbers = card_list[0::2]
    #print(numbers)
    for i, num in enumerate(numbers):
        if num == "A":
            numbers[i] = 14
        elif num == "K":
            numbers[i] = 13
        elif num == "Q":
            numbers[i] = 12
        elif num == "J":
            numbers[i] = 11
        elif num == "T":
            numbers[i] = 10
    print(numbers)
    number_dict = collections.defaultdict(int)
    suit_dict = collections.defaultdict(int)
    for i in numbers:
        number_dict[i] += 1
    for j in suits:
        suit_dict[j] += 1
    print(max(numbers))
    print(min(numbers))

    # 4-of-a-kind
    if len(number_dict) == 2:
        if 4 in number_dict.values():
            rank = Hands[1]
            return rank
            print(rank)
        # Full house

    elif len(number_dict) == 2:
        if 3 in number_dict.values():
            for my_card in numbers:
                if my_card == "K":
                    count = count + 1
            if count == 2:
                rank = Hands[3]
                return rank
                print(rank)

        # flush

    elif len(suit_dict) == 1:
        if 5 in suit_dict.values():
            rank = Hands[4]
            return rank
            print(rank)

        # straight

    elif len(number_dict) == 5:

        max_val = (max([numbers.index(x) for x in number_dict.keys()]))
        min_val = (min([numbers.index(x) for x in number_dict.keys()]))
        # print(max_val,min_val)
        if int(max_val) - int(min_val) == 4:
            rank = Hands[5]
            return rank
            print(rank)


        # 3-of-a-kind
    elif len(number_dict) == 3:
        if 3 in number_dict.values():
            rank = Hands[6]
            return rank
            print(rank)

            # 2 Pair
    elif len(number_dict) == 3:
        if 2 in number_dict.values():
            rank = Hands[7]
            return rank
            print(rank)

            # 1 Pair
    elif len(number_dict) == 2:
        rank = Hands[8]
        return rank
        print(rank)
    elif len(number_dict)==5:
        for my_card in numbers:
            if my_card =="K" or my_card=="A":
                rank=Hands[9]
                return rank
                print(rank)






'''
* Called during the showdown when a players undisputed win is reported.
* @param playerName    the name of the player whose undisputed win is anounced.
* @param winAmount     the amount of chips the player won.
'''

def infoRoundUndisputedWin(_playerName, _winAmount):
    print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

'''
* Called during the showdown when a players win is reported. If a player does not win anything,
* this method is not called.
* @param playerName    the name of the player whose win is anounced.
* @param winAmount     the amount of chips the player won.
'''
def infoRoundResult(_playerName, _winAmount):
    print("Player "+ _playerName +" won " + _winAmount + " chips.")

