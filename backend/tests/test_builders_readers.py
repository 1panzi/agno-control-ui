"""
Reader builders build() 测试。
可选依赖未安装时自动跳过。
"""
import pytest
from unittest.mock import MagicMock

from builders.readers.pdf import PdfReaderBuilder
from builders.readers.docx import DocxReaderBuilder
from builders.readers.text import TextReaderBuilder
from builders.readers.csv import CsvReaderBuilder
from builders.readers.json_reader import JsonReaderBuilder
from builders.readers.website import WebsiteReaderBuilder
from builders.readers.youtube import YoutubeReaderBuilder
from builders.readers.arxiv import ArxivReaderBuilder


@pytest.fixture
def resolver():
    return MagicMock()


@pytest.mark.asyncio
async def test_pdf_reader_build(resolver):
    pytest.importorskip("pypdf", reason="pypdf not installed")
    builder = PdfReaderBuilder()
    obj = await builder.build({}, resolver)
    from agno.knowledge.reader.pdf_reader import PDFReader
    assert isinstance(obj, PDFReader)


@pytest.mark.asyncio
async def test_pdf_reader_no_chunk(resolver):
    pytest.importorskip("pypdf", reason="pypdf not installed")
    builder = PdfReaderBuilder()
    obj = await builder.build({"chunk": False}, resolver)
    assert obj.chunk is False


@pytest.mark.asyncio
async def test_docx_reader_build(resolver):
    pytest.importorskip("docx", reason="python-docx not installed")
    builder = DocxReaderBuilder()
    obj = await builder.build({}, resolver)
    from agno.knowledge.reader.docx_reader import DocxReader
    assert isinstance(obj, DocxReader)


@pytest.mark.asyncio
async def test_text_reader_build(resolver):
    builder = TextReaderBuilder()
    obj = await builder.build({}, resolver)
    from agno.knowledge.reader.text_reader import TextReader
    assert isinstance(obj, TextReader)


@pytest.mark.asyncio
async def test_text_reader_with_encoding(resolver):
    builder = TextReaderBuilder()
    obj = await builder.build({"encoding": "gbk"}, resolver)
    assert obj.encoding == "gbk"


@pytest.mark.asyncio
async def test_csv_reader_build(resolver):
    builder = CsvReaderBuilder()
    obj = await builder.build({}, resolver)
    from agno.knowledge.reader.csv_reader import CSVReader
    assert isinstance(obj, CSVReader)


@pytest.mark.asyncio
async def test_json_reader_build(resolver):
    builder = JsonReaderBuilder()
    obj = await builder.build({}, resolver)
    from agno.knowledge.reader.json_reader import JSONReader
    assert isinstance(obj, JSONReader)


@pytest.mark.asyncio
async def test_website_reader_build(resolver):
    pytest.importorskip("bs4", reason="beautifulsoup4 not installed")
    builder = WebsiteReaderBuilder()
    obj = await builder.build({}, resolver)
    from agno.knowledge.reader.website_reader import WebsiteReader
    assert isinstance(obj, WebsiteReader)


@pytest.mark.asyncio
async def test_website_reader_with_options(resolver):
    pytest.importorskip("bs4", reason="beautifulsoup4 not installed")
    builder = WebsiteReaderBuilder()
    obj = await builder.build({"max_depth": 3, "max_links": 50}, resolver)
    assert obj.max_depth == 3
    assert obj.max_links == 50


@pytest.mark.asyncio
async def test_youtube_reader_build(resolver):
    pytest.importorskip("youtube_transcript_api", reason="youtube_transcript_api not installed")
    builder = YoutubeReaderBuilder()
    obj = await builder.build({}, resolver)
    from agno.knowledge.reader.youtube_reader import YouTubeReader
    assert isinstance(obj, YouTubeReader)


@pytest.mark.asyncio
async def test_arxiv_reader_build(resolver):
    pytest.importorskip("arxiv", reason="arxiv not installed")
    builder = ArxivReaderBuilder()
    obj = await builder.build({}, resolver)
    from agno.knowledge.reader.arxiv_reader import ArxivReader
    assert isinstance(obj, ArxivReader)


def test_reader_category_and_types():
    assert PdfReaderBuilder.category == "reader"
    assert PdfReaderBuilder.type == "pdf"
    assert DocxReaderBuilder.type == "docx"
    assert TextReaderBuilder.type == "text"
    assert CsvReaderBuilder.type == "csv"
    assert JsonReaderBuilder.type == "json"
    assert WebsiteReaderBuilder.type == "website"
    assert YoutubeReaderBuilder.type == "youtube"
    assert ArxivReaderBuilder.type == "arxiv"


def test_reader_schema_has_chunk_fields():
    for builder in [PdfReaderBuilder(), TextReaderBuilder(), CsvReaderBuilder()]:
        names = [f["name"] for f in builder.schema]
        assert "chunk" in names, f"{builder.__class__.__name__} schema missing 'chunk'"
