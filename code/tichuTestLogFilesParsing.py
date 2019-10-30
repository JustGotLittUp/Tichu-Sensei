import os
logsDir = os.path.normpath(r'INSERT_YOUR_PATH_HERE')
os.chdir(logsDir)


def player_decisions_for_this_hand(start_line, team_one_current_score, team_two_current_score):

    player_hand_result_line = start_line.split()
    player = player_hand_result_line.pop(0)
    player_hand_result_line.insert(0, '0')
    player_hand_result_line.insert(1, team_one_current_score)
    player_hand_result_line.insert(2, team_two_current_score)

    return player,player_hand_result_line


def skip_six_lines(logfile):

    for _ in range(6):
        curr_line = logfile.readline()

    return curr_line


for log in os.listdir(logsDir):
    # Read the first line
    print(log)
    with open(log) as lg:
        currentLine = lg.readline()
        previousLine = ''
        grandTichuStartString = '---------------Gr.Tichukarten------------------'
        grandTichuEndString = 'Schupfen:'
        scoreString = 'Ergebnis:'
        with open('grandTichuTestLogs.inputData', 'a+') as gtLogs:
            while currentLine:
                if grandTichuStartString not in currentLine:
                    previousLine = currentLine
                    currentLine = lg.readline()
                    continue
                else:
                    lastScoreUpdate = previousLine.split()
                    if scoreString in previousLine:
                        teamOneCurrentScore = lastScoreUpdate.pop(1)
                        teamTwoCurrentScore = lastScoreUpdate.pop(2)
                    else:
                        teamOneCurrentScore = '0'
                        teamTwoCurrentScore = '0'
                    previousLine = currentLine
                    playerOne, lineInputPlayerOne = player_decisions_for_this_hand(lg.readline(), teamOneCurrentScore,
                                                                                   teamTwoCurrentScore)
                    playerTwo, lineInputPlayerTwo = player_decisions_for_this_hand(lg.readline(), teamTwoCurrentScore,
                                                                                   teamOneCurrentScore)
                    playerThree, lineInputPlayerThree = player_decisions_for_this_hand(
                        lg.readline(), teamOneCurrentScore, teamTwoCurrentScore)
                    playerFour, lineInputPlayerFour = player_decisions_for_this_hand(
                        lg.readline(), teamTwoCurrentScore, teamOneCurrentScore)
                    currentLine = skip_six_lines(lg)
                    while grandTichuEndString not in currentLine:
                        if playerOne in currentLine:
                            lineInputPlayerOne[0] = '1'
                        elif playerTwo in currentLine:
                            lineInputPlayerTwo[0] = '1'
                        elif playerThree in currentLine:
                            lineInputPlayerThree[0] = '1'
                        elif playerFour in currentLine:
                            lineInputPlayerFour[0] = '1'
                        currentLine = lg.readline()
                        if lineInputPlayerThree[0] is '0':
                            gtLogs.write(' '.join(lineInputPlayerOne))
                            gtLogs.write('\n')
                        if lineInputPlayerFour[0] is '0':
                            gtLogs.write(' '.join(lineInputPlayerTwo))
                            gtLogs.write('\n')
                        if lineInputPlayerOne[0] is '0':
                            gtLogs.write(' '.join(lineInputPlayerThree))
                            gtLogs.write('\n')
                        if lineInputPlayerTwo[0] is '0':
                            gtLogs.write(' '.join(lineInputPlayerFour))
                            gtLogs.write('\n')
            gtLogs.close()
    lg.close()
