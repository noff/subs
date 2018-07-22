import nltk
# nltk.download('punkt')
# nltk.download('gutenberg')
from nltk.corpus import gutenberg
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
import textwrap
import sys
import os.path

if len(sys.argv) != 2:
    print("Syntax: python3 subtitles.py filename")
    print("Filenames: ex1.txt, ex2.txt, etc.")
    quit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print("Source file '{}' not found ".format(filename))
    quit(1)

# Read source data
file = open(filename, "r")
sentence = file.read()

# Teach model on Gutenberg corpora
text = ""
for file_id in gutenberg.fileids():
    text += gutenberg.raw(file_id)

trainer = PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True
trainer.train(text)
tokenizer = PunktSentenceTokenizer(trainer.get_params())

# Tokenize by default
rows = tokenizer.tokenize(sentence)

# ** Manual cut

# Split >> if not in the beginning
new_rows = []
for item in rows:
    if '>>' in item:
        if item[:2] == '>>':
            # Split. Prepend all elements. Store it.
            substrings = item.split('>>')
            for substring in substrings:
                if substring != '':
                    new_rows.append('>> ' + substring.strip())
        else:
            # Split. Prepend all elements except the first. Store it.
            substrings = item.split('>>')
            for index, substring in enumerate(substrings):
                if index == 0:
                    new_rows.append(substring.strip())
                else:
                    if substring != '':
                        new_rows.append('>> ' + substring.strip())

    else:
        new_rows.append(item.strip())

rows = new_rows

new_rows = []
for row in rows:

    # Fix this: [ELECTRONIC DANCE MUSIC] Hey, hey, let's take a selfie!
    # Fix this: Fuck [CAR SPEEDS AWAY]
    # Fix this: Fuck [CAR SPEEDS AWAY] it
    # Here must be a better way to split this sentence to chunks
    if '[' in row and not row[:2] == '>>': # Problems in ex3 in the end
        substrings = row.split('[')
        for substring in substrings:
            substring = substring.strip()
            if substring != '':
                if ']' in substring:
                    substring = '[' + substring
                    if substring[len(substring) - 1] == ']':
                        new_rows.append(substring)
                    else:
                        subsubstrings = substring.split(']')
                        for subsubstring in subsubstrings:
                            subsubstring = subsubstring.strip()
                            if subsubstring != '':
                                if '[' in subsubstring:
                                    new_rows.append(subsubstring + ']')
                                else:
                                    new_rows.append(subsubstring)
                else:
                    new_rows.append(substring)
    else:
        new_rows.append(row)


rows = new_rows

# for row in rows:
#     print(row)
# exit()

# Save dump for debug
dump = open("rows." + filename, "w")
for row in rows:
    dump.write(row + "\n")
dump.close()

# ** Reduce

captions = []
caption = []
total_rows = len(rows)
for index, row in enumerate(rows):
    # Flush
    if len(caption) == 2:
        captions.append(caption)
        caption = []

    if len(row) > 0:

        # Leave tags on separate places
        if row[0] == '[':
            caption.append(row)
            rows[index] = ''
            continue

        # Under no circumstances should dialogue from two separate speakers be contained within the same caption
        if row[:2] == '>>' and len(row) <= 42:
            if len(caption) == 0:
                caption = [row]
                captions.append(caption)
                caption = []
            else:
                captions.append(caption)
                caption = [row]
                captions.append(caption)
                caption = []
            rows[index] = ''
            continue

        # Add normal sentences
        if len(row) <= 42 and len(row) >= 30:
            caption.append(row)
            rows[index] = ''
            continue

        # Concat short sentences
        if len(row) < 30 and index < (total_rows - 1) and rows[index + 1][0] != '[' and rows[index + 1][0] != '>' and (len(rows[index + 1]) + len(row)) < 42:
            caption.append(row + ' ' + rows[index + 1])
            rows[index + 1] = '' # Do not remove
            rows[index] = ''
            continue

        # Just add short sentence
        if len(row) <= 42:
            caption.append(row)
            rows[index] = ''
            continue

        # Split long sentences

        if row[:2] == '>>' and len(row) > 42:
            # Under no circumstances should dialogue from two separate speakers be contained within the same caption
            if len(caption) == 1:
                captions.append(caption)
                caption = []

            elements = textwrap.wrap(row, 42, break_long_words=False)
            for element in elements:
                if len(caption) == 2:
                    captions.append(caption)
                    caption = []
                caption.append(element)
                continue
            rows[index] = ''
            continue

        if len(row) > 42:
            elements = textwrap.wrap(row, 42, break_long_words=False)
            for element in elements:
                if len(caption) == 2:
                    captions.append(caption)
                    caption = []
                caption.append(element)
                continue
            rows[index] = ''

# Caption leftover
if len(caption) != 0:
    captions.append(caption)
    caption = []

for index, caption in enumerate(captions):
    print(index)
    for row in caption:
        print(row)
    print('')

# Show leftovers
# print(rows)



