# %%
import requests
import time
with open('58k-words.txt') as fin:
    WORD_LIST = [x.rstrip().lower() for x in fin.readlines()]

# %%

x = requests.get('https://scrabblewordfinder.org/dictionary/fa')
print('<span class="green">Yes</span>' in x.text,
      '<span class="red">Not a valid word.</span>' in x.text)
# <span class="green">Yes</span>


y = requests.get('https://scrabblewordfinder.org/dictionary/fyz')
print('<span class="green">Yes</span>' in y.text,
      '<span class="red">Not a valid word.</span>' in y.text)
#print(y.text)

# <span class="red">Not a valid word.</span>
# %%

start = time.time()
valid = []
error = []
for i, w in enumerate(WORD_LIST):
    #print(w)
    try:
        req = requests.get('https://scrabblewordfinder.org/dictionary/'+w)
        page = req.text
        if '<span class="green">Yes</span>' in page and \
            '<span class="red">Not a valid word.</span>' not in page:
            valid.append(w)
        else:
            print(w, 'not valid')
    except:
        print('error for', w)
        error.append(w)
    
    if i % 1000 == 0:
        print(i, 'words in', time.time()-start, 'seconds')

print(time.time()-start)
print(len(valid))

# %%
with open('56k-valid-words.txt', 'w') as out_file:
    for w in valid: out_file.write(w+'\n')