import logging.config
from datetime import datetime, timezone, date




logger = logging.getLogger(__name__)


class ParseModes:
    MARKDOWN_V2 = 'MarkdownV2'
    MARKDOWN = 'Markdown'
    HTML = 'HTML'
    

def escape_markdown_v2(text: str) -> str:
    """ Экранирует специальные символы в строке для использования в режиме ParseMode.MARKDOWN_V2."""
    reserved_chars = '}{[]()>#+=.:,!@/_-'
    for char in reserved_chars:
        text = text.replace(char, f'\\{char}')
    return text

