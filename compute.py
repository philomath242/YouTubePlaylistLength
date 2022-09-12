from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time, asyncio


class timestamp:
    def __init__(self, t_string):
        if t_string.count(":") == 1:
            tlist = t_string.split(":")
            # only mins and secs
            self.hours = 0
            self.minutes = int(tlist[0])
            self.seconds = int(tlist[1])

        elif t_string.count(":") == 2:
            # hours too
            tlist = t_string.split(":")
            # only mins and secs
            self.hours = int(tlist[0])
            self.minutes = int(tlist[1])
            self.seconds = int(tlist[2])

    def __repr__(self) -> str:

        if self.hours > 0:
            return (
                f"{self.hours} hours, {self.minutes} minutes and {self.seconds} seconds"
            )
        else:
            return f"{self.minutes} minutes and {self.seconds} seconds"

    def __add__(self, t):

        h = self.hours + t.hours
        s = self.seconds + t.seconds
        m = self.minutes + t.minutes
        while s > 59:
            m += 1
            s -= 60
        while m > 59:
            h += 1
            m -= 60

        return timestamp(f"{h}:{m}:{s}")


def compute(url):
    # start = time.time()
    _index = url.rfind("list")
    new_url = "https://www.youtube.com/playlist?list=" + url[_index + 5 :]

    # print(new_url)

    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get(new_url)

    total = driver.find_elements(By.CSS_SELECTOR, "span.yt-formatted-string")

    print(url)
    num_of_videos = int(total[0].text)

    actions = ActionChains(driver, duration=0)

    up = False

    video_lengths = {}

    divelem = driver.find_element(By.ID, "contents")

    while True:
        actual_no_of_videos = int(
            divelem.find_elements(By.CSS_SELECTOR, "yt-formatted-string#index")[-1].text
        )
        # print(len(video_lengths), actual_no_of_videos)
        if len(video_lengths) >= actual_no_of_videos:
            break

        if up:
            up = False
            actions.send_keys([Keys.PAGE_UP] * (num_of_videos // 6)).perform()
        else:
            up = True
            actions.send_keys([Keys.PAGE_DOWN] * (num_of_videos // 6)).perform()

        elems = divelem.find_elements(By.TAG_NAME, "ytd-playlist-video-renderer")

        for elem in elems:
            index = int(
                elem.find_element(By.CSS_SELECTOR, "yt-formatted-string#index").text
            )
            duration = elem.find_element(By.CSS_SELECTOR, "span#text").text

            if index not in video_lengths and len(duration) > 1:
                video_lengths[index] = duration

    # print(len(video_lengths))

    timestamps = [timestamp(video_lengths[v]) for v in video_lengths]

    sum = timestamp("0:0:0")
    for t in timestamps:
        sum += t

    # end = time.time()

    # print(f"Executed in {end - start} seconds")

    return (sum.hours, sum.minutes, sum.seconds)

    # https://www.youtube.com/watch?v=gXH7vytxGus&list=PLbpi6ZahtOH4iCcgQWXOD4j2olmXGg8_i
    # https://www.youtube.com/playlist?list=PLbpi6ZahtOH4iCcgQWXOD4j2olmXGg8_i


# print(
#     compute("https://www.youtube.com/playlist?list=PLVR0lPOi5HIlhJcMrO-D7ssoZv0NDykP5")
# )


# print(
#     compute("https://www.youtube.com/playlist?list=PLR5CygEnLHSLjoPpVXGoC3GyOo2hd3QsY")
# )
