import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time
import reader

if __name__ == "__main__":
    driver = uc.Chrome(version_main=144)

    driver.get("https://music.youtube.com/")
    time.sleep(2)

    signin = driver.find_element(By.CSS_SELECTOR, ".sign-in-link")
    driver.execute_script("arguments[0].click()", signin)
    input("Коли успішно увійдете і сторінка завантажиться, натисніть ENTER")

    # elem = driver.find_element(By.CSS_SELECTOR, '#sections #buttons [class="style-scope ytmusic-guide-section-renderer"] button[class="yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--enable-backdrop-filter-experiment"]')
    # driver.execute_script("arguments[0].click()", elem)
    # time.sleep(2)
    with open("songs.txt", "r", encoding="UTF-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                playlist_name = line.strip()
    print(f".......{playlist_name}...........")
    # elem = driver.find_element(By.CSS_SELECTOR, '#title-input input')
    # elem.click()
    # elem.send_keys(playlist_name)
    # elem = driver.find_element(By.CSS_SELECTOR, '[class="actions style-scope ytmusic-playlist-form"] [class="style-scope ytmusic-playlist-form"] button[class="yt-spec-button-shape-next yt-spec-button-shape-next--filled yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--enable-backdrop-filter-experiment"]')
    # driver.execute_script("arguments[0].click()", elem)



    #finding a music
    song = ''
    with open("songs.txt", "r", encoding="UTF-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            song = line.strip()
            # search
            elem = driver.find_element(By.CSS_SELECTOR, '[class="search-box style-scope ytmusic-search-box"] input#input')
            driver.execute_script("arguments[0].click()", elem)
            elem.send_keys(song)
            elem.send_keys(Keys.ENTER)
            time.sleep(1)
            # 3 colon
            elem = driver.find_element(By.CSS_SELECTOR, 'ytmusic-shelf-renderer ytmusic-responsive-list-item-renderer .menu button')
            driver.execute_script("arguments[0].click()", elem)
            time.sleep(1)
            # add to playlist button
            elem = driver.find_element(By.XPATH, '/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-iron-dropdown/div/ytmusic-menu-popup-renderer/tp-yt-paper-listbox/ytmusic-menu-navigation-item-renderer[2]/a/yt-formatted-string')
            driver.execute_script("arguments[0].click()", elem)
            time.sleep(1)
            # плейлісти
            playlists = driver.find_elements(By.CSS_SELECTOR, '[class="scrollable-content scroller style-scope ytmusic-add-to-playlist-renderer"] #playlists ytmusic-playlist-add-to-option-renderer button #title')

            target_playlist = driver.find_element(By.XPATH, f"//ytmusic-playlist-add-to-option-renderer//yt-formatted-string[@title='{playlist_name}' or text()='{playlist_name}']")
            # Клікаємо на знайдений плейліст
            driver.execute_script("arguments[0].click()", target_playlist)
            print("Ура! Пісню додано.")
            # for i in range(len(playlists)):
            #     playlists[i] = playlists[i].text
            # print(f"names: \n{playlists}")
            # if playlist_name not in playlists:
            #     print(f"Wops, somthing went wrong: {playlist_name} not in")
            #     print(f"names: {playlists}")
            # else:
            #     print("start")
            #     child_number_of_playlist = playlists.index(playlist_name) + 1
            #     child_number_of_playlist = int(child_number_of_playlist)
            #     # concrete playlist
            #     elem = driver.find_element(By.CSS_SELECTOR, f'[class="scrollable-content scroller style-scope ytmusic-add-to-playlist-renderer"] #playlists:nth-child({child_number_of_playlist}) button[class="style-scope ytmusic-playlist-add-to-option-renderer"]')
            #     driver.execute_script("arguments[0].click()", elem)
            #     print("uhu, 1 more song")
            # print("dcds")
            # clear button
            elem = driver.find_element(By.ID, 'clear-button')
            driver.execute_script("arguments[0].click()", elem)
            time.sleep(0.5)
"""
#id
.class

[href='/favourites']"
[type='submit']

[type='text'][name='email']
a#offers[href='/offers']

[class^='Navbar_logo_']           щоб задати початок назви класу
[class$='26S5Y']                  щоб задати кінець назви класу
[class*='logo_']                  щоб задати довільну частину назви класу

button.buttonКлас +-
.buttonКлас +-
[name='button1'] +-
"""
