import pytest
from bs4 import BeautifulSoup
from bookmark_parser import BookmarkParser
from config import DEFAULT_SHOW_BOOKMARK_NAME

# 模拟 HTML 书签文件内容
MOCK_HTML = """
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="1737899046" LAST_MODIFIED="0" PERSONAL_TOOLBAR_FOLDER="true">书签栏</H3>
    <DL><p>
    </DL><p>
    <DT><H3 ADD_DATE="1737899106" LAST_MODIFIED="1737899188">level1</H3>
    <DL><p>
        <DT><A HREF="https://www.bing.com/?toWww=1&redig=94CAE9A6C29B49D289601040D4DDEF11" ADD_DATE="1737899081" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABrElEQVQ4jc2Sv0tbURTHv+fea9575of6F3ToVErV2ckfS+MP6JJRELQOhRfQSQfRouLcgEsKKggOOggOcZBE26E4uEhx6FChdGkdxDyfiSZ593TICzHymjp08Ludy/d87veec4H/rwUBMNVrpurZ41RvHFs3YWeMRlCzBl/hyYNXslUtktYjVYfarRTd9zfpoa9NAEwAcejdpxeWIY+hKwazTgNcESTfMildLJd6Sqv9ZzVvDdDwNlOWV0jIEoqFl06qP+mkBqb52u0iIciUvBIU2gcQY/KkhWQoru/czXx68DsSZyHEM0Z+bfhcl242iNRrxDMGAA4AAPh5IcBMABQAwP1BiDyrmhkeAIGI29B8Pw8B4FgyuyeU1ctXl935teFzAGizs88p1PpZlws5JzUw+nAGyh8iAMKtR7OW4C8UjZzGktmPgkULg8fJbLPorvALAJDYEdiB9/c1Tux3qrA1D/beAEIweAuaf8tw+5R368w5H/qWgtaJ+jp92RkDY4dmrYwlj+Y6Zk45aueWgy6+p4CvnNiWABC1c8sxO/cNvYeqCeAf6XzY09EfOYea735J+IkAAAAASUVORK5CYII=">搜索 - Microsoft 必应</A>
        <DT><A HREF="https://learn.weeklyfinancialsolutions.com/open-program-fdr-5/?utm_medium=native&utm_media=microsoft&utm_source=msn_native&utm_campaign=698161314&utm_adgroup=1252345049883449&utm_content=78271696829971&utm_publisher=devicec&utm_adcampaign=781bc10d28531022f21ba69b14d6f61e&utm_match_type=carousel&msclkid=781bc10d28531022f21ba69b14d6f61e" ADD_DATE="1737899179" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACuklEQVQ4jXWT22tUVxTGf/ucM9cYkzyE3CaaMWeiMZTGzMRqJ9hOJvPkQyvaIiU+tFBBxL9A8I43YlCxEpGiYJCWFpo3oaESa0SDpA9FqZhxvGSMNdEkDnFmZOac5YM6xph8b3vv9a0F+/ctxRzVBSOfGaJ3Cva6vGUtATB0fVRp6u+8bfU++Gfgxux6NfsQCLafRNN3JJNjZCan0D0eUGCls7jLSvDVVoMtp+PDf23/qEFDa+zPdCYTS44kCK0J0bl5Aw3L6kDBSOIRF3/pY+j6ED7Tj8frHRi52R8pTDZD0VO+pjbBUSk79xyVhbRr/zHBUSW+prAEQtEzAPhXRT4NtMYEo1L2Hj4xr/H/6Usykb4gIiKHunoEo0LM1g4xg+0tmMHoWXdFo6yOfDWv2bZz0n+rWa7eiRXu1nZsFFf5cgkEo+c1RMLZqWm+3/LtHB7CzcSPjKeuUOZtwuOsLrz8sOUbXr1IYYu0aTnLqtG8Hkz/EgDy9kvujZ9iJnuXp6lLiOTRlBuQ97SWLcVYVETessq19zDeAJmcucF/j3ezyL2cYlcDRa6lOIxibMnNS18zdP2JnU5z78Ej3oaGvD3F7ce7SGX/ZeRpN6PP/wDsgil+/yH5mZcYuv5MU0oNukpLOHfhNwDKij6hqnQTE6lBqsvWk8mN4XauoKr060KDc72/4yxZjFJqkLrmL5vN1phgVMjBrp8WzMA7HTneI+gVUh/qkPqWSPDNp7REe3wrw4KzUnYf6F7QvO/wCcFZJb7GzyUQiv78YZRDHZfT6UwkGb/PmvBqvtu8gUbTD0pxJ57g4q99XL86RI3pp6jYe+3uUH/bR8tkBttPo2nbkqNjZKdf4PB6AMilM7hKFlNbWwNin40PX9467zYC1DdHwuh6J2J/kbesagCHrj8R1BVRVm9ieGBwdv1rIxaPTbOZGRQAAAAASUVORK5CYII=">Overcome Thousands in Credit Card Debt</A>
    </DL><p>
    <DT><A HREF="https://www.lendgo.com/heloc/la/?tg_ref=662765111&msclkid=f44de7129d751b5542528084a139580c&camp_id=1236951641210667&keyword=&sub2=77309611590503&mcampid=662765111&orderitemid=&targetid=:loc-190&matchtype=e&bmatchtype=be&network=a&device=c&feeditemid=&loc_interest_ms=&loc_physical_ms=&querystring=&orderitemid=&tactic=" ADD_DATE="1737899152" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABK0lEQVQ4jWNkeNzE8JeR4R8jw18Ghn+MDH9hCCICZUBEGBj+MjIxkAhor4EFmSPPwl8kYsbPyLHo3dXf//4lCep+/vN7wrOz9759wmIDJxPrYdlYHia2e78/rFUIiBTUfPDrEzsT82GdSB5mNiw2GLNL/GH4l/x8G8NfRkEmzt9//zU+O8rwl/G6XpI5j8Ted4/RNdz5/V6UmSuEV+PBz4+///8NElBb8+6mFAuvDBvvrR/vsdjw4s+X+BebO8Qc+ZnYz31/eezrs00qQV/+/k65u/Pxz88MDIzoGtTZhA3YxdXuzmT4yzhD0uPFr68S96ZCIw6mGkXDsz9fUvgNxJm4n//+GiGg6XJnJdZgRYTS538/bR4v/vX/rzwrv9+DtWe+vcCqgXEYpCUADtGMfrV1vlwAAAAASUVORK5CYII=">How Much Will You Get With a Home Equity Loan?</A>
</DL><p>
"""

@pytest.fixture
def mock_bookmark_file(tmp_path):
    """
    创建一个临时的模拟书签文件，并返回其路径
    """
    mock_file = tmp_path / "mock_bookmarks.html"
    mock_file.write_text(MOCK_HTML, encoding='utf-8')
    return str(mock_file)

def test_parse_file(mock_bookmark_file):
    """
    测试 _parse_file 方法是否能正确解析文件
    """
    parser = BookmarkParser(mock_bookmark_file)
    result = parser._parse_file()
    assert isinstance(result, BeautifulSoup)

def test_export_directory_and_bookmarks(mock_bookmark_file):
    """
    测试 export_directory_and_bookmarks 方法
    """
    parser = BookmarkParser(mock_bookmark_file)
    result = parser.export_directory_and_bookmarks()
    assert isinstance(result, list)
    if result:
        # 检查是否包含目录或书签信息
        assert any('name' in item or 'title' in item for item in result)

def test_export_directory_structure(mock_bookmark_file):
    """
    测试 export_directory_structure 方法
    """
    parser = BookmarkParser(mock_bookmark_file)
    result = parser.export_directory_structure()
    assert isinstance(result, list)
    for item in result:
        assert 'name' in item
        assert 'title' not in item

def test_export_bookmarks(mock_bookmark_file):
    """
    测试 export_bookmarks 方法
    """
    parser = BookmarkParser(mock_bookmark_file)
    result = parser.export_bookmarks()
    assert isinstance(result, list)
    for item in result:
        if DEFAULT_SHOW_BOOKMARK_NAME:
            assert 'name' in item
        else:
            assert 'url' in item

def test_nonexistent_file():
    """
    测试处理不存在的文件时是否抛出 FileNotFoundError
    """
    with pytest.raises(FileNotFoundError):
        BookmarkParser("nonexistent_file.html")

def test_traverse_directory(mock_bookmark_file):
    parser = BookmarkParser(mock_bookmark_file)
    root_dl = parser.tree.find('dl')
    if root_dl:
        result = parser._traverse_directory(root_dl)
        print("遍历结果：", result)
        assert isinstance(result, list)
        if result:
            assert any('name' in item or 'title' in item for item in result)