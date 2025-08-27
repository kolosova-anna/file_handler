import asyncio
import aiofiles
from dataclasses import dataclass
import os

@dataclass
class FileInfo:
    path: str
    name: str
    count_lines: int = 0
    count_words: int = 0
    count_characters: int = 0

    def __str__(self):
        return (f"File: {self.name}\n"
                f"  Path: {self.path}\n"
                f"  Lines: {self.count_lines}\n"
                f"  Words: {self.count_words}\n"
                f"  Characters: {self.count_characters}\n")


async def handle_files(paths: list[str]) -> list[FileInfo | None]:
    tasks = [handle_file(path) for path in paths]
    results = await asyncio.gather(*tasks)
    return results


async def handle_file(path: str) -> FileInfo | None:
    try:
        file_name = os.path.basename(path)
        file_info = FileInfo(path, file_name)

        async with aiofiles.open(path, 'r', encoding='utf-8') as file:
            async for line in file:
                file_info.count_lines += 1
                file_info.count_words += len(line.split())
                file_info.count_characters += len(line)
        return file_info
    except FileNotFoundError:
        print(f'File not found: {path}')
        return None
          
    
def get_paths():
    paths = input("\nEnter file paths: ").strip()
    if not paths:
        print("No files specified!")
        return []
    file_paths = [path.strip() for path in paths.split(',')]
    return file_paths
    

async def main():
    print('\nWelcome! Specify the path to the files, divided by comma, in the format' \
        '"C:\\Users\\ADMIN\\Documents\\file1.txt, C:\\Users\\ADMIN\\Documents\\file2.txt"' \
        'The program will calculate and display the number of lines, words, and characters.')
    paths = get_paths()
    print('\nProcessing...')
    results = await handle_files(paths)
    for result in results:
        print(f"\n{result}")


if __name__ == "__main__":
    asyncio.run(main())