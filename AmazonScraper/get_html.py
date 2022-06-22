from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
options = Options()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def get_html(url):
    driver.get(url)
    raw_html = ""
    while True:
        try:
            raw_html += str(driver.page_source.encode(sys.stdout.encoding, errors="replace"))
            print(len(raw_html))

            driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='a-last']/a"))))
            driver.find_element_by_xpath("//li[@class='a-last']/a").click()
            time.sleep(10)

            print("Navigating to Next Page")
        except (TimeoutException, WebDriverException) as e:
            print("Last page reached")
            break

    driver.quit()
    print("before bombing run: ", len(raw_html))
    while True:  # Maybe keep top reviews for something else
        index = raw_html.find("a-column a-span6 view-point-review positive-review")
        endindex = raw_html[index:].find("reviews-container") + index
        print("index", index, "endindex: ", endindex)
        if index != -1:
            print("found something")
            raw_html = raw_html.replace(raw_html[index:endindex], "")
        else:
            break
    print("after bombing run: ", len(raw_html))

    with open("page_source.txt", "w") as file:
        file.write(raw_html)

get_html("https://www.amazon.com/Barbie-You-Can-Be-Anything/product-reviews/B081DD8P2W/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")