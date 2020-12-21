"""Haiku_gen.py
Generates a Haiku given a set of poetic inputs, and the output is 
gen'd using Markov chains
"""

import random 
import pickle

def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def next_word(line, model):
    last_word = line.split()[-1]
    return random.choice(model[last_word])

def is_pick_complete(syllables, model, pick):
    complete = False
    for i in model[pick]:
        if syllable_count(i) <= syllables:
            complete = True
    return complete

def gen_line(syllables, model, current_line="", previous=""):
    if syllables > 0:
        # new line who dis
        if not previous:
            if not current_line:
                pick = random.choice(list(model.keys()))
                if is_pick_complete(syllables, model, pick):
                    return gen_line((syllables-syllable_count(pick)), model, pick)
                else:
                    return get_line(syllables, model, current_line)
            # old line wazzup
            else:
                pick = next_word(current_line, model)
                if is_pick_complete(syllables, model, pick):
                    # the pick works
                    return gen_line(syllables-syllable_count(pick), model, current_line + " " + pick)
                else:
                    # the last pick was somehow a deadend - go back and try again
                    last_word = current_line.split(" ")[-1]
                    return gen_line(syllables+syllable_count(last_word), model, current_line.rsplit(' ', 1)[0])
        else:
            pick = random.choice(list(model.keys()))
            if is_pick_complete(syllables, model, pick):
                return gen_line((syllables-syllable_count(pick)), model, pick)
            else:
                return get_line(syllables, model, "", previous)
    else:
        return current_line

def gen_haiku(model):
    line_one = gen_line(5, model)
    line_two = gen_line(7, model, "", line_one)
    line_three = gen_line(5, model, "", line_two)
    return line_one + "\n" + line_two + "\n" + line_three

def load_model(model):
    with open(model, 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    model = load_model("model.p")
    print(gen_haiku(model))