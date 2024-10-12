import time
import httpx
from urllib.parse import quote
import env


class Ggk:
    def __init__(self, key_array):
        self.k = key_array

    def c(self, a):
        r = ""
        a = str(a)
        for ii in a:
            if ii == ".":
                r += "."
                continue
            try:
                idx = int(ii)
            except ValueError:
                continue
            if idx < len(self.k):
                r += self.k[idx]
        return r

    def hack(self, time_val, score):
        return {
            't': self.c(time_val / 1000),
            's': self.c(score),
            'm': self.c(1)
        }


# noinspection PyTypeChecker
def run_matching_game_api(driver, match_site):
    time.sleep(1.5)
    tid = driver.execute_script('return window.tid;')
    set_idx = driver.execute_script('return window.set_idx;')
    class_idx = driver.execute_script('return window.class_idx;')
    cookies = "; ".join([f"{c['name']}={c['value']}" for c in driver.get_cookies()])

    #-----------options-------------
    count = env.setting_matching_game['count']
    interval = env.setting_matching_game['interval']
    #-----------options-------------

    activity = 4
    start_time = int(time.time() * 1000)

    arr_key = driver.execute_script('return ggk.a();')
    ggk_instance = Ggk(arr_key)
    arr_score = [ggk_instance.hack(start_time + i * interval, 130) for i in range(count)]

    encoded_data_array = [f"set_idx={set_idx}"]
    for key in arr_key:
        encoded_data_array.append(f"arr_key%5B%5D={key}")
    for index, score in enumerate(arr_score):
        encoded_data_array.append(f"arr_score%5B{index}%5D%5Bt%5D={quote(score['t'])}")
        encoded_data_array.append(f"arr_score%5B{index}%5D%5Bs%5D={quote(score['s'])}")
        encoded_data_array.append(f"arr_score%5B{index}%5D%5Bm%5D={quote(score['m'])}")
    encoded_data_array.append(f"activity={activity}")
    encoded_data_array.append(f"tid={tid}")
    encoded_data_array.append(f"class_idx={class_idx}")

    #print(encoded_data_array)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": match_site,
        "Origin": "https://classcard.net",
        "Cookie": cookies,
    }

    try:
        response = httpx.post("https://www.classcard.net/Match/save", headers=headers,
                              data="&".join(encoded_data_array))
        response.raise_for_status()
        #data = response.json()
        #print("응답 데이터:", data)
        print("조작된 페이로드가 성공적으로 전송되었습니다.")
    except httpx.RequestError as e:
        print("페이로드 전송 중 오류가 발생했습니다:", e)
    except ValueError:
        print("서버로부터 유효한 JSON 응답을 받지 못했습니다.")
