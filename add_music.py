import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time
import reader

class AddMusic:
    def __init__(self):
        self.driver = uc.Chrome(version_main=144)
        self.playlist_name = ""

    def login(self):
        self.driver.get("https://music.youtube.com/")
        time.sleep(2)

        signin = self.driver.find_element(By.CSS_SELECTOR, ".sign-in-link")
        self.driver.execute_script("arguments[0].click()", signin)
        input("When you successfully log in and the page loads, press ENTER")

    def get_playlist_name(self):
        with open("songs.txt", "r", encoding="UTF-8") as f:
            for i, line in enumerate(f):
                if i == 0:
                    self.playlist_name = line.strip()

    def add_songs(self):
        with open("songs.txt", "r", encoding="UTF-8") as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                song = line.strip()
                # search
                elem = self.driver.find_element(By.CSS_SELECTOR, '[class="search-box style-scope ytmusic-search-box"] input#input')
                self.driver.execute_script("arguments[0].click()", elem)
                elem.send_keys(song)
                elem.send_keys(Keys.ENTER)
                time.sleep(1)
                # 3 colon
                elem = self.driver.find_element(By.CSS_SELECTOR, 'ytmusic-shelf-renderer ytmusic-responsive-list-item-renderer .menu button')
                self.driver.execute_script("arguments[0].click()", elem)
                time.sleep(1)
                # add to playlist button
                try:
                    elem = self.driver.find_element(By.XPATH, '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-iron-dropdown/div/ytmusic-menu-popup-renderer/tp-yt-paper-listbox/ytmusic-menu-navigation-item-renderer[2]/a/yt-formatted-string')
                    self.driver.execute_script("arguments[0].click()", elem)
                    time.sleep(1)
                    # playlist
                    target_playlist = self.driver.find_element(By.XPATH, f"//ytmusic-playlist-add-to-option-renderer//yt-formatted-string[@title='{self.playlist_name}' or text()='{self.playlist_name}']")
                    self.driver.execute_script("arguments[0].click()", target_playlist)
                    elem = self.driver.find_element(By.ID, 'clear-button')
                    self.driver.execute_script("arguments[0].click()", elem)
                    time.sleep(0.5)
                except:
                    print("We can't find the playlist")
                    return


def add_music_to_playlist():
    bot = AddMusic()
    bot.login()
    bot.get_playlist_name()
    try:
        bot.add_songs()
    except:
        print("Something went wrong. Maybe you haven't log in")

if __name__ == "__main__":
    print("For the addition to be successful, you must have a single playlist in YouTube Music that is named the same as in Spotify")
    # is_any_song = True
    is_any_song = reader.read_songs("data.txt")
    if (is_any_song == False):
        print("You have no song in the playlist or you have some problem with file")
    else:
        add_music_to_playlist()


