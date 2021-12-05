###########################################
###################DAY 1###################
###########################################

def sonar_sweep(k):

    with open('input-day01.txt', 'r') as f:

        lines = f.readlines()

        values = [int(line) for line in lines]

    d_sums = [sum(values[i: i + k])
                for i in range(0, len(values))
                    if len(values[i: i + k]) > 2] if k == 3 else values

    return sum([1
                for i in range(0, len(d_sums))
                    if len(d_sums[i: i + 2]) > 1
                    if (lambda l: l[0] < l[1])
                        (d_sums[i: i + 2])])

###########################################
###################DAY 2###################
###########################################

def dive(part):

    with open('input-day02.txt', 'r') as f:

        lines = f.readlines()

        commands = list(map(lambda l: (l[0], int(l[1])),
                            [line.split() for line in lines]))

    horizontal = 0
    depth = 0

    if part == 1:
        for (cmd, value) in commands:
            if cmd == 'forward':
                horizontal += value
            elif cmd == 'down':
                depth += value
            else:
                depth -= value
    else:
        aim = 0

        for (cmd, value) in commands:
            if cmd == 'forward':
                horizontal += value
                depth += aim * value
            elif cmd == 'down':
                aim += value
            elif cmd == 'up':
                aim -= value

    return horizontal * depth

###########################################
###################DAY 3###################
###########################################

def binary_diagnostic(part):

    with open('input-day03.txt', 'r') as f:

        bins = list(map(str.strip, f.readlines()))

    if part == 1:

        counters = [0] * len(bins[0])

        for bin in (bins):
            for i, bit in enumerate(bin):
                counters[i] += int(bit)

        gamma, epsilon = '', ''

        for counter in counters:

            if counter > len(bins) - counter:
                gamma += '1'
                epsilon += '0'

            else:
                gamma += '0'
                epsilon += '1'

        return int(gamma, 2) * int(epsilon, 2)

    else:

        def get_common(frequency, bins):

            common = 0

            for bin in bins:
                common += int(bin[0])

            if frequency == 'most':
                return '1' if common >= len(bins) - common else '0'

            return '0' if common >= len(bins) - common else '1'

        def bit_criteria(rating, current, bins):
            if len(bins) == 1:
                return current + bins[0]

            if rating == 'ogr':
                common = get_common('most', bins)
                current += common

            else:
                common = get_common('least', bins)
                current += common

            return bit_criteria(rating, current, [bin[1:] for bin in bins if bin[0] == common])

        return int(bit_criteria('ogr', '', bins), 2) * int(bit_criteria('co2', '', bins), 2)

###########################################
###################DAY 4###################
###########################################

class Board():

    def __init__(self, rows):
        self.rows = [[{number: number, 'drawn': False} for number in row] for row in rows]
        self.has_won = False

    def mark_number(self, drawn_number):

        def sweep(i, j):
            
            won_by_row = True
            won_by_column = True

            # Check by row
            for k, row in enumerate(self.rows):
                if k != i:
                    continue # Not interested in other rows
                for l, _ in enumerate(row):
                    number = self.rows[k][l]
                    won_by_row = won_by_row and number.get('drawn')
                    if not won_by_row:
                        break # no need to continue, need to check by column
                else:
                    continue
                break

            if not won_by_row:
                # Check by column
                for l, number in enumerate(self.rows[0]):
                    if l != j:
                        continue # not interested in other columns
                    for k, row in enumerate(self.rows):
                        number = self.rows[k][l]
                        won_by_column = won_by_column and number.get('drawn')
                        if not won_by_column:
                            return False

            return True

        for row in self.rows:
            for number in row:
                if number.get(drawn_number) == 0 and drawn_number == 0:
                    number['drawn'] = True
                if number.get(drawn_number):
                    number['drawn'] = True

        # Check if the board won with the latest drawn number
        for i, row in enumerate(self.rows):
            for j, number in enumerate(row):
                if i != j: # I just need to check diagonals
                    continue

                self.has_won = sweep(i, j)

                if self.has_won:
                    break # no need to continue

            else:
                continue
            break

    def score(self, last_drawn_number):
        unmarked = 0
        for row in self.rows:
            for number in row:
                for value in number:
                    if type(value) is int:
                        if not number['drawn']:
                            unmarked += value

        return unmarked * last_drawn_number

    def __repr__(self):
        # Needs improvement tbh.
        print('Board: ')
        for row in self.rows:
            print(row)
        return ''

def process_input(lines):

    drawn, boards = [], []

    counter = 0
    aux_board = []
    in_board = False

    for i, line in enumerate(lines):
        if i == 0:
            drawn = list(map(int, line.split(','))) # numbers drawn
        else:
            if not line: # starts new board
                in_board = True
                continue
            if in_board:
                aux_board.append(map(int, line.split()))
                counter += 1

                if counter == 5:
                    boards.append(Board(aux_board))
                    counter = 0
                    in_board = False
                    aux_board = []

    return (drawn, boards)

def play(drawn, boards, part):

    if part == 1:
        winner = None
        last_drawn_number = None
        for i, number in enumerate(drawn):
            for j, board in enumerate(boards):
                board.mark_number(number)
                if board.has_won:
                    print('Winner winner chicken dinner.')
                    print('Board number %d has won with number %d after %d drawns.' % (j + 1, number, i))
                    print(board)
                    winner = board
                    last_drawn_number = number
                    break
            else:
                continue
            break


        ## calculate score
        return winner.score(last_drawn_number)
    else:

        logs = [{'board_num': i,
                'won_in_iteration': None,
                'number_drawn': None } for i in range(0, len(boards))]

        for i, number in enumerate(drawn):
            for j, board in enumerate(boards):
                if board.has_won:
                    continue # it already won
                board.mark_number(number)
                if board.has_won: # won after last number
                    print('Winner winner chicken dinner.')
                    print('Board number %d has won with number %d after %d drawns.' % (j + 1, number, i))
                    print(board)

                    logs[j]['won_in_iteration'] = i
                    logs[j]['number_drawn'] = number

        last = None
        iteration = 0
        for log in logs:
            if log.get('won_in_iteration') > iteration:
                iteration = log.get('won_in_iteration')
                last = log

        return boards[last.get('board_num')].score(last.get('number_drawn'))

def giant_squid(part):

    with open('input-day04-1.txt', 'r') as f:
    # with open('input-day04-1.txt', 'r') as f:
        lines = list(map(str.strip, f.readlines()))

    drawn, boards = process_input(lines)

    return play(drawn, boards, part)

def main():

    ###########################################
    ###################DAY 1###################
    ###########################################

    # print(sonar_sweep(1))
    # print(sonar_sweep(3))

    ###########################################
    ###################DAY 2###################
    ###########################################

    # print(dive(1))
    # print(dive(2))

    ###########################################
    ###################DAY 3###################
    ###########################################

    # print(binary_diagnostic(1))
    # print(binary_diagnostic(2))

    ###########################################
    ###################DAY 4###################
    ###########################################

    print(giant_squid(1))
    print(giant_squid(2))

if __name__ == '__main__':
    main()
