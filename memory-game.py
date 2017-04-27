import random
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


animals = ['dog', 'cat', 'hippo', 'bunny', 'horse', 'hedgehog', 'wombat', 'porcupine',
           'dog', 'cat', 'hippo', 'bunny', 'horse', 'hedgehog', 'wombat', 'porcupine']
# animals = ['dog', 'cat', 'dog', 'cat']

animals = random.sample(animals, len(animals))
animals_dict = {}
for index, animal in enumerate(animals):
    animals_dict[index] = animal
print(animals_dict)
table = []
for i in range(len(animals)):
    table.append('0')
rows = int(len(animals) ** 0.5)
first_guess = True
found = 0


def print_table(table_to_print):
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
        return render_template('table.html', table=table, rows=rows, found=found)


@app.route('/click/<id>')
def click(id):
    print(id)
    global first_guess
    global found
    global temp_table
    global first_guessed_animal
    global second_guessed_animal
    if found == 8:
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
        return render_template('table.html', table=temp_table, rows=rows, found=found)
    else:
        second = int(id)
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
                print_table(temp_table)
                return render_template('table.html', table=temp_table, rows=rows, found=found)
        else:
                print('Wrong! Press any key to try again! ')
                print_table(table)
                first_guess = True
                print_table(temp_table)
                return render_template('table.html', table=temp_table, rows=rows, found=found)


print_table(table)
if __name__ == '__main__':
    app.run()
