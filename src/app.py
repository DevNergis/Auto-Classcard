import random
import time
import warnings

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from learning_types import (
    memorization,
    recall,
    spelling,
    test,
    matching_game,
    matching_game_API,
    quiz_battle,
)
from src.utility import (
    chd_wh,
    get_id,
    word_get,
    choice_class,
    choice_set,
    classcard_api_post,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)


def chrome():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)


def main(driver: WebDriver, loop: bool):
    temp_loop = True

    account = get_id()
    driver.get("https://www.classcard.net/Login")
    time.sleep(1)
    driver.find_element(By.NAME, "login_id").send_keys(account["ID"])
    driver.find_element(By.NAME, "login_pwd").send_keys(account["PW"])
    time.sleep(1)
    driver.find_element(
        By.CSS_SELECTOR,
        "#loginForm > div.checkbox.primary.text-primary.text-center.m-t-md > a",
    ).click()
    time.sleep(1)

    while temp_loop:
        time_1, time_2 = (
            round(random.uniform(0.7, 1.3), 4),
            round(random.uniform(1.7, 2.3), 4),
        )

        driver.get("https://www.classcard.net/Main")

        try:
            class_list_element = driver.find_element(
                By.CSS_SELECTOR,
                "body > div.mw-1080 > div:nth-child(6) > div > div > div.left-menu > div.left-item-group.p-t-none.p-r-lg > div.m-t-sm.left-class-list",
            )
            class_dict = {
                i: {
                    "class_name": item.text,
                    "class_id": item.get_attribute("href").split("/")[-1],
                }
                for i, item in enumerate(
                    class_list_element.find_elements(By.TAG_NAME, "a")
                )
                if item.get_attribute("href").split("/")[-1] != "joinClass"
            }

            if not class_dict:
                print("클래스가 없습니다.")
                quit()
            choice_class_val = 0 if len(class_dict) == 1 else choice_class(class_dict)
            class_id = class_dict[choice_class_val]["class_id"]

            driver.get(f"https://www.classcard.net/ClassMain/{class_id}")
            time.sleep(1)

            sets_div = driver.find_element(
                By.XPATH, "/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div"
            )
            sets = sets_div.find_elements(By.CLASS_NAME, "set-items")
            sets_dict = {
                i: {
                    "card_num": item.find_element(By.TAG_NAME, "a")
                    .find_element(By.TAG_NAME, "span")
                    .text,
                    "title": item.find_element(By.TAG_NAME, "a").text.replace(
                        item.find_element(By.TAG_NAME, "a")
                        .find_element(By.TAG_NAME, "span")
                        .text,
                        "",
                    ),
                    "set_id": item.find_element(By.TAG_NAME, "a").get_attribute(
                        "data-idx"
                    ),
                }
                for i, item in enumerate(sets)
            }

            choice_set_val = choice_set(sets_dict)
            set_site = f"https://www.classcard.net/set/{sets_dict[choice_set_val]['set_id']}/{class_id}"
            driver.get(set_site)
            time.sleep(1)

            user_id = int(driver.execute_script("return c_u;"))
            ch_d = chd_wh()

            driver.find_element(
                By.CSS_SELECTOR,
                "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > a",
            ).click()
            driver.find_element(
                By.CSS_SELECTOR,
                "body > div.test > div.p-b-sm > div.set-body.m-t-25.m-b-lg > div.m-b-md > div > ul > li:nth-child(1)",
            ).click()

            html = BeautifulSoup(driver.page_source, "html.parser")
            num_d = (
                len(
                    html.find("div", class_="flip-body").find_all(
                        "div", class_="flip-card"
                    )
                )
                + 1
            )
            time.sleep(0.5)

            da_e, da_k, da_kn, da_kyn, da_ked, da_sd = word_get(driver, num_d)

            print(da_e, da_k, da_kn, da_kyn, da_ked, da_sd)

            if ch_d == 1:
                print("암기학습 API 요청 변조를 시작합니다.")
                classcard_api_post(
                    user_id, sets_dict[choice_set_val]["set_id"], class_id, num_d, 1
                )
            elif ch_d == 2:
                print("리콜학습 API 요청 변조를 시작합니다.")
                classcard_api_post(
                    user_id, sets_dict[choice_set_val]["set_id"], class_id, num_d, 2
                )
            elif ch_d == 3:
                print("스펠학습 API 요청 변조를 시작합니다.")
                classcard_api_post(
                    user_id, sets_dict[choice_set_val]["set_id"], class_id, num_d, 3
                )
            elif ch_d == 4:
                match_site = f"https://www.classcard.net/Match/{sets_dict[choice_set_val]['set_id']}?c={class_id}"
                driver.get(match_site)
                matching_game_API.run_matching_game_api(driver, match_site)
            elif ch_d == 5:
                test.run_test(driver, num_d, da_e, da_k, da_kn, da_ked, time_1)
            elif ch_d == 6:
                quiz_battle.run_quiz_battle(driver, da_e, da_k, da_sd)
            elif ch_d == 7:
                memorization.run_memorization(driver, num_d)
            elif ch_d == 8:
                recall.run_recall(driver, num_d, da_e, da_kyn, time_2)
            elif ch_d == 9:
                spelling.run_spelling(driver, num_d, da_e, da_k)
            elif ch_d == 10:
                matching_game.run_matching_game(driver, da_e, da_k)
            else:
                print("프로그램을 종료합니다.")
        except KeyboardInterrupt:
            print("프로그램을 종료합니다.")
        finally:
            if loop:
                pass
            else:
                temp_loop = False

    driver.quit()
