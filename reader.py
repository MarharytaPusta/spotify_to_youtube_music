
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

if __name__ == "__main__":
    with open("data.txt") as f:
        for i, line in enumerate(f):
            if i == 0:
                playlist = line.strip()
                print(playlist)

    driver = webdriver.Chrome()
    driver.get(playlist)
    time.sleep(5)

    songs = set()
    previous_count = 0
    stuck_counter = 0

    while True:
        try:
            #плейліст
            elem = driver.find_element(By.CSS_SELECTOR, '[data-testid="playlist-tracklist"]')
            #пісні всередині
            rows = elem.find_elements(By.CSS_SELECTOR, '[data-testid="tracklist-row"]')
        except:
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
                songs.add(full)
            except Exception:
                continue

        current_count = len(songs)
        print(current_count)
        if current_count == previous_count:
            stuck_counter += 1
            if stuck_counter >= 8:
                print("all")
                break
        else:
            stuck_counter = 0
            previous_count = current_count

        try:
            fresh_rows = elem.find_elements(By.CSS_SELECTOR, '[data-testid="tracklist-row"]')
            if fresh_rows:
                last_row = fresh_rows[-1]
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", last_row)
            else:
                driver.execute_script("window.scrollBy(0, 500);")
        except:
            driver.execute_script("window.scrollBy(0, 600);")

        time.sleep(1)


    playlist_name = driver.find_element(By.CSS_SELECTOR,
                                        '.main-view-container__scroll-node-child [data-testid="playlist-page"] [role="grid"][aria-label]')
    playlist_name = playlist_name.get_attribute("aria-label")

    with open("songs.txt", "w", encoding="UTF-8") as f:
        f.write(f"{playlist_name}\n")
        for song in songs:
            f.write(f"{song}\n")

    driver.quit()