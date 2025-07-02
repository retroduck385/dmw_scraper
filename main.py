from selenium import webdriver

def main():
    driver = webdriver.Chrome()
    driver.get("https://www.w3schools.com/python/python_virtualenv.asp")

if __name__ ==  '__main__':
    main()