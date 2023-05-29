from random import randint
from selenium.webdriver.common.by import By
from re import sub
from statistics import median
from selenium import webdriver
from random import randint

def get_most_frequent_elements(lst, limit=15):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    most_frequent = dict(sorted_counts[:limit])
    return most_frequent

def remove_words_from_string(text, words_to_remove):
    return [word for word in text if word not in words_to_remove]

def scrap(keywords):
    options = webdriver.ChromeOptions() 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    
    driver = webdriver.Chrome(options=options) 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    useragentarray = [ 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36", 
    ] 
    responses = []
    for keyword in keywords:
        try:
            driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragentarray[randint(0,1)]}) 
            driver.execute_script("return navigator.userAgent;")
            driver.get(f'https://www.fiverr.com/search/gigs?query={keyword}')
            total_services = sub('[^\d\.]', '', driver.find_element(By.CSS_SELECTOR, 'div.number-of-results').get_attribute('textContent'))
            ratings = [float(sub('[^\d\.]','',i.get_attribute('textContent'))) for i in driver.find_elements(By.CSS_SELECTOR, '.rating-score')]
            starting_prices = [float(sub('[^\d\.]','',i.get_attribute('textContent'))) for i in driver.find_elements(By.XPATH, "//span[contains(text(), 'From')]")]
            total_reviews = [float(sub('[^\d\.]','',i.get_attribute('textContent'))) for i in driver.find_elements(By.CSS_SELECTOR, '.rating-count-number')]
            primary_keywords = list(filter(lambda a : len(a) > 2, ' '.join([i.get_attribute('textContent').replace(',', ' ').lower() for i in driver.find_elements(By.CSS_SELECTOR, 'h3.text-normal')]).split(' ')))
            driver.get(f'https://www.fiverr.com/search/gigs?query={keyword}&source=toggle_filters&ref=is_seller_online%3Atrue')
            online_services = sub('[^\d\.]', '', driver.find_element(By.CSS_SELECTOR, 'div.number-of-results').get_attribute('textContent'))

            response = {
                'Keyword' : keyword,
                'Total Services' : total_services,
                'Online Servies' : online_services,
                'Total Ratings on First Page' : sum(total_reviews),
                'Average Rating' : sum(ratings)/len(ratings),
                'Average Starting Price' : sum(starting_prices)/len(starting_prices),
                'Median Starting Price' : median(starting_prices),
                'Related Keywords' : get_most_frequent_elements(remove_words_from_string(primary_keywords, ['i','will', 'do', 'your', 'you', 'and', 'for', 'from', 'what', 'create', 'using', 'with',]))
            }

            responses.append(response)
        except:
            print("Error Scrap")
            pass
    print(responses)
    return(responses)
