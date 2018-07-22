# What is it

Ugly prototype of script to prepare subs for video from a plain text. 


# Prepare

```
pip3 install nltk
python3
>> import nltk
>> nltk.download('punkt')
>> nltk.download('gutenberg')
>> quit() 
```

# Use

```
python3 subtitles.py ex1.txt
python3 subtitles.py ex2.txt
python3 subtitles.py ex3.txt
python3 subtitles.py ex4.txt
python3 subtitles.py ex5.txt
```

# Next steps

1. Teach NLTK model to tokenize according to subs rules.
2. Teach model to group hard related words on a same line.
3. Do something with trashy code.