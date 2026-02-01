import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import reader

if __name__ == "__main__":
    driver = uc.Chrome(version_main=144)

    driver.get("https://music.youtube.com/")
    time.sleep(2)
    signin = driver.find_element(By.CSS_SELECTOR, ".sign-in-link")
    driver.execute_script("arguments[0].click()", signin)
    # email = ''
    # password = ''
    # with open("data.txt") as f:
    #     for i, line in enumerate(f):
    #         if i == 1:
    #             email = line.strip()
    #         if i == 2:
    #             password = line.strip()
    input("Коли успішно увійдете і сторінка завантажиться, натисніть ENTER")
    # elem = driver.find_element(By.CSS_SELECTOR, '[type="email"]')
    # elem.send_keys(email)
    # elem = driver.find_element(By.ID, 'identifierNext')
    # driver.execute_script("arguments[0].click()", elem)
    # time.sleep(2)
    # # TODO: Selenium Google Login Block
    # elem = driver.find_element(By.CSS_SELECTOR, '[type="password"]')
    # elem.send_keys(password)
    # elem = driver.find_element(By.ID, 'identifierNext')
    # driver.execute_script("arguments[0].click()", elem)
    # time.sleep(2)

    elem = driver.find_element(By.CSS_SELECTOR, '#sections #buttons [class="style-scope ytmusic-guide-section-renderer"] button[class="yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--enable-backdrop-filter-experiment"]')
    driver.execute_script("arguments[0].click()", elem)
    time.sleep(2)
    elem = driver.find_element(By.CSS_SELECTOR, '#title-input input')
    playlist_name = "idk"
    elem.click()
    elem.send_keys(playlist_name)
    elem = driver.find_element(By.CSS_SELECTOR, '[class="actions style-scope ytmusic-playlist-form"] [class="style-scope ytmusic-playlist-form"] button[class="yt-spec-button-shape-next yt-spec-button-shape-next--filled yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--enable-backdrop-filter-experiment"]')
    driver.execute_script("arguments[0].click()", elem)


print("ddcd")
print("ddcd")




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
