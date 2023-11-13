from playwright.async_api._generated import Page
from playwright._impl._api_types import Error

from capmonstercloudclient import ClientOptions, CapMonsterClient
from capmonstercloudclient.requests import ImageToTextRequest
from capmonstercloudclient.exceptions import GetTaskError
import asyncio
import aiofiles


async def captcha(config, page: Page, number) :
    img_name = f'img{number}.png'

    async def sender_solve(cap_monster_client, path=img_name):

        # print('2) Изображение отправленно для разгадывания:')
        async with aiofiles.open(f'captcha_images/{path}', 'rb') as f:
            image_bytes = await f.read()
        imr = ImageToTextRequest(image_bytes=image_bytes, threshold=50, case=True, numeric=0, math=False)

        result = await cap_monster_client.solve_captcha(imr)
#         print('3) От API пришёл ответ: ', result['text'])
        return result['text']

    client_options = ClientOptions(api_key=config.capmonster_token)
    cap_monster_client = CapMonsterClient(options=client_options)

    while True:
        text = ''
        page_content = await page.content()
        flag = False
        if 'Для продолжения необходимо пройти дополнительную проверку' in page_content:
            flag = True

        if flag == False:
            # print(f"Капча успешно решена. CapMonster")
            return True

        else:
            await page.locator('#kcaptchaForm img').screenshot(path=f'captcha_images/img{number}.png', timeout=240000)
            # print('1) Скриншот области успешно сделан')
            try:
                text = await sender_solve(cap_monster_client)
            except (GetTaskError, asyncio.TimeoutError):
                await page.reload(timeout=120000)
            await page.fill('.text-input', text)
            await page.press('.button-normal', 'Enter')
            await asyncio.sleep(1)
            if 'Для продолжения необходимо пройти дополнительную проверку' in page_content:
                flag = True
                # print('Повторяю попытку')