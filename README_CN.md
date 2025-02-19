# 书签解析器

简体中文 | [English](README.md)

这是一个用于解析 Firefox、Chrome 和 Edge 导出的 HTML 书签文件的 Python 项目。它提供多种导出选项，以满足您的特定需求。

## 功能

1. 导出目录结构和书签：输出指定书签目录的完整目录结构和书签，包括所有子目录。
2. 仅导出目录结构：输出指定书签目录（不包括书签）的完整目录结构。
3. 仅导出书签：输出指定书签目录下的所有书签，不包括目录结构。

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法


```
python main.py -f <bookmark_file> [-fmt <format>] [-d <directory>]
- `<bookmark_file>`: 书签文件的路径。
- `--format` 或 `-fmt`: 导出格式，可选值为 `all`、`directory` 或 `bookmarks`，默认为 `directory`。
- `--directory` 或 `-d`: 指定书签目录，默认为根目录。
```

## 示例

```
python main.py -f bookmarks.html -fmt all -d "My Bookmarks"
```

## 输出格式

1. **包含目录结构的书签**:


```bash
Bookmarks Bar
|- Level1
   |- Search Engines
      |- Google
      |- Bing
```

2. **输出目录结构**:

```bash
Bookmarks Bar
|- Level1
   |- Search Engines
```

3. **输出书签**:

```bash
Google
Bing
```

## 日志
日志文件存储在 `logs/bookmark_parser.log` 中，包含详细的错误信息。

## License

GPL-3.0 License

## Author

Victor Lee