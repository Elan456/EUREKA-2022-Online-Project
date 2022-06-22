from bs4 import BeautifulSoup as BS


#  "https://www.amazon.com/Barbie-You-Can-Be-Anything/dp/B081DD8P2W/ref=sr_1_1?qid=1655822134&rnid=13727922011&s=alexa-skills&sr=1-1#"

class Review:
    def __init__(self, user, review, rating, date):
        self.user = user
        self.review = review
        self.rating = rating
        self.date = date


def make_apos(string: str):
    while True:
        i = string.find("\\xe2\\x80\\x99")
        if i != -1:
            string = string.replace(string[i:i + len("\\xe2\\x80\\x99")], "\'")
        else:
            break
    return string


def cus_data(soup):  # Soup is BeatuifulSoup parsed html string
    # find the Html tag
    # with find()
    # and convert into string
    data_str = ""
    review_list = []
    users = []
    reviews = []

    for item in soup.find_all("span", class_="a-profile-name"):
        name = data_str + item.get_text()
        users.append(name)
        data_str = ""

    for item in soup.find_all("span", class_="a-size-base review-text review-text-content"):
        review = data_str + item.get_text()
        reviews.append(make_apos(review))
        data_str = ""
    print("# of users:", len(users))
    print("# of description:", len(reviews))
    for i in range(len(users)):
        entire_review = {}  # Empty dictionary
        entire_review["User"] = users[i]
        entire_review["Review"] = reviews[i]
        review_list.append(entire_review)
    return review_list


with open("page_source.txt", "r") as raw_html:
    raw_html = raw_html.read()
    soup = BS(raw_html, 'html.parser')

data = cus_data(soup)
print(data)
