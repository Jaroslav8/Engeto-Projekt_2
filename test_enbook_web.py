import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture()
def browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=1000)
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

# The object of testing is the website www.enbook.sk

# 1st. test - verify if searchbar on the website works

def test_enbook_search(page):
    page.goto("https://www.enbook.sk/")

    page.wait_for_selector('input[id="search"]', timeout=10000)  
    page.fill('input[id="search"]', "The Colosseum")
    page.press('input[id="search"]', "Enter")

    page.wait_for_selector('a[data-role="result-link"]', timeout=10000)  
    search_results = page.query_selector_all('a[data-role="result-link"]')  
    
    assert len(search_results) > 0, "No search results found"
    print(f"Number of search results: {len(search_results)}")
       

# 2nd. test - verify if a try to log into account with incorrect e-mail and password failed

def test_log_in(page):
    page.goto("https://www.enbook.sk")
    
    page.wait_for_selector('div[data-block="dropdownmenu"]', timeout=5000)
    page.query_selector('div[data-block="dropdownmenu"]').click()

    page.wait_for_selector('input[id="email"]', timeout=5000)
    page.fill('input[id="email"]', "nic@nic.sk")
    page.fill('input[id="pass"]', "heslo")
    page.query_selector("button#send2").click()

    page.wait_for_selector('div[role="alert"]', timeout=5000)
    warning_notice = page.locator('div[role="alert"]')
    assert warning_notice.inner_text() == "Prihlásenie do konta bolo nesprávne alebo je vaše konto dočasne deaktivované. Počkajte a skúste to neskôr."


# 3rd. test - verify if a book is added into the shopping cart

def test_add_to_chart(page):
    page.goto("https://www.enbook.sk/9781728296210")

    page.wait_for_selector("#product-addtocart-button", timeout=5000)
    page.query_selector("#product-addtocart-button").click()
    page.get_by_role("button", name="Zobraziť košík").click()
    
    page.wait_for_selector('input[class="input-text qty activated"]', timeout=5000)
    amount_input = page.locator('input[class="input-text qty activated"]')
    item_in_cart = page.locator('div[class="product-item-details"]')
    
    assert item_in_cart.inner_text() == "The Teacher"
    assert amount_input.input_value() == "1"

