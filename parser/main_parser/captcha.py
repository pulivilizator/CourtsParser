import base64
import json

from playwright.async_api._generated import Page

import asyncio
import aiofiles
import aiohttp


# async def captcha(config, page: Page, number):
#     img_name = f'img{number}.png'
#
#     async def sender_solve(cap_monster_client, path=img_name):
#         result = None
#         print('2) Изображение отправленно для разгадывания:')
#         async with aiofiles.open(f'captcha_images/{path}', 'rb') as f:
#             image_bytes = await f.read()
#         print(1)
#         imr = ImageToTextRequest(image_bytes=image_bytes, threshold=50, case=True, numeric=0, math=False)
#         print(2)
#         while not result:
#             try:
#                 result = await cap_monster_client.solve_captcha(imr)
#             except asyncio.TimeoutError:
#                 pass
#         print(3)
#         print('3) От API пришёл ответ: ', result['text'])
#         return result['text']
#
#     client_options = ClientOptions(api_key=config.capmonster_token)
#     cap_monster_client = CapMonsterClient(options=client_options)
#
#     while True:
#         page_content = await page.content()
#         flag = False
#         if 'Для продолжения необходимо пройти дополнительную проверку' in page_content:
#             flag = True
#
#         if flag == False:
#             # print(f"Капча успешно решена. CapMonster")
#             return True
#
#         else:
#             await page.locator('#kcaptchaForm img').screenshot(path=f'captcha_images/img{number}.png', timeout=240000)
#             print('1) Скриншот области успешно сделан')
#             # try:
#             #     text = await sender_solve(cap_monster_client)
#             # except (GetTaskError, asyncio.TimeoutError) as e:
#             #     print(e, 'ERROR')
#             #     await page.reload(timeout=60000)
#             text = await sender_solve(cap_monster_client)
#             await page.fill('.text-input', text)
#             await page.press('.button-normal', 'Enter', timeout=240000)
#             await asyncio.sleep(1)
#             if 'Для продолжения необходимо пройти дополнительную проверку' in page_content:
#                 flag = True
#                 print('Повторяю попытку')


async def captcha(config, page: Page, number, session: aiohttp.ClientSession):
    img_name = f'img{number}.png'

    async def sender_solve(path=img_name):
        async with aiofiles.open(f'captcha_images/{path}', 'rb') as f:
            image_bytes = await f.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        create_task_data = {
            "clientKey": config.capmonster_token,
            "task":
                {
                    "type": "ImageToTextTask",
                    "body": image_base64
                }
        }

        r = await session.post(url='https://api.capmonster.cloud/createTask', json=create_task_data)
        r_text = await r.text()
        r_dict = json.loads(r_text)
        if r_dict['errorId']:
            print(f'CAPMOSTER ERROR: {r_dict["errorCode"]}: {r_dict["errorDescription"]}')
            return ''
        get_task_data = {
            "clientKey": config.capmonster_token,
            "taskId": r_dict["taskId"]
        }
        while True:
            captcha_resp = await session.post(url='https://api.capmonster.cloud/getTaskResult', json=get_task_data)
            captcha_text = await captcha_resp.text()
            captcha_dict = json.loads(captcha_text)
            if captcha_dict['status'] == 'ready':
                return captcha_dict['solution']['text']
            await asyncio.sleep(1)


    while True:
        page_content = await page.content()
        flag = False
        if 'Для продолжения необходимо пройти дополнительную проверку' in page_content:
            flag = True

        if flag == False:
            # print(f"Капча успешно решена. CapMonster")
            return True

        else:
            await page.locator('#kcaptchaForm img').screenshot(path=f'captcha_images/img{number}.png', timeout=120000)
            text = await sender_solve()
            await page.fill('.text-input', text)
            await page.press('.button-normal', 'Enter', timeout=120000)
            await asyncio.sleep(1)
            if 'Для продолжения необходимо пройти дополнительную проверку' in page_content:
                flag = True
                # print('Повторяю попытку')