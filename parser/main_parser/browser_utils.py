import asyncio
import random
import logging

from fake_useragent import UserAgent
from playwright.async_api import Page

from .captcha import captcha


async def _open_page(page, config, number, url, timeout, captcha_session):
    goto_flag = False
    while not goto_flag:
        try:
            await page.goto(url, timeout=timeout)
            await asyncio.sleep(3)
            checker = await _goto_checker(page, config, number, captcha_session)
            if checker is None:
                return False
            goto_flag = checker
        except Exception as e:
            print(e)
            print(type(e))
            print('Goto error')
            logging.warning(f'OPEN_PAGE::ERROR_TYPE:{type(e)}::ERROR_DESCRIPTION:{e}')
            if str(e) == 'Target page, context or browser has been closed':
                return {'error': 'page closed'}
            goto_flag = False
    return goto_flag

async def _goto_checker(page: Page, config, number, captcha_session):
    page_content = await page.content()
    if 'К сожалению, запрашиваемая вами страница не найдена' in page_content:
        return None
    while 'временно недоступен. Обратитесь к данной странице позже.' in page_content:
        await asyncio.sleep(2)
        await page.reload()
        await asyncio.sleep(2)
        page_content = await page.content()
    captcha = await _solve_captcha(config, page, number, captcha_session)
    if not captcha:
        return False
    try:
        check_id = await page.locator('#search_results').text_content(timeout=120000)
    except Exception as e:
        return False
    if 'В настоящий момент сервер, на котором расположен модуль сопряжения с БД «АМИРС», недоступен. Попробуйте обратиться к данной странице позже.' == check_id.strip():
        return None

    if f'На {page.url[-10:]} слушаний дел не назначено.' == check_id.strip():
        return None
    return True

async def _solve_captcha(config, page, number, captcha_session):
    captcha_flag = False
    while not captcha_flag:
        # try:
        #     captcha_flag = await captcha(config, page, number)
        # except Exception as e:
        #     print(e)
        #     print(2)
        #     return False
        captcha_flag = await captcha(config, page, number, captcha_session)
    return True

async def page_goto_validator(page: Page, config, url, number, captcha_session, timeout=50000):
    checker = await _open_page(page, config, number, url, timeout, captcha_session)
    # while isinstance(checker, dict):
    #     await context.close()
    #     context = await browser.new_context(user_agent=UserAgent().random)
    #     page = await context.new_page()
    #     checker = await _open_page(page, config, number, url, timeout, captcha_session)
    return checker