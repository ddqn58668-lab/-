import os
import re

CONTENT_DIR = "content"

def markdown_files(root_directory):
    for directory, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.lower().endswith(".md"):
                yield os.path.join(directory, filename)

def paragraphs(text):
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
    return [paragraph.strip() for paragraph in re.split(r"\n\s*\n", normalized_text) if paragraph.strip()]

def search_file(path, pattern):
    try:
        with open(path, "r", encoding="utf-8") as note_file:
            content = note_file.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="utf-8-sig") as note_file:
            content = note_file.read()
    except OSError as error:
        print("无法读取文件：" + path + "（" + str(error) + "）")
        return []

    return [paragraph for paragraph in paragraphs(content) if pattern.search(paragraph)]

def main():
    if not os.path.isdir(CONTENT_DIR):
        print("未找到 content/ 目录。")
        return

    keyword = input("请输入搜索关键词或正则表达式：").strip()
    if not keyword:
        print("关键词不能为空。")
        return

    try:
        pattern = re.compile(keyword, re.IGNORECASE)
    except re.error as error:
        print("正则表达式无效：" + str(error))
        return

    matched_files = 0
    matched_paragraphs = 0

    for path in markdown_files(CONTENT_DIR):
        matches = search_file(path, pattern)
        if not matches:
            continue

        matched_files += 1
        relative_path = os.path.relpath(path, CONTENT_DIR)
        print("\n文件：" + relative_path)
        print("-" * 60)

        for number, paragraph in enumerate(matches, start=1):
            matched_paragraphs += 1
            print("匹配段落 " + str(number) + "：")
            print(paragraph)
            print()

    if matched_files == 0:
        print("未找到匹配内容。")
    else:
        print("共找到 " + str(matched_files) + " 个文件、" + str(matched_paragraphs) + " 个匹配段落。")

if __name__ == "__main__":
    main()
    