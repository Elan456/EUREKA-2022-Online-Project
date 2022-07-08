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
    # separates reviews into short sentences
    reviews_nlp = []
    sents_nlp = []
    with tqdm(total=len(reviews)) as pbar:
        for review in reviews:
            # Creates a spacy doc object that can have each sentence separated based on the string review
            doc = nlp(review)
            reviews_nlp.append(doc)
            # break_conjunctions also breaks sentences up along with conjunctions
            sents_nlp = sents_nlp + break_conjunctions(doc)
    return reviews_nlp, sents_nlp


def get_verb(i):
    """
Takes a word from a sentence and returns the verb most closely related to the given token i
    :param i: Token
    :return: Token
    """
    if i.head.pos_ == 'VERB':  # pos_ is part of speech
        return i.head
    elif i.head == i:
        return i
    else:
        return get_verb(i.head)


def check_sent_for_poor_recognition(sent, info=False):
    """
Checks a sentence to see if the Alexa was having trouble understanding the user
    :param sent: Spacy sentence
    :param info: Whether individual token data is printed out for testing purposes
    :return: Boolean
    """
    keywords = ['understand', 'recognize']
    m = 0  # Whether the sentence is about misunderstanding
    n = 0  # Whether the sentence is about the user misunderstanding instead of the Alexa
    keywordPresent = True in [(i.lemma_ in keywords) for i in sent]  # Checks if any of the keywords are in the sentence
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
            print(i, i.tag_, spacy.explain(i.tag_), "|||", i.pos_, spacy.explain(i.pos_), "|||", i.dep_, spacy.explain(i.dep_), "|", get_verb(i).lemma_)

        # Checking if a negative modifier is acting on a keyword
        if i.dep_ == 'neg':  # Is the word negating something?
            if get_verb(i).lemma_ in keywords:  # Is the most closely related verb to this word a keyword?
                m = 1

        if i.tag_ == "PRP" and i.dep_ == "nsubj" and i.lemma_.lower() == "i":  # If the nominal subject is a personal pronoun that is "i"
            n = 1
    if m == 1 and n == 0:  # The sentence is about misunderstanding but not the user misunderstanding
        print("WW:", sent, sent._.blob.polarity)
        return True
    elif m == 1 and n == 1:  # The sentence is about misunderstanding but the user is the one misunderstanding
        print("I NOT:", sent)  # The user is the one who could not understand
    else:
        print("NOT:", sent, sent._.blob.polarity)  # The sentence is not about misunderstanding

    return False


def main():
    reviews = open('kids.txt').read().split('\n')[:-1]
    reviews_nlp, sents_nlp = get_nlp_reviews(reviews)

    for sent in sents_nlp:  # Checks all the sentences for poor recognition
        check_sent_for_poor_recognition(sent)  # The return value isn't taken we just looked at the print output


if __name__ == '__main__':
    main()
