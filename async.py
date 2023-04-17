import asyncio
import os
import time

from getpass_asterisk.getpass_asterisk import getpass_asterisk
from playwright.async_api import async_playwright

email = input("Enter your email: ")


async def download_excel(page):
    choices_selector = 'a[title="Volby"]'
    excel_export_selector = 'a[title="Exportovat do Excelu"]'

    await page.click(choices_selector)
    await page.click(excel_export_selector)


def make_dir(email):
    newpath = r".\{}".format(email)
    if not os.path.exists(newpath):
        os.makedirs(newpath)


async def choose_course(page):
    button_selector3 = "input[name='course_id']"
    await page.click(button_selector3)

    first_id = page.locator('li:has-text("-- AKTIVNÍ KURZY ---")')
    last_id = page.locator('li:has-text("-- SUPLOVANÉ A NEZAPSANÉ KURZY --")')

    start = int("".join(filter(str.isdigit, await first_id.get_attribute("id"))))
    end = int("".join(filter(str.isdigit, await last_id.get_attribute("id"))))

    for i in range(start + 1, end + 1):
        id = "cbr_" + str(i)
        print(id)

        button_selector3 = "input[name='course_id']"
        await page.click(button_selector3)

        await page.wait_for_load_state("networkidle")

        course = page.locator(f'li[id="{id}"]')
        await course.click()
        id2 = "cbr_" + str(i - 1)
        if id2 != "cbr_1":
            name = await page.locator(f'li[id="{id2}"]').inner_text()
            make_dir(email)
            await download_excel(page)
            async with page.expect_download() as download_info:
                download = await download_info.value
                await download.save_as(f".\{email}\{name}.xlsx")
        else:
            continue


async def main():
    password = getpass_asterisk("Enter your password: ")

    start_time = time.time()
    print("start")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://cmczs-login.edookit.net/")
        button_selector = "#plus4ULoginButton"
        await page.click(button_selector)
        await page.wait_for_load_state("networkidle")
        button = await page.query_selector('button:has-text("Microsoft")')
        await button.click()

        await page.wait_for_load_state("networkidle")

        email_selector = "input[type='email']"
        await page.fill(email_selector, f"{email}")

        await page.wait_for_load_state("networkidle")

        sign_in_button_selector = "input[type='submit']"
        await page.click(sign_in_button_selector)

        await page.wait_for_load_state("networkidle")

        password_selector = "input[type='password']"
        await page.fill(password_selector, f"{password}")
        await page.click(sign_in_button_selector)

        button_selector2 = "input[id='idBtn_Back']"
        await page.click(button_selector2)

        evaluation_selector = "#lid221"
        await page.click(evaluation_selector)

        await choose_course(page)

        await context.close()
        await browser.close()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

#awating the main function
asyncio.run(main())
