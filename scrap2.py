from playwright.sync_api import sync_playwright
from getpass_asterisk.getpass_asterisk import getpass_asterisk
import os

email = input("Enter your email: ")
password = getpass_asterisk("Enter your password: ")

def download_excel(page):
    choices_selector = 'a[title="Volby"]'
    excel_export_selector = 'a[title="Exportovat do Excelu"]'

    page.wait_for_selector(choices_selector).click()
    page.wait_for_selector(excel_export_selector).click()


def make_dir():
    newpath = r'.\{}'.format(email)
    if not os.path.exists(newpath):
        os.makedirs(newpath)



def choose_course(page):
    button_selector3 = "input[name='course_id']"
    page.wait_for_selector(button_selector3).click()

    first_id = page.locator('li:has-text("-- AKTIVNÍ KURZY ---")')
    last_id = page.locator('li:has-text("-- SUPLOVANÉ A NEZAPSANÉ KURZY --")')

    start = int(''.join(filter(str.isdigit, first_id.get_attribute('id'))))
    end = int(''.join(filter(str.isdigit, last_id.get_attribute('id'))))

    for i in range(start + 1, end+1):
        id = "cbr_" + str(i)
        print(id)

        button_selector3 = "input[name='course_id']"
        page.wait_for_selector(button_selector3).click()

        page.wait_for_load_state("networkidle")
        
        course = page.locator(f'li[id="{id}"]')
        course.click()
        id2 = "cbr_" + str(i-1)
        if id2 != "cbr_1":           
            name = page.locator(f'li[id="{id2}"]').inner_text()
            make_dir()
            download_excel(page)
            with page.expect_download() as download_info:
                download = download_info.value
                download.save_as(f".\{email}\{name}.xlsx") 
        else:
            continue

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://cmczs-login.edookit.net/")
        button_selector = "#plus4ULoginButton"
        page.click(button_selector)
        page.wait_for_load_state("networkidle")
        button = page.query_selector('button:has-text("Microsoft")')
        button.click()

        page.wait_for_load_state("networkidle")

        email_selector = "input[type='email']"
        page.fill(email_selector, f"{email}") 

        page.wait_for_load_state("networkidle")

        sign_in_button_selector = "input[type='submit']"
        page.click(sign_in_button_selector)

        page.wait_for_load_state("networkidle")

        password_selector = "input[type='password']"
        page.fill(password_selector, f"{password}")
        page.click(sign_in_button_selector)

        button_selector2 = "input[id='idBtn_Back']"
        page.wait_for_selector(button_selector2).click()

        page.wait_for_load_state("networkidle")

        evaluation_selector = "#lid221"
        page.click(evaluation_selector)
   
        choose_course(page)

        context.close()
        browser.close()


if __name__ == '__main__':
    main()
    
