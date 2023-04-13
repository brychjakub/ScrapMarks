from playwright.sync_api import Playwright, sync_playwright
import getpass
import time

#password = getpass.getpass("Enter your password: ")




def main():
    with sync_playwright() as playwright:
        # Your code here
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
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

        #tlačítko "hodnocení"
        evaluation_selector = "#lid221"

        page.click(evaluation_selector)

        page.wait_for_load_state("networkidle")

        button_selector3 = "input[name='course_id']"
        page.click(button_selector3)

        page.wait_for_load_state("networkidle")


        #class= combobox_in
        #getting the ID of "aktivní kurzy"
        active_courses = page.locator('li:has-text("Ajk - 8.A 8.B")')
        element_id = active_courses.get_attribute('id')
        print(element_id)

        active_courses.click()

        page.wait_for_load_state("networkidle")

        #clicking 3 dots to rollout option to download excel file
        choices = page.locator('a[title="Volby"]')
        choices.click()

        page.wait_for_load_state("networkidle")
        
        link = page.locator('a[title="Exportovat do Excelu"]')
        href = link.get_attribute("href")

        link.click()

        # Wait for the download to start
        with page.expect_download() as download_info:
            download = download_info.value
        # Wait for the download process to complete
            download.save_as(".\hi.xlsx")       

        context.close()
        browser.close()


if __name__ == '__main__':
    main()
