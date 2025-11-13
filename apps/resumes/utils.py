#解析效果，对docx和pdf文件简历进行解析，取出其中的文本内容，组成一个长的字符串，存储到数据库，供AI调用
#解析工具
import PyPDF2
import docx


def parse_pdf(file_path):
    """解析 PDF 文件"""
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def parse_docx(file_path):
    """解析 Word 文件"""
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

