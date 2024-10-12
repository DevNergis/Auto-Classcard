import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException


def run_matching_game(driver, da_e, da_k):
    print("매칭게임을 시작합니다...")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[5]").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#wrapper-learn .btn-opt-start").click()
    time.sleep(3.5)
    past_cards = ""
    cards = ""

    while True:
        try:
            html = BeautifulSoup(driver.page_source, "html.parser")
            cards = html.find("div", class_="match-body").get_text(strip=True)

            if past_cards == cards:
                raise NotImplementedError

            unsorted_cards = {
                f"{html.find('div', id=f'left_card_{i}').get_text(strip=True)}_{i}": int(
                    html.find('div', id=f'left_card_{i}').find("span", class_="card-score").get_text(strip=True)
                ) for i in range(4)
            }

            sorted_lists = sorted(unsorted_cards.items(), key=lambda item: item[1])

            for k, _ in sorted_lists:
                word, order = k.split("_")
                answer = da_k[da_e.index(word)]

                for j in range(4):
                    if html.find("div", id=f"right_card_{j}").get_text(strip=True) == answer:
                        left_element = driver.find_element(By.ID, f"left_card_{order}")
                        right_element = driver.find_element(By.ID, f"right_card_{j}")
                        try:
                            left_element.click()
                            right_element.click()
                        except ElementClickInterceptedException:
                            ActionChains(driver).click(left_element).click(right_element).perform()
                        raise NotImplementedError

        except NotImplementedError:
            try:
                if driver.find_element(By.CLASS_NAME, "rank-info").size["height"] > 0:
                    print("매칭게임이 완료되었습니다.")
                    driver.find_element(By.CSS_SELECTOR, ".btn-default").click()
                    time.sleep(1)
                    break
                else:
                    past_cards = cards
            except NoSuchElementException:
                past_cards = cards
        except KeyboardInterrupt:
            print("\n사용자에 의해 종료되었습니다.")
            break
