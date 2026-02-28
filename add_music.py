import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time
import reader
from difflib import SequenceMatcher

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
                elem = self.driver.find_element(By.XPATH, '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-iron-dropdown/div/ytmusic-menu-popup-renderer/tp-yt-paper-listbox/ytmusic-menu-navigation-item-renderer[2]/a/yt-formatted-string')
                self.driver.execute_script("arguments[0].click()", elem)
                time.sleep(1)
                # playlist
                # target_playlist = self.driver.find_element(By.XPATH, f"//ytmusic-playlist-add-to-option-renderer//yt-formatted-string[@title='{self.playlist_name}' or text()='{self.playlist_name}']")
                # self.driver.execute_script("arguments[0].click()", target_playlist)

                #scroll
                try:
                    is_found = False
                    for j in range(10):
                        try:
                            target_playlist = self.driver.find_element(By.XPATH, f"//ytmusic-playlist-add-to-option-renderer//yt-formatted-string[@title='{self.playlist_name}' or text()='{self.playlist_name}']")
                            self.driver.execute_script("arguments[0].click()", target_playlist)
                            is_found = True
                            break
                        except:
                            elem = self.driver.find_element(By.CSS_SELECTOR, 'ytmusic-add-to-playlist-renderer #playlists')
                            self.driver.execute_script("arguments[0].scrollTop += 300;", elem)
                            time.sleep(0.5)

                    if not is_found and j == 9:
                        print(f"We can't find the playlist")
                        return
                    if not is_found:
                        continue
                except:
                    print(f"We can't find the playlist")
                    return

                elem = self.driver.find_element(By.ID, 'clear-button')
                self.driver.execute_script("arguments[0].click()", elem)
                time.sleep(0.5)

    def some_songs_was_missing(self):
        number_of_songs_from_spotify = 0
        with open("songs.txt", 'r', encoding="UTF-8") as file:
            for line in file:
                number_of_songs_from_spotify += 1

        number_of_songs_from_spotify -= 1
        print("Total number of songs:", number_of_songs_from_spotify)

        self.driver.get("https://music.youtube.com/library/playlists")
        time.sleep(3)
        try:
            is_found = False
            last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            xpath_query = f"//ytmusic-two-row-item-renderer//a[@title='{self.playlist_name}']"
            for j in range(20):
                try:
                    target_playlist = self.driver.find_element(By.XPATH, xpath_query)
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_playlist)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click()", target_playlist)
                    is_found = True
                    break
                except:
                    self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                    time.sleep(1)
                    new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
            if not is_found:
                return
            else:
                time.sleep(2)
        except:
            print("Something is wrong with your library")
            return

        # create an array of songs
        print("are we still here?")
        songs_here = self.driver.find_elements(By.CSS_SELECTOR, 'ytmusic-responsive-list-item-renderer .title a')
        songs_here = [song.text for song in songs_here]
        print(songs_here)
        print(len(songs_here))
        is_missing = self.delete_if_in_file(songs_here, number_of_songs_from_spotify)
        return is_missing


    def delete_if_in_file(self, songs_here, number_of_songs_from_spotify):
        songs_here = [song.lower() for song in songs_here]
        spotify_songs = []
        already_in_spotify = []
        with open("songs.txt", 'r', encoding="UTF-8") as file:
            for i, line in enumerate(file):
                spotify_songs.append(line.lower().strip())
        spotify_songs.pop(0)
        spotify_songs_name = []
        for song in spotify_songs:
            index = song.find('—')
            spotify_songs_name.append(song[0:index].strip())

        print(spotify_songs_name)
        if len(spotify_songs) - len(songs_here) != 0:
            for i in range(len(spotify_songs)):
                for here in songs_here:
                    similarity1 = SequenceMatcher(None, spotify_songs[i], here).ratio()
                    similarity2 = SequenceMatcher(None, spotify_songs_name[i], here).ratio()
                    if similarity1 > 0.75 or similarity2 > 0.75:
                        already_in_spotify.append(spotify_songs[i])
                        break
                    elif here in spotify_songs_name[i]:
                        already_in_spotify.append(spotify_songs[i])
                        break
        set_already_in_spotify = set(already_in_spotify)
        set_sporify_songs = set(spotify_songs)

        still_not_found = set_sporify_songs - set_already_in_spotify
        print(still_not_found)
        print(len(still_not_found))

        self.driver.get("https://music.youtube.com/")
        time.sleep(2)
        with open("songs.txt", "w", encoding="UTF-8") as f:
            f.write(f"{self.playlist_name}\n")
            for song in still_not_found:
                f.write(f"{song}\n")
        # self.add_songs()

        number_of_missing_songs_from_spotify = 0
        with open("songs.txt", 'r', encoding="UTF-8") as file:
            for line in file:
                number_of_missing_songs_from_spotify += 1
        if number_of_missing_songs_from_spotify == 0:
            return False
        return (True, still_not_found)




def add_music_to_playlist():
    bot = None
    try:
        bot = AddMusic()
        bot.login()
        bot.get_playlist_name()
        # bot.add_songs()
        for i in range(5):
            print("\n\n\nrestart\n\n\n")
            is_missing, still_not_found = bot.some_songs_was_missing()
            if is_missing == False:
                break
            bot.add_songs()
        if is_missing == True:
            print(f"This song maybe has not been added: {still_not_found}")
    except Exception:
        print("An error occurred while logging")
    finally:
        if bot and hasattr(bot, 'driver'):
            try:
                bot.driver.quit()
            except:
                pass
            try:
                bot.driver.quit = lambda: None
                bot.driver.service.process = None
            except:
                pass

if __name__ == "__main__":
    print("For the addition to be successful, you must have a single playlist in YouTube Music that is named the same as in Spotify")
    print("It may also happen that the program does not find certain songs")
    is_any_song = True
    # is_any_song = reader.read_songs("data.txt")
    if (is_any_song == False):
        print("You have no song in the playlist or you have some problem with file")
    else:
        add_music_to_playlist()

