import random

animals = ['dog', 'cat', 'hippo', 'bunny', 'horse', 'hedgehog', 'wombat', 'porcupine', 
           'dog', 'cat', 'hippo', 'bunny', 'horse', 'hedgehog', 'wombat', 'porcupine']
# animals = ['dog', 'cat', 'dog', 'cat']


def print_table(table_to_print):
    rows = int(len(animals) ** 0.5)
    for row in range(rows):
        for cell in range(rows):
            print(table_to_print[rows*row+cell], ' ', end='')
        print()
    return


animals = random.sample(animals, len(animals))
animals_dict = {}
for index, animal in enumerate(animals):
    animals_dict[index] = animal
# print(animals_dict)
table = []
for i in range(len(animals)):
    table.append('-')
print_table(table)
first_guess = True
found = 0
while found < int(len(animals)/2):
    guess = -1
    while guess < 0 or guess > len(table)-1 or table[guess] != '-' or (not first_guess and guess == first):
        guess = int(input('Next turn: '))
    if first_guess:
        first = guess
        first_guessed_animal = animals_dict.get(first)
        temp_table = []
        for i in range(len(table)):
            if i == first:
                temp_table.append(first_guessed_animal)
            else:
                temp_table.append(table[i])
        print_table(temp_table)
        first_guess = False
        continue
    else:
        second = guess
        second_guessed_animal = animals_dict.get(second)
        for i in range(len(temp_table)):
            if i == second:
                temp_table[i] = second_guessed_animal
        print_table(temp_table)
        if first_guessed_animal == second_guessed_animal:
            found += 1
            for i in range(len(temp_table)):
                table[i] = temp_table[i]
            print('Nice guess! ')
            first_guess = True
            continue
        else:
            input('Wrong! Press any key to try again! ')
            print_table(table)
            first_guess = True
            continue
print('You won!')
