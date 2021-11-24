

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import string
import random
import math

############################################################
# Section 1: Markov Models
############################################################

def depunct(word):
    arr = []
    word = word.strip()
    blep = ''
    ori = len(word)
    if punctin(word):
        for index in range(ori):
            if word[index] in string.punctuation + "\t\n\r\x0b\x0c":
                arr += [blep]
                blep = ''
                arr += [word[index]]
            else:
                blep += word[index]
        arr += [blep]
    else:
        arr.append(word)
    return arr


def punctin(word):
    for sym in string.punctuation + "\t\n\r\x0b\x0c":
        if sym in word:
            return True
    return False


def delete_sym(word):
    for sym in string.punctuation + "\t\n\r\x0b\x0c":
        word = word.replace(sym, "")
    return word


def tokenize(text):
    words = filter(lambda x: x != '', text.split(" "))
    arr = []
    result = []
    for word in words:
        arr += depunct(word)
    arr = list(filter(lambda x: x != '', arr))
    for word in arr:
        if len(word)>1:
            result += [delete_sym(word)]
        elif word not in ['','\t','\n','\r','\x0b','\x0c']:
            result += [word]
    return result


def ngrams(n, tokens):
    ogtokens = tokens + ['<END>']
    p = n-1
    tokens = ['<START>'] * p + tokens
    ngramlist = []
    for tind in range(len(ogtokens)):
        ngramlist += [(tuple(tokens[tind:tind+n-1]), ogtokens[tind])]
    return ngramlist


class NgramModel(object):

    def __init__(self, n):
        self.order = n
        self.ngram = []

    def update(self, sentence):
        self.ngram += ngrams(self.order, tokenize(sentence))

    def get_tokens(self, context):
        dicty = set()
        for pair in self.ngram:
            if context == pair[0]:
                    dicty.add(pair[1]) # = self.prob(context, pair[1])
        dicty = list(dicty)
        return sorted(dicty)

    def prob(self, context, token):
        if context == ():
            count = 0
            for x in self.ngram:
                if x == (context, token):
                    count+=1
            return count/len(self.ngram)
        else:
            count = 0
            cou = 0
            for pair in self.ngram:
                if context == pair[0]:
                    count += 1
                    if token == pair[1]:
                        cou+=1
            return cou/count

    def random_token(self, context):
        r = random.random()
        total_prob = 0
        tokendist = self.get_tokens(context)
        for token in tokendist:
            previous_prob = total_prob
            total_prob += self.prob(context, token)
            if total_prob>r and r>=previous_prob:
                return token

    def random_text(self, token_count):
        p = self.order - 1
        # if self.order > 1:
        context = ('<START>',) * p
        arr = []
        for x in range(token_count):
            newword = self.random_token(context)
            arr += [newword]
            if newword == "<END>":
                context = ('<START>',) * p
            else:
                context = list(context)
                if len(context) > 0:
                    context.pop(0)
                    context += [newword]
                context = tuple(context)
        return " ".join(arr)
        # else:
        #     arr = [self.random_token(()) for x in range(token_count)]
        #     return " ".join(arr)

    def perplexity(self, sentence):
        p = 0
        d = tokenize(sentence)

        for context, token in ngrams(self.order, d):
            p += math.log(self.prob(context, token))
        ins = 1/math.exp(p)
        return ins ** (1/(len(d)+1))


n = NgramModel(1)
n.update("a b c d")
n.update("a b a b")
print(n.perplexity("a b"))

# m = NgramModel(2)
# m.update("a b c d")
# m.update("a b a b")
# print(m.ngram)
# random.seed(2)
# print(m.random_text(15))

def create_ngram_model(n, path):
    model = NgramModel(n)
    with open(path, "r+") as f:
        [model.update(line) for line in f.readlines()]
    return model

# model = create_ngram_model(2, 'frankenstein.txt')
# print(model.random_text(15))

# ############################################################
# # Section 2: Feedback
# ############################################################

# feedback_question_1 = 0

# feedback_question_2 = """
# Type your response here.
# Your response may span multiple lines.
# Do not include these instructions in your response.
# """

# feedback_question_3 = """
# Type your response here.
# Your response may span multiple lines.
# Do not include these instructions in your response.
# """
