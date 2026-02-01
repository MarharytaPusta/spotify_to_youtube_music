import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

if __name__ == "__main__":

    with open("data.txt") as f:
        for i, line in enumerate(f):
            if i == 0:
                playlist = line.strip()

    driver = webdriver.Chrome()
    driver.get(playlist)
    time.sleep(5)

    print("gfg")
    print("gfg")
#TODO перевірка чи прокручено сторінку до низу. Чому навіть при ручному прокруті не всі пісні бере?
    element = driver.find_element(By.XPATH, '//*[@id="main-view"]/div/div[2]/div[3]/div/div')

    driver.execute_script("arguments[0].scrollIntoView();", element)

    names_of_songs = driver.find_elements(By.CSS_SELECTOR, '.main-view-container__scroll-node-child div[role="grid"] [role="row"] [data-testid="tracklist-row"][role="presentation"] [role="gridcell"] [data-testid="internal-track-link"] [data-encore-id="text"]')
    print(len(names_of_songs))
    names_of_songs = [names.text for names in names_of_songs]
    print(len(names_of_songs))

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
    print(len(names_of_songs))
    names_of_songs = names_of_songs[:number_of_songs]
    print(len(names_of_songs))
    authors = authors_find[:number_of_songs]
    print(len(authors))

    with open("songs.txt", "w", encoding="UTF-8") as f:
        for i in range(len(names_of_songs) - 1):
            f.write(f"{names_of_songs[i]} — {authors_find[i]}\n")

    driver.quit()




