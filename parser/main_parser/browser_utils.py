import asyncio

from playwright.async_api import Page

from .captcha import captcha


async def _open_page(page, config, number, url, timeout):
    goto_flag = False
    while not goto_flag:
        try:
            await page.goto(url, timeout=timeout)
            checker = await _goto_checker(page, config, number)
            if checker is None:
                return False
            goto_flag = checker
        except Exception as e:
            goto_flag = False
    return goto_flag

async def _goto_checker(page: Page, config, number):
    page_content = await page.content()
    while 'временно недоступен. Обратитесь к данной странице позже.' in page_content:
        await asyncio.sleep(2)
        await page.reload()
        await asyncio.sleep(2)
        page_content = await page.content()
    await _solve_captcha(config, page, number)

    check_id = await page.locator('#search_results').text_content(timeout=120000)
    if 'В настоящий момент сервер, на котором расположен модуль сопряжения с БД «АМИРС», недоступен. Попробуйте обратиться к данной странице позже.' == check_id.strip():
        return False

    if (f'На {page.url[-10:]} слушаний дел не назначено.' == check_id.strip() or
            'К сожалению, запрашиваемая вами страница не найдена. Возможно, она была удалена или перемещена.' in page_content):
        return None
    return True

async def _solve_captcha(config, page, number):
    captcha_flag = False
    while not captcha_flag:
        try:
            captcha_flag = await captcha(config, page, number)
        except Exception as e:
            captcha_flag = False

async def page_goto_validator(page: Page, config, url, number, timeout=240000):
    checker = await _open_page(page, config, number, url, timeout)
    return checker