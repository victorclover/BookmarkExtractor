# BookmarkExtractor
Bookmark Analysis and Export Tool. This Python program is designed to analyze HTML bookmark files exported from popular web browsers like Firefox, Chrome, and Edge. It provides multiple export options to suit your specific needs.

## Features

1. Export directory structure with bookmarks
2. Export directory structure only
3. Export bookmarks only (flattened list)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py -f <bookmark_file> [-fmt <format>] [-d <directory>]

Required arguments:
  -f, --file          Path to HTML bookmark file
  
Optional arguments:
  -fmt, --format      Output format: all, directory, bookmarks (default: directory)
  -d, --directory     Target directory name (default: root)
```

## Examples

1. Export full structure from specific directory:

```bash
python main.py -f bookmarks.html -fmt all -d "Bookmarks Bar"
```

2. Export only bookmarks from root:

```bash
python main.py -f bookmarks.html -fmt bookmarks
```

## Output Formats

1. **Directory + Bookmarks**:


```bash
Bookmarks Bar
|- Level1
   |- Search Engines
      |- Google
      |- Bing
```

2. **Directory Only**:

```bash
Bookmarks Bar
|- Level1
   |- Search Engines
```

3. **Bookmarks Only**:

```bash
Google
Bing
```

## Logging

Log files are stored in `logs/bookmark_parser.log`

## License

GPL-3.0 License

## Author

Victor Lee

