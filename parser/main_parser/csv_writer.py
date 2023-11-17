import aiofiles
import aiocsv

class CsvWriter:
    def __init__(self, writer):
        self.writer = writer


    async def write_lines(self, lines):
        async with aiofiles.open('results.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = aiocsv.AsyncWriter(file, delimiter=';')
            await writer.writerows(lines)