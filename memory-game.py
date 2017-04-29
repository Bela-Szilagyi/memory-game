import random
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


def init():
    global animals
    animals = ['dog1', 'cat1', 'hippo1', 'bunny1', 'horse1', 'hedgehog1', 'wombat1', 'porcupine1',
               'dog2', 'cat2', 'hippo2', 'bunny2', 'horse2', 'hedgehog2', 'wombat2', 'porcupine2']
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
def list():
    if request.method == "POST":
        return add_new_story()
    else:
        init()
        return render_template('table.html', table=table, rows=rows, found=found)


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
    if found == 8:
        init()
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
        return render_template('table.html', table=temp_table, rows=rows, found=found, first_guess=first_guess, first_guessed_animal=first_guessed_animal, second_guessed_animal=None)
    else:
        second = int(id)
        second_guessed_animal = animals_dict.get(second)
        for i in range(len(temp_table)):
            if i == second:
                temp_table[i] = second_guessed_animal
        print_table(temp_table)
        if first_guessed_animal == second_guessed_animal and first_guessed_animal[-1] != second_guessed_animal[-1]:
                found += 1
                for i in range(len(temp_table)):
                    table[i] = temp_table[i]
                print('Nice guess! ')
                first_guess = True
                print_table(temp_table)
                return render_template('table.html', table=temp_table, rows=rows, found=found, first_guess=first_guess, first_guessed_animal=first_guessed_animal, second_guessed_animal=second_guessed_animal)
        else:
                print('Wrong! Press any key to try again! ')
                print_table(table)
                first_guess = True
                print_table(temp_table)
                return render_template('table.html', table=temp_table, rows=rows, found=found, first_guess=first_guess, first_guessed_animal=first_guessed_animal, second_guessed_animal=second_guessed_animal)


if __name__ == '__main__':
    app.run()
