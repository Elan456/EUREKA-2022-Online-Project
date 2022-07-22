import not_recognize
import pandas as pd
import numpy as np
import tqdm
import multiprocessing as mp

check = not_recognize.check_sent_for_poor_recognition  # Grabs the function


# for result in tqdm.tqdm([pool.apply(get_sentiment, args=(row,)) for row in all_data]):
#     results.append(result)


def get_understand(review, info=False):
    clauses = not_recognize.break_conjunctions(not_recognize.nlp(review[0]))
    c = 0
    for sent in clauses:  # If any of the clauses are positive, the whole review is
        if check(sent, info):
            c = 1
            break
    return c


"""
Goal:
OG score: 137
Get to 60% of the 300Check test set

176 - removed keyword recognize
176 - Added you to n detection
177 (48, 75) - Added understand me detection
183 (53, 64) - Added recognize voice/command detection
188 (47, 65) - Added they to subject n = 1 prevention
189 (46, 65) - Added Alexa's voice detection
190 (46, 64) - Added check word "instruction" for not recognize
206 (45, 49) - Added check word "answer" for not recognize because of the prevalence of quiz skills (Also changed some false positives to be true positives (3) in data set)

You won't be able to understand her
You will not be understood by her

understand you
understand me

recognize command

"""

check(not_recognize.nlp("She won't understand me"), info=True)
exit()
if __name__ == "__main__":
    reviews = pd.read_csv("300Check.csv").to_numpy()[:, 1:]
    # print(reviews[:20])
    # print("Previous points:", sum(reviews[:, 2]))
    points = 0
    false_negs = 0
    nl = []
    false_pos = 0
    pl = []
    for i, r in enumerate(reviews):
        is_about_understanding = get_understand(r)
        correct_answer = r[1] if r[2] == 1 else (r[1] + 1) % 2
        if is_about_understanding == correct_answer:
            points += 1
        elif is_about_understanding == 1 and correct_answer == 0:
            false_pos += 1
            pl.append(i)
        elif is_about_understanding == 0 and correct_answer == 1:
            false_negs += 1
            nl.append(i)
    print("Points:", points, "Percent Points:", str(round(points / 300, 2) * 100) + "%")
    print("Falsepos: ", false_pos, "False Negs:", false_negs)
    print(pl)
    print(nl)
