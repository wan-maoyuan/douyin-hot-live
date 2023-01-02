import time

from selenium import webdriver
from selenium.webdriver.common.by import By


HOT_LIVE_URL = "https://live.douyin.com/hot_live"
RUN_COUNT = 100000


class HotLive:
    def __init__(self):
        self.chrome = webdriver.Chrome(executable_path='./data/chromedriver.exe')

    def __del__(self):
        self.chrome.quit()

    def get_all_hot_lives(self):
        self.get_index_page()

    def get_index_page(self):
        self.chrome.implicitly_wait(20)
        self.chrome.get(HOT_LIVE_URL)
        self.chrome.maximize_window()
        lives = self.chrome.find_elements(By.XPATH, "/html/body/div[1]/div/main/div[3]/div/div[2]/div/ul/li")
        count = 0
        for index, live in enumerate(lives):
            live_name = live.find_element(By.XPATH, "a/div[2]/p").get_attribute("title")
            live_url = live.find_element(By.XPATH, "a").get_attribute("href")
            live_id = live_url.split("/")[-1]
            user_name = live.find_element(By.XPATH, "a/div[3]/a").text
            people_number = live.find_element(By.XPATH, "a/div[1]/div/div[5]/div/div/span/span").text

            count = index
            print("index = ", count)
            print("直播间名称 = ", live_name)
            print("直播链接 = ", live_url)
            print("直播ID = ", live_id)
            print("用户名 = ", user_name)
            print("直播间人数 = ", people_number)
            print()
        self._get_next_page(count)
        # js = "var q=document.getElementById('_douyin_live_scroll_container_').scrollTop=10000"
        # self.chrome.execute_script(js)

    def _get_next_page(self, count: int):
        for i in range(RUN_COUNT):
            js = "var q=document.getElementById('_douyin_live_scroll_container_').scrollTop=10000"
            self.chrome.execute_script(js)
            time.sleep(2)
            count = self._get_next_page_info(count)

    def _get_next_page_info(self, count: int) -> int:
        lives = self.chrome.find_elements(By.XPATH, "/html/body/div[1]/div/main/div[3]/div/div[2]/div/ul/li")
        for index in range(count, len(lives)):
            live_name = lives[index].find_element(By.XPATH, "a/div[2]/p").get_attribute("title")
            live_url = lives[index].find_element(By.XPATH, "a").get_attribute("href")
            live_id = live_url.split("/")[-1]
            user_name = lives[index].find_element(By.XPATH, "a/div[3]/a").text
            people_number = lives[index].find_element(By.XPATH, "a/div[1]/div/div[5]/div/div/span/span").text

            count += 1
            print("index = ", count)
            print("直播间名称 = ", live_name)
            print("直播链接 = ", live_url)
            print("直播ID = ", live_id)
            print("用户名 = ", user_name)
            print("直播间人数 = ", people_number)
            print()
        return count


if __name__ == '__main__':
    hot = HotLive()
    hot.get_all_hot_lives()
