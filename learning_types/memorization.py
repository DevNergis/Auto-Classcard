import time
from selenium.webdriver.common.by import By


# noinspection PyBroadException
def run_memorization(driver, num_d):
    print("Starting memorization learning...")
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "#wrapper-learn > div.start-opt-body > div > div > div > div.m-t > a").click()

    for _ in range(1, num_d):
        time.sleep(2.5)
        try:
            driver.find_element(By.CSS_SELECTOR, "#wrapper-learn > div > div > div.study-bottom > div.btn-text.btn-down-cover-box").click()
            time.sleep(0.5)
            driver.find_element(By.CSS_SELECTOR, "#wrapper-learn > div > div > div.study-bottom.down > div.btn-text.btn-know-box").click()
        except:
            print("No more cards to memorize.")
            break

    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "body > div.study-header-body > div > div:nth-child(1) > div:nth-child(1) > a").click()
    print("Memorization learning completed.")
