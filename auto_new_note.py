import os
import subprocess
from datetime import date


CONTENT_DIR = "content"


def safe_category_path(category):
    normalized = os.path.normpath(category.strip())
    if not normalized or normalized == ".":
        raise ValueError("分类目录不能为空。")
    if os.path.isabs(normalized) or normalized == ".." or normalized.startswith(".." + os.sep):
        raise ValueError("分类目录必须位于 content 目录内。")
    return normalized


def yaml_string(value):
    return value.replace("\\", "\\\\").replace('"', '\\"')


def open_in_editor(path):
    absolute_path = os.path.abspath(path)
    if os.name == "nt":
        os.startfile(absolute_path)
    elif os.name == "posix":
        opener = "open" if os.uname().sysname == "Darwin" else "xdg-open"
        subprocess.Popen([opener, absolute_path])
    else:
        raise OSError("当前系统不支持自动打开文件。")


def main():
    note_name = input("请输入笔记名称：").strip()
    category = input("请输入分类目录：").strip()

    if not note_name:
        print("笔记名称不能为空。")
        return

    try:
        category_path = safe_category_path(category)
    except ValueError as error:
        print(str(error))
        return

    directory = os.path.join(CONTENT_DIR, category_path)
    file_path = os.path.join(directory, note_name + ".md")

    if os.path.exists(file_path):
        print("文件已存在，未覆盖：" + file_path)
        open_in_editor(file_path)
        return

    os.makedirs(directory, exist_ok=True)
    frontmatter = (
        "---\n"
        + 'title: "' + yaml_string(note_name) + '"\n'
        + "date: " + date.today().isoformat() + "\n"
        + "tags:\n"
        + "  - 待分类\n"
        + "---\n\n"
    )

    with open(file_path, "x", encoding="utf-8", newline="\n") as note_file:
        note_file.write(frontmatter)

    print("已创建笔记：" + file_path)
    open_in_editor(file_path)


if __name__ == "__main__":
    main()
