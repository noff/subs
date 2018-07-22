# It's only to test reducer on dump file

import textwrap

file = open("rows.ex1.txt", "r")
text = file.read()
rows = text.split("\n")

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
print(rows)



