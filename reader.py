import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


class SporifyWriter:
    def __init__(self, file_name):
        self.driver = webdriver.Chrome()
        self.playlist_url = ""
        self.songs = set()
        self.file_name = file_name

    def get_playlist_url(self):
            with open(self.file_name) as file:
                for i, line in enumerate(file):
                    if i == 0:
                        self.playlist_url = line.strip()

    def open_playlist(self):
        self.driver.get(self.playlist_url)
        time.sleep(5)

    def read_songs(self):
        previous_count = 0
        stuck_counter = 0
        no_song_case = 0
        while True:
            try:
                elem = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="playlist-tracklist"]')
                rows = elem.find_elements(By.CSS_SELECTOR, '[data-testid="tracklist-row"]')
            except:
                no_song_case += 1
                if no_song_case > 7:
                    return
                time.sleep(1)
                continue
            for row in rows:
                try:
                    title = row.find_element(By.CSS_SELECTOR, '[data-testid="internal-track-link"] div').text
                    button = row.find_element(By.CSS_SELECTOR, 'button[aria-label]')
                    aria_text = button.get_attribute("aria-label")
                    index = aria_text.find(title)
                    if index != -1:
                        aria_text = aria_text[index:]
                    index = len(title) + 1
                    aria_text = aria_text[index:]
                    index = aria_text.find(' ') + 1
                    artist = aria_text[index:]
                    full = f"{title} — {artist}"
                    self.songs.add(full)
                except Exception:
                    continue
            current_count = len(self.songs)
            if current_count == previous_count:
                stuck_counter += 1
                if stuck_counter >= 8:
                    break
            else:
                stuck_counter = 0
                previous_count = current_count

            try:
                fresh_rows = elem.find_elements(By.CSS_SELECTOR, '[data-testid="tracklist-row"]')
                if fresh_rows:
                    last_row = fresh_rows[-1]
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                                               last_row)
                else:
                    self.driver.execute_script("window.scrollBy(0, 500);")
            except:
                self.driver.execute_script("window.scrollBy(0, 600);")

            time.sleep(1)

    def save_to_file(self):
        try:
            playlist_name = self.driver.find_element(By.CSS_SELECTOR,
                                                     '.main-view-container__scroll-node-child [data-testid="playlist-page"] [role="grid"][aria-label]')
            playlist_name = playlist_name.get_attribute("aria-label")
        except:
            playlist_name = "unknown playlist"
        with open("songs.txt", "w", encoding="UTF-8") as f:
            f.write(f"{playlist_name}\n")
            for song in self.songs:
                f.write(f"{song}\n")

    def is_any_song(self):
        if len(self.songs) > 0:
            return True
        else:
            return False

    def end(self):
        self.driver.quit()


def read_songs(file_name):
    reader = SporifyWriter(file_name)
    try:
        reader.get_playlist_url()
    except:
        print("Something wrong with data file")
        return False
    reader.open_playlist()
    reader.read_songs()
    reader.save_to_file()
    reader.end()
    is_any_song_there = reader.is_any_song()
    return is_any_song_there