from playwright.sync_api import Playwright, sync_playwright

with sync_playwright() as playwright:
    # Your code here
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://cmczs-login.edookit.net/")
    button_selector = "#plus4ULoginButton"
    page.click(button_selector)
    page.wait_for_load_state("networkidle")
    button = page.query_selector('button:has-text("Microsoft")')
    button.click()

# Wait for the page to fully load
    page.wait_for_load_state("networkidle")

    email_selector = "input[type='email']"
    page.fill(email_selector, "brych@cmczs.cz")


    page.wait_for_load_state("networkidle")


    sign_in_button_selector = "input[type='submit']"
    page.click(sign_in_button_selector)

    page.wait_for_load_state("networkidle")

    password_selector = "input[type='password']"
    page.fill(password_selector, "Iphone4S")

    sign_in_button_selector = "input[type='submit']"
    page.click(sign_in_button_selector)

    page.wait_for_load_state("networkidle")

    button_selector2 = "input[id='idBtn_Back']"
    page.click(button_selector2)

    page.wait_for_load_state("networkidle")

    evaluation_selector = "#lid221"

    page.click(evaluation_selector)

    page.wait_for_load_state("networkidle")

    button_selector3 = "input[name='course_id']"
    page.click(button_selector3)

    page.wait_for_load_state("networkidle")

    first_id = page.query_selector('button:has-text("Microsoft")')

    element = page.locator('.r_selected')
    text = element.inner_text()
    print(text)

    page.screenshot(path="example.png")
    browser.close()
    