import spacy
from tqdm import tqdm
from spacytextblob.spacytextblob import SpacyTextBlob  # Necessary for the spacytextblob pipe to be added

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('spacytextblob')  # Adds sentiment analysis when nlp is used

def get_nlp_reviews(reviews):
    # seperate reviews into short sentences
    reviews_nlp = []
    sents_nlp = []
    with tqdm(total = len(reviews)) as pbar:
        for review in reviews:  
            x = pbar.update(1)
            doc = nlp(review)  # Creates a spacy doc object that can have each sentence seprated based on the string review
            reviews_nlp.append(doc)
            sents_nlp = sents_nlp + list(doc.sents)
    return reviews_nlp, sents_nlp


def getverb(i):  # Takes a word from a sentence and returns the verb sometimes gets the wrong verb
    if i.head.pos_ == 'VERB':  # pos_ is part of speech
        return i.head
    elif i.head == i:
        return i
    else:
        return getverb(i.head)


def main():
    reviews = open('kids.txt').read().split('\n')[:-1]
    reviews_nlp, sents_nlp = get_nlp_reviews(reviews)
    words = ['understand', 'recognize']

    for sent in sents_nlp:
        m = 0
        n = 0
        #print(sent._.blob.polarity)
        #print("i, getverb of i, i.dep_, i.head, i.children:")
        for i in sent:  # i is a word in the sentence sent
            #print(i.text, getverb(i).text, i.dep_, i.head, [v.text for v in i.children])
            # i.lemma_ is the lemmatized form i
            # i.head is a word connected over a single arc
            # i.dep_ is how it is connected i.head
            # print(i.dep_ == 'neg', sent._.blob.polarity < 0, getverb(i).lemma_)
            if (i.dep_ == 'neg') != (sent._.blob.polarity < 0):  # XOR
                if getverb(i).lemma_ in words:
                    m = 1
            #print("\nStart")
            if i.dep_ == 'nsubj':  # If the token is a normal subject
                if i.text.lower() == 'i':  # Checks if the user is misunderstanding not the Alexa eg. "I don't understand"
                    n = 1
        if m == 1 and n == 0:
            print("VV:", sent, sent._.blob.polarity)
        elif m == 1 and n == 1:

            print("I NOT UNDERSTANDING:", sent)
        else:
            print("NOT:", sent, sent._.blob.polarity)


if __name__ == '__main__':
    main()