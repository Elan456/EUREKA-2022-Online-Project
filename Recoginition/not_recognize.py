import spacy
from tqdm import tqdm
from spacytextblob.spacytextblob import SpacyTextBlob  # Necessary for the spacytextblob pipe to be added

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('spacytextblob')  # Adds sentiment analysis when nlp is used


def break_conjunctions(doc):
    seen = set()  # keep track of covered words

    chunks = []
    for sent in doc.sents:
        heads = [cc for cc in sent.root.children if cc.dep_ == 'conj']

        for head in heads:
            words = [ww for ww in head.subtree]
            for word in words:
                seen.add(word)

            chunks.append((head.i, words))

        unseen = [ww for ww in sent if ww not in seen]
        # chunk = ' '.join([ww.text for ww in unseen])
        chunks.append((sent.root.i, unseen))

    chunks = sorted(chunks, key=lambda x: x[0])
    # print([nlp(" ".join([v.text for v in c[1]])) for c in chunks])
    return [nlp(" ".join([v.text for v in c[1]])) for c in chunks]
    # for ii, chunk in chunks:
    #     print(chunk)


def get_nlp_reviews(reviews):
    # seperate reviews into short sentences
    reviews_nlp = []
    sents_nlp = []
    with tqdm(total=len(reviews)) as pbar:
        for review in reviews:
            x = pbar.update(1)
            doc = nlp(review)  # Creates a spacy doc object that can have each sentence seprated based on the string review
            reviews_nlp.append(doc)
            sents_nlp = sents_nlp + break_conjunctions(doc)
    return reviews_nlp, sents_nlp


def getverb(i):  # Takes a word from a sentence and returns the verb sometimes gets the wrong verb
    if i.head.pos_ == 'VERB':  # pos_ is part of speech
        return i.head
    elif i.head == i:
        return i
    else:
        return getverb(i.head)


def check_sent_for_poor_recognition(sent, info=False):
    keywords = ['understand', 'recognize']
    m = 0
    n = 0
    double_negative = 0  # Set to 1 when a negative word negates a negative adjective to understand
    # print(sent._.blob.polarity)
    # print("i, getverb of i, i.dep_, i.head, i.children:")
    keywordPresent = True in [(i.lemma_ in keywords) for i in sent]
    if keywordPresent and sent._.blob.polarity < 0:  # If there is a keyword and the sentiment is negative
        m = 1  # if n gets set to 1 this won't matter
    for i in sent:  # i is a word in the sentence sent
        """
        i.lemma_ is the lemmatized form of i
        i.head is a word connected over a single arc
        i.dep_ is the token's relationship to other tokens
        i.tag_ detailed part-of-speech tag
        i.pos_ part-of-speech
        """
        if info:  # For debug and testing purposes
            print(i, i.tag_, spacy.explain(i.tag_), "|||", i.pos_, spacy.explain(i.pos_), "|||", i.dep_, spacy.explain(i.dep_), "|", getverb(i).lemma_)

        # Checking if a negative modifer is acting on a keyword
        if i.dep_ == 'neg':
            if getverb(i).lemma_ in keywords:
                m = 1
        # print("\nStart")
        if i.tag_ == "PRP" and i.dep_ == "nsubj" and i.lemma_.lower() == "i":  # If the nominal subject is a personal pronoun that is i
            n = 1
    if m == 1 and n == 0:
        print("WW:", sent, sent._.blob.polarity)
        return True
    elif m == 1 and n == 1:
        print("I NOT:", sent)  # The user is the one who could not understand
    else:
        print("NOT:", sent, sent._.blob.polarity)

    return False


def main():
    reviews = open('kids.txt').read().split('\n')[:-1]
    reviews_nlp, sents_nlp = get_nlp_reviews(reviews)

    for sent in sents_nlp:
        check_sent_for_poor_recognition(sent)


if __name__ == '__main__':
    # break_conjunctions(nlp("I love chicken, but it taste gross"))
    # check_sent_for_poor_recognition(nlp("It has lot's of trouble understanding even simple commands"), info=True)
    main()
