import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://open.spotify.com/playlist/5qcxf9em7LHR8igrX5zA3c")
time.sleep(5)

names_of_songs = driver.find_elements(By.CSS_SELECTOR, '.main-view-container__scroll-node-child div[role="grid"] div[role="row"] div[data-testid="tracklist-row"][role="presentation"] div[role="gridcell"] a[data-testid="internal-track-link"] div[data-encore-id="text"]')
names_of_songs = [names.text for names in names_of_songs]

full_songs_name = driver.find_elements(By.CSS_SELECTOR, '.main-view-container__scroll-node-child [role="grid"] [role="row"] [data-testid="tracklist-row"][role="presentation"] [role="gridcell"] button[aria-label]')
authors_find = []
for name in full_songs_name:
    authors_find.append(name.get_attribute("aria-label"))
authors_find = authors_find[0::3]
for i in range(len(authors_find) - 1):
    index = authors_find[i].find(names_of_songs[i])
    authors_find[i] = authors_find[i][index:]
for i in range(len(authors_find) - 1):
    index = len(names_of_songs[i]) + 1
    authors_find[i] = authors_find[i][index:]
    index = authors_find[i].find(' ') + 1
    authors_find[i] = authors_find[i][index:]

number_of_songs = driver.find_element(By.CSS_SELECTOR, '.main-view-container__scroll-node-child [data-testid="playlist-page"] [role="grid"][aria-rowcount]')
number_of_songs = number_of_songs.get_attribute("aria-rowcount")
number_of_songs = int(number_of_songs) - 1
print(number_of_songs)

names_of_songs = names_of_songs[:number_of_songs]
authors = authors_find[:number_of_songs]

with open("songs.txt", "w", encoding="UTF-8") as f:
    for i in range(len(names_of_songs) - 1):
        f.write(f"{names_of_songs[i]} — {authors_find[i]}\n")

driver.quit()




