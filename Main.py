#imports:
import random, sys

#current video progress: 
#variables
max_lines = 3
max_bet = 1000
min_bet = 1

#reel lines for slot machine. 
rows = 3 #rows
cols = 3 #columns

#symbol counts
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

#Multiplier
symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

#functions
# Checks for winnings based on the spun columns, number of lines, bet, and values of symbols.
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_line = []
    for line in range(lines):
        symbol = columns[0][line]
        symbol_check = True
        for column in columns:
            if symbol != column[line]:
                symbol_check = False
                break
        
        if symbol_check:
            winnings += values[symbol] * bet
            winning_line.append(line + 1)
    
    winnings = round(winnings,2)
    return winnings, winning_line

#sets up the reel rows for the machine
def spin_reel_get(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows): #rows would be matching that of variable above, and also for columns 
            value = random.choice(all_symbols)
            current_symbols.remove(value) #ensures we don't pick that value again
            column.append(value)
        
        columns.append(column) #adds itself to the column list
    return columns

#sets up the columns
def print_slots(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="\n")

#Sets up the deposits
def deposit():
    while True:
        amount = input("Input how much you want to deposit?\n")
        if amount.isdigit(): #Checks if this is valid input
            amount = float(amount)
            if amount > 0.00:
                break
            else:
                print("The amount must be greater than 0")
        else:
            print("Number input only. No other input allowed.")
    return float(amount)

#sets up the lines (for betting on rows)
def lines_get(current_balance):
    while True:
        num_lines = input(f"How many lines do you want to bet on? Must be at least 1 and no more than {max_lines}\n")
        if num_lines.isdigit():
            num_lines = int(num_lines)
            if num_lines <= max_lines and num_lines > 0:
                print(f"You are betting ${current_balance} on {num_lines} lines")
                break
            else:
                print(f"You must not go below 0 nor exceed maximum number of {max_lines}")
        else:
            print("Number input only. No other input allowed")
    return num_lines
            
#Sets up the bets
def get_bet():
    while True:
        amount = input("Input how much you want to bet on each line?\n")
        if amount.isdigit():
            amount = float(amount)
            if min_bet <= amount <= max_bet:
                break
            else:
                print(f"The amount must between ${min_bet} - ${max_bet}")
        else:
            print("Number input only. No other input allowed.")
    return amount

#Spins the slot machine so long as you have enough balance left.
def spin(balance):
    line = lines_get(balance)
    while True:
        bet = get_bet()
        total_bet = bet * line
        #checking to see if total bet is within balance.
        if total_bet > balance:
            print(f"You do not have enough to bet that amount to bet per lines. Your current balance is ${balance}")
            if balance == 0: #forcibly quits when your balance is 0.
                print("Your deposit is now empty. Exiting.")
                sys.exit()
        else:
            break
    remain_balance = round(balance - total_bet, 2)
    print(f"You are betting {bet} on {line} lines. Total bet is equal to: ${total_bet}.")

    slots = spin_reel_get(rows, cols, symbol_count)
    print_slots(slots)
    winnings, winning_line = check_winnings(slots, line, bet, symbol_value)
    if winnings > 0:
        print(f"You won ${winnings}, increasing your overall deposit amount total: ${winnings + remain_balance}")
        print(f"you won on lines", *winning_line)
    else:
        print(f"You have not won anything. Your remaining deposit amount is: ${remain_balance}")
    #return the net amount won or lost in this spin
    return total_bet, winnings

def update_balance(balance, total_bet, winnings):
    return balance - total_bet + winnings

def main():
    balance = deposit()
    while True:
        print(f"current balance is: ${balance}")
        play = input("Press enter to play. (q to quit).\n")
        if play.lower().strip() == "q":
            break
        total_bet, winnings = spin(balance)
        balance = update_balance(balance, total_bet, winnings)

    print(f"You're left with {balance}")
    
main()