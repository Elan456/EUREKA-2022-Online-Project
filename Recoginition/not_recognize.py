import spacy
from tqdm import tqdm
nlp = spacy.load("en_core_web_lg")


def get_nlp_reviews(reviews):
    # seperate reviews into short sentences
    reviews_nlp = []
    sents_nlp = []
    with tqdm(total = len(reviews)) as pbar:
        for review in reviews:  
            x = pbar.update(1)
            doc = nlp(review)  # Creates a spacy doc object that can have each sentence seprated based the on the string review
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
    print(spacy.explain("acl"))
    print(spacy.explain("dobj"))

    for sent in sents_nlp:
        m = 0
        n = 0
        for i in sent:  # i is a word in the sentence sent
            print("i, getverb of i, i.dep_, i.head:", i.text, getverb(i).text, i.dep_, i.head)
            # i.lemma_ is the lemmatized form i
            # i.head is a word connected over a single arc
            # i.dep_ is how it is connected i.head
            if i.dep_ == 'neg':
                if getverb(i).lemma_ in words:
                    m = 1
            #print("\nStart")
            if i.dep_ == 'nsubj':
                #print("i.lemma:", i.lemma_)
                #print(i, i.lemma_, i.lemma_ == "I")
                if i.text.lower() == 'i':  # Checks if the user is misunderstanding not the Alexa eg. "I don't understand"
                    #print("dep_ is nsubj and lemma is -pron-", i.text)
                    n = 1
                    continue
            #print("End\n")
        if m == 1 and n == 0:
            print(sent)
        elif m == 1 and n == 1:
            print("THIS HIT THE NEGATED KEYWORD BUT I THING:")
            print(sent)


if __name__ == '__main__':
    main()