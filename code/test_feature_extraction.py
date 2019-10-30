# changing our file to two files, one with the decisions of the players ( calls / non-calls )
# and one with the features we want to examine.

import os
Dir = os.path.normpath(r'INSERT_YOUR_PATH_HERE')
os.chdir(Dir)

# assigning values to cards
DOG = 0
JACK = 11
QUEEN = 12
KING = 13
ACE = 14
PHOENIX = 15
DRAGON = 16


# translate_hand function which creates a 17-index array which counts how many cards of a kind a player has in his hand.
def translate_hand(cards):
    current_hand = [0.0 for x in range(17)]
    cards = cards.split()
    for card in cards:
        if card == 'Dr':
            current_hand[DRAGON] = 1
        elif card == 'Ph':
            current_hand[PHOENIX] = 1
        elif card == 'Hu':
            current_hand[DOG] = 1
        elif card == 'Ma':
            current_hand[1] = 1
        elif card == 'GK' or card == 'BK' or card == 'SK' or card == 'RK':
            current_hand[KING] += 0.25
        elif card == 'GD' or card == 'BD' or card == 'SD' or card == 'RD':
            current_hand[QUEEN] += 0.25
        elif card == 'GB' or card == 'BB' or card == 'SB' or card == 'RB':
            current_hand[JACK] += 0.25
        elif card == 'GA' or card == 'BA' or card == 'SA' or card == 'RA':
            current_hand[ACE] += 0.25
        elif card == 'G10' or card == 'B10' or card == 'S10' or card == 'R10':
            current_hand[10] += 0.25
        elif card == 'G9' or card == 'B9' or card =='S9' or card == 'R9':
            current_hand[9] += 0.25
        elif card == 'G8' or card == 'B8' or card == 'S8' or card == 'R8':
            current_hand[8] += 0.25
        elif card == 'G7' or card == 'B7' or card == 'S7' or card == 'R7':
            current_hand[7] += 0.25
        elif card == 'G6' or card == 'B6' or card == 'S6' or card == 'R6':
            current_hand[6] += 0.25
        elif card == 'G5' or card == 'B5' or card == 'S5' or card == 'R5':
            current_hand[5] += 0.25
        elif card == 'G4' or card == 'B4' or card == 'S4' or card == 'R4':
            current_hand[4] += 0.25
        elif card == 'G3' or card == 'B3' or card == 'S3' or card == 'R3':
            current_hand[3] += 0.25
        elif card == 'G2' or card == 'B2' or card == 'S2' or card == 'R2':
            current_hand[2] += 0.25

    # sanity check
    summary = 0
    for x in range(17):
        if x < 2 and current_hand[x] == 1:
            summary = summary+1
        elif x > ACE and current_hand[x] == 1:
            summary = summary+1
        elif current_hand[x] == 0.25:
            summary = summary+1
        elif current_hand[x] == 0.5:
            summary = summary+2
        elif current_hand[x] == 0.75:
            summary = summary+3
        elif current_hand[x] == 1.0 and x>1 and x < PHOENIX:
            summary = summary+4
    if summary != 8:
        # Gr.Tichu database has hands of 8 cards for each player.
        print("Oops!")
        print(summary)
        print(current_hand)

    return list(current_hand)


def find_steps(current_hand):
    # find_steps function which finds how many consecutive pairs a player has in his hand
    steps_in_hand = [0.0 for x in range(14)]
    for i in range(13):
        if current_hand[i+2] > 0.25 and current_hand[i+3] > 0.25:
            steps_in_hand[i+1] = steps_in_hand[i]+1
            # e.g 2 2 3 3 4 4 will give step[3] = 0+1 = 1 and step[4] = 1+1 = 2
            # which means I have 2 consecutive pairs below my 4 4 pair.
    for i in range(14):
        steps_in_hand[i] = round((steps_in_hand[i] / 3), 3)
        # normalize (/6 when I have all 14 cards, but only /3 now since I have 8 cards available).
    steps_in_hand.pop(0)
    return list(steps_in_hand)


def find_full_houses(current_hand):
    full_houses = [0.0 for x in range(15)]
    for i in range(13):
        if current_hand[i+2] > 0.5:
            for j in range(13):
                if not(j == i):
                    if current_hand[j+2] > 0.25:
                        full_houses[i] = 1
                        continue
    return list(full_houses)


def find_straights(current_hand):
    # find_straights function which
    # finds how many straights a player has in his hand
    hand_straights = [0.0 for x in range(11)]
    for ind in range(10):
      if current_hand[ind+1] > 0 and current_hand[ind+2] > 0 and current_hand[ind+3] > 0 and current_hand[ind+4] > 0 and current_hand[ind+5] > 0:
          hand_straights[ind+1] = hand_straights[ind]+1
# 1 means a 5-straight with highest card equaling the value of the index, 2 means a 6-straight with highest
#  card equaling the value of the index, 3 means a 7-straight and so on.
    for i in range(11):
        hand_straights[i] = round((hand_straights[i] / 4), 3)
        # normalize. (/9 when we have 14 cards, but only /4 now since we have 8 cards.)
    hand_straights.pop(0)
    return list(hand_straights)


def find_fourofakind(current_hand):
    # find_fourofakind function which finds number of four of a kind bombs in hand
    hand_bombcount = 0.0
    for i in range(2, 15):
        if current_hand[i] > 0.75:
            hand_bombcount += 1
    hand_bombcount = hand_bombcount / 2
    # normalize (max 3 bombs per hand, but only 2 when calling grand (as we have 8 cards!))
    return hand_bombcount


def find_flushes_and_total_bombcount(cards):
    # find_flushes function which finds number of same-colored straights with the help of
    # find_straights function and then add the total number of bombs in hand as the last element
    current_hand = translate_hand(cards)
    cards = cards.split()
    S = [0.0 for x in range(17)]
    R = [0.0 for x in range(17)]
    G = [0.0 for x in range(17)]
    B = [0.0 for x in range(17)]
    for card in cards:
        if card == 'SK':
            S[KING] += 1
        elif card == 'SD':
            S[QUEEN] += 1
        elif card == 'SB':
            S[JACK] += 1
        elif card == 'SA':
            S[ACE] += 1
        elif card == 'S10':
            S[10] += 1
        elif card == 'S9':
            S[9] += 1
        elif card == 'S8':
            S[8] += 1
        elif card == 'S7':
            S[7] += 1
        elif card == 'S6':
            S[6] += 1
        elif card == 'S5':
            S[5] += 1
        elif card == 'S4':
            S[4] += 1
        elif card == 'S3':
            S[3] += 1
        elif card == 'S2':
            S[2] += 1
        if card == 'RK':
            R[KING] += 1
        elif card == 'RD':
            R[QUEEN] += 1
        elif card == 'RB':
            R[JACK] += 1
        elif card == 'RA':
            R[ACE] += 1
        elif card == 'R10':
            R[10] += 1
        elif card == 'R9':
            R[9] += 1
        elif card == 'R8':
            R[8] += 1
        elif card == 'R7':
            R[7] += 1
        elif card == 'R6':
            R[6] += 1
        elif card == 'R5':
            R[5] += 1
        elif card == 'R4':
            R[4] += 1
        elif card == 'R3':
            R[3] += 1
        elif card == 'R2':
            R[2] += 1
        if card == 'GK':
            G[KING] += 1
        elif card == 'GK':
            G[QUEEN] += 1
        elif card == 'GB':
            G[JACK] += 1
        elif card == 'GA':
            G[ACE] += 1
        elif card == 'G10':
            G[10] += 1
        elif card == 'G9':
            G[9] += 1
        elif card == 'G8':
            G[8] += 1
        elif card == 'G7':
            G[7] += 1
        elif card == 'G6':
            G[6] += 1
        elif card == 'G5':
            G[5] += 1
        elif card == 'G4':
            G[4] += 1
        elif card == 'G3':
            G[3] += 1
        elif card == 'G2':
            G[2] += 1
        if card == 'BK':
            B[KING] += 1
        elif card == 'BD':
            B[QUEEN] += 1
        elif card == 'BB':
            B[JACK] += 1
        elif card == 'BA':
            B[ACE] += 1
        elif card == 'B10':
            B[10] += 1
        elif card == 'B9':
            B[9] += 1
        elif card == 'B8':
            B[8] += 1
        elif card == 'B7':
            B[7] += 1
        elif card == 'B6':
            B[6] += 1
        elif card == 'B5':
            B[5] += 1
        elif card == 'B4':
            B[4] += 1
        elif card == 'B3':
            B[3] += 1
        elif card == 'B2':
            B[2] += 1
    s_flush = find_straights(S)
    g_flush = find_straights(G)
    b_flush = find_straights(B)
    r_flush = find_straights(R)
    total_flush_sum = 0.0
    for i in range(9):
        if s_flush[i+1] > s_flush[i]:
            total_flush_sum = total_flush_sum+1
        if g_flush[i+1] > g_flush[i]:
            total_flush_sum = total_flush_sum+1
        if b_flush[i+1] > b_flush[i]:
            total_flush_sum = total_flush_sum+1
        if r_flush[i+1] > r_flush[i]:
            total_flush_sum = total_flush_sum+1
    flush_list = (s_flush+g_flush+b_flush+r_flush)
    total_bomb_count=[0.0 for x in range(0, 1)]
    total_bomb_count[0] = total_flush_sum + find_fourofakind(hand)
    return flush_list+total_bomb_count


# normalize total bomb count. ( /4 when I got 14 cards,
# but now no need to normalize, since I can't have 2 diff color flushes in 8 cards. ) NEED TO CHECK!
with open('grandTichuTestLogs.inputData') as f:
    with open('SVRTestFeatures.data', 'a+') as fout:
        with open('SVRTestPlayerCalls.data', 'a+') as calls:
            line_count = 0
            for line in f:
                line_count = line_count+1
                parts = line.split(' ', 1)
                if len(parts) < 2:
                    continue
                # splitting input to save the call or no-call value ( 1 or 0 )
                call = parts[0]
                # call = 1 if player called Gr.Tichu or 0 if he didn't
                parts = parts[1].split(' ', 1)
                # splitting the rest of the input to save the player's team score and opponent's team score
                team_score=(parts[0])
                # normalize scores.
                if int(team_score) > 1000:
                    team_score = str(1.0)
                elif int(team_score) < -1000:
                    team_score = str(0.0)
                elif int(team_score) == 0:
                    team_score = str(0.5)
                elif int(team_score) < 0:
                    team_score = str(round((((int(team_score)/1000) +1)/2),3))
                elif int(team_score) > 0:
                    team_score = str(round((((int(team_score)/1000) +1)/2),3))
                parts=parts[1].split(' ', 1)
                opp_score=(parts[0])
                # normalize scores.
                if int(opp_score) > 1000:
                    opp_score = str(1.0)
                elif int(opp_score) < -1000:
                    opp_score = str(0.0)
                elif int(opp_score) == 0:
                    opp_score = str(0.5)
                elif int(opp_score) < 0:
                    opp_score = str(round((((int(opp_score)/1000) + 1)/2), 3))
                elif int(opp_score) > 0:
                    opp_score = str(round((((int(opp_score)/1000) + 1)/2), 3))
                hand = translate_hand(parts[1])
                # translates our cards to create the hand list
                steps = find_steps(hand)
                # finds consecutive pairs in our hand
                straights = find_straights(hand)
                # finds straights in our hand
                f_houses = find_full_houses(hand)
                # finds full houses in our hand
                flushes = find_flushes_and_total_bombcount(parts[1])
                # finds flushes  and total bomb count in our hand
                # creating two files, which will be used to train and test our SVR predictor model.
                features_inplist = hand+steps+straights+f_houses+flushes
                features_inplist.insert(0, opp_score)
                features_inplist.insert(0, team_score)
                # features_inplist.insert(0, call)
                calls_inplist = []
                calls_inplist.insert(0, call)
                fout.write(' '.join(str(v) for v in features_inplist))
                fout.write('\n')
                calls.write(' '.join(str(v) for v in calls_inplist))
                calls.write('\n')
        calls.close()
    fout.close()
f.close()
print("# of features:")
print(len(features_inplist))
print("# of samples:")
print(line_count)
input("Press enter to exit ;)")
