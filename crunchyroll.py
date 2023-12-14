from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import csv

def get_chrome_options():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService,site-per-process")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-javascript")
    options.add_argument("--disable-automation")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')
    return options

driver = uc.Chrome(options=get_chrome_options())
driver.get("https://www.crunchyroll.com")
time.sleep(5)
genres_list = []  

def scrape_anime(url):
    anime_list = []

    driver.get(url)
    time.sleep(5)
 
    old_list = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(5)
        new_list = driver.execute_script("return document.body.scrollHeight")
        if new_list == old_list:
            break
        old_list = new_list
        time.sleep(5)

    anime_items = driver.find_elements(By.CLASS_NAME, 'browse-card')
    for item in anime_items:
        try:
            name_element = item.find_element(By.XPATH, ".//h4[@data-t='title']")
            name = name_element.text if name_element else ""
            dub_name_element = item.find_element(By.XPATH, ".//div[@data-t='meta-tags']")
            dub_name = dub_name_element.text if dub_name_element else ""
            anime_list.append((name, dub_name))
        except:
            continue

    return anime_list

genres_section = driver.find_element(By.CLASS_NAME, 'genres-section')
for anchor in genres_section.find_elements(By.TAG_NAME, 'a'):
    genres_list.append(anchor.get_attribute('href'))

for genres_url in genres_list:
    driver.get(genres_url)
    time.sleep(5)

    genre_parts = genres_url.split('/')
    genre_name = genre_parts[-1]

    csv_filename = f"{genre_name}.csv"
    csv_headers = ['Name', 'Dub Name']

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_headers)

        new_anime_data = scrape_anime(genres_url + '/new')
        for name, dub_name in new_anime_data:
            writer.writerow([name, dub_name])

        popular_anime_data = scrape_anime(genres_url + '/popular')
        for name, dub_name in popular_anime_data:
            writer.writerow([name, dub_name])

driver.quit()