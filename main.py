'''
LOTR Risk Simulator CLI
Modified from Vegar Andreas Bergum's Risk Roller
A simple application that eliminates the need for dice in the board-game Risk.
'''

from random import randrange

def main():
    '''Outer loop for the application, calls risk_roller until user exits'''
    while True:
        print('------------------------------------------')
        choice = input('risk-roller-cli (r: roll with steps, s: simulate battle, q: quit): ')
        if choice == 'q':
            exit()
        elif choice == 'r':
            risk_roller()
        elif choice == 's':
            simulate_battle()

def risk_roller():
    '''Main flow of the application with step-by-step rolls'''
    try: 
        attacker = int(input("Attacker's troops: "))
        validate_troop_numbers(True, attacker)
    except ValueError:
        print('Invalid troop input')
        return

    try:
        defender = int(input("Defender's troops: "))
        validate_troop_numbers(False, defender)
    except ValueError:
        print('Invalid troop input')
        return

    while attacker > 1 and defender > 0:
        # Get and sort rolls in descending order
        a_rolls = sorted(get_rolls(get_amount_of_dice(True, attacker)), reverse=True)
        d_rolls = sorted(get_rolls(get_amount_of_dice(False, defender)), reverse=True)

        lost_attackers = 0
        lost_defenders = 0
        
        # Compare dice pairs (they're already sorted)
        for i in range(min(len(a_rolls), len(d_rolls))):
            if d_rolls[i] >= a_rolls[i]:  # Defender wins ties
                lost_attackers += 1
            else:
                lost_defenders += 1

        attacker -= lost_attackers
        defender -= lost_defenders

        print('-----')
        print(f'Attacker rolls: {a_rolls}')
        print(f'Defender rolls: {d_rolls}')
        cont = input(('Attacker lost {0}, {1} remaining\n'
                    + 'Defender lost {2}, {3} remaining\n'
                    + '(q to quit, enter to continue)')
                    .format(lost_attackers, attacker, lost_defenders, defender))
        if cont == 'q':
            return

    print_battle_result(attacker, defender)

def simulate_battle():
    '''Simulates entire battle at once without step-by-step input'''
    try: 
        attacker = int(input("Attacker's troops: "))
        validate_troop_numbers(True, attacker)
    except ValueError:
        print('Invalid troop input')
        return

    try:
        defender = int(input("Defender's troops: "))
        validate_troop_numbers(False, defender)
    except ValueError:
        print('Invalid troop input')
        return
    attacker_extra = int(input("Extra points for attacker: "))
    defender_extra = int(input("Extra points for defender: "))
    threedice = input("will defender roll 3 dice? (Y/N)")
    td = False
    
    if threedice == "Y":
        td = True
    
    elif threedice == "N":
        td = False
        

    initial_attacker = attacker
    initial_defender = defender
    rounds = 0

    print('\nBattle simulation starting...')
    print(f'Initial forces - Attacker: {attacker}, Defender: {defender}\n')

    while attacker > 1 and defender > 0:
        a_rolls = sorted(get_rolls(get_amount_of_dice(True, False, attacker)), reverse=True)
        d_rolls = sorted(get_rolls(get_amount_of_dice(False, td, defender)), reverse=True)
        a_rolls[0] += attacker_extra
        d_rolls[0] += defender_extra

        lost_attackers = 0
        lost_defenders = 0
        
        for i in range(min(len(a_rolls), len(d_rolls))):
            if d_rolls[i] >= a_rolls[i]:
                lost_attackers += 1
            else:
                lost_defenders += 1

        attacker -= lost_attackers
        defender -= lost_defenders
        rounds += 1

        print(f'Round {rounds}:')
        print(f'Attacker rolls: {a_rolls}')
        print(f'Defender rolls: {d_rolls}')
        print(f'Casualties - Attacker: {lost_attackers}, Defender: {lost_defenders}')
        print(f'Remaining forces - Attacker: {attacker}, Defender: {defender}\n')

    print(f'Battle finished in {rounds} rounds!')
    print(f'Initial forces - Attacker: {initial_attacker}, Defender: {initial_defender}')
    print_battle_result(attacker, defender)

def get_amount_of_dice(attacker, td, troops):
    '''Returns the amount of dice the player can use'''
    if attacker:
        if troops <= 1:  # Can't attack with 1 troop
            return 0
        return min(3, troops - 1)  # Max 3 dice, must leave 1 troop behind
    else:
        if td:
            return min(3,troops)
        else: 
            return min(2, troops)  # Defender gets up to 2 dice

def get_rolls(amount):
    '''Returns a list of dice-rolls'''
    return [randrange(1, 7) for _ in range(amount)]  # Fix: dice are 1-6, not 0-5

def validate_troop_numbers(attacker, amount):
    '''Validates the number of troops'''
    if amount <= 0:
        raise ValueError
    if attacker and amount < 2:
        raise ValueError

def print_battle_result(attacker, defender):
    '''Prints the final result of the battle'''
    if defender < 1:
        print('Attacker won, and has {0} troops left'.format(attacker))
    else:
        print('Defender won, and has {0} remaining. Attacker has {1} remaining'
              .format(defender, attacker))

if __name__ == "__main__":
    main()
