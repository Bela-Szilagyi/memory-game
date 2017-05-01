import random
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


def init(level):
    global animals
    ''' animals = ['dog1', 'cat1', 'hippo1', 'bunny1', 'horse1', 'hedgehog1', 'wombat1', 'porcupine1',
                   'dog2', 'cat2', 'hippo2', 'bunny2', 'horse2', 'hedgehog2', 'wombat2', 'porcupine2']'''
    # animals_init = ['dog', 'cat', 'hippo', 'bunny', 'horse', 'hedgehog', 'wombat', 'porcupine']
    animals_init_18 = ['dog', 'cat', 'hippo', 'bunny', 'horse', 'hedgehog', 'wombat', 'porcupine',
                       'polar bear', 'black bear', 'mouse', 'dolphin', 'chipmunk', 'penguin', 'orangutan',
                       'kangaroo', 'elephant', 'chimp']
    # animals_init_18_sample = random.sample(animals_init_18, 8)
    global size
    if level == 'hard':
        size = 80
        animals_init_18_sample = random.sample(animals_init_18, len(animals_init_18))
    elif level == 'easy':
        size = 120
        animals_init_18_sample = random.sample(animals_init_18, 8)
    animals = []
    # for animal in animals_init:
    for animal in animals_init_18_sample:
        animals.append(animal + '1')
        animals.append(animal + '2')
    print(animals)
    # animals = ['dog', 'cat', 'dog', 'cat']
    animals = random.sample(animals, len(animals))
    global animals_dict
    animals_dict = {}
    for index, animal in enumerate(animals):
        animals_dict[index] = animal
    print(animals_dict)
    global table
    table = []
    for i in range(len(animals)):
        table.append('00')
    global rows
    rows = int(len(animals) ** 0.5)
    global first_guess
    first_guess = True
    global found
    found = 0
    print_table(table)
    return


def print_table(table_to_print):
    global animals
    rows = int(len(animals) ** 0.5)
    for row in range(rows):
        for cell in range(rows):
            print(table_to_print[rows*row+cell], ' ', end='')
        print()
    return


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        return None
    else:
        return render_template('index.html')


@app.route('/level', methods=['GET', 'POST'])
def game():
    global level
    print(request.form['level'])
    if request.form['level'] == 'easy':
        level = "easy"
    elif request.form['level'] == 'hard':
        level = 'hard'
    init(level)
    return render_template('table.html', size=size, table=table, rows=rows, found=found, message='Make your first guess!')


@app.route('/click/<id>')
def click(id):
    global first_guess
    global found
    global temp_table
    global first_guessed_animal
    global second_guessed_animal
    global table
    global rows
    print(id)
    if (level == 'easy' and found == 8) or (level == 'hard' and found == 18):
        return redirect('/')
    if first_guess:
        first = int(id)
        first_guessed_animal = animals_dict.get(first)
        temp_table = []
        for i in range(len(table)):
            if i == first:
                temp_table.append(first_guessed_animal)
            else:
                temp_table.append(table[i])
        first_guess = False
        print_table(temp_table)
        return render_template('table.html', size=size, table=temp_table, rows=rows, found=found, first_guess=first_guess, first_guessed_animal=first_guessed_animal[:-1], second_guessed_animal='-', message='What\'s your second guess?')
    else:
        second = int(id)
        second_guessed_animal = animals_dict.get(second)
        for i in range(len(temp_table)):
            if i == second:
                temp_table[i] = second_guessed_animal
        print_table(temp_table)
        if first_guessed_animal[:-1] == second_guessed_animal[:-1] and first_guessed_animal[-1] != second_guessed_animal[-1]:
                found += 1
                for i in range(len(temp_table)):
                    table[i] = temp_table[i]
                print('Nice guess! ')
                first_guess = True
                print_table(temp_table)
                if (level == 'easy' and found == 8) or (level == 'hard' and found == 18):
                    return render_template('table.html', size=size, table=temp_table, rows=rows, found=found, first_guess=first_guess, first_guessed_animal=first_guessed_animal[:-1], second_guessed_animal=second_guessed_animal[:-1], message='You won! Click to play again!')
                else:
                    return render_template('table.html', size=size, table=temp_table, rows=rows, found=found, first_guess=first_guess, first_guessed_animal=first_guessed_animal[:-1], second_guessed_animal=second_guessed_animal[:-1], message='Nice guess!')
        else:
                print('Wrong! Press any key to try again! ')
                print_table(table)
                first_guess = True
                print_table(temp_table)
                return render_template('table.html', size=size, table=temp_table, rows=rows, found=found, first_guess=first_guess, first_guessed_animal=first_guessed_animal[:-1], second_guessed_animal=second_guessed_animal[:-1], message='Wrong! Try again!')


if __name__ == '__main__':
    app.run()
