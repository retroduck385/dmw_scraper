from selenium import webdriver

def main():
    driver = webdriver.Chrome()
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")

if __name__ ==  '__main__':
    main()