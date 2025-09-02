import logging.config
from datetime import datetime, timezone, date




logger = logging.getLogger(__name__)


def escape_markdown_v2(text: str) -> str:
    """
    Экранирует специальные символы в строке для использования в режиме ParseMode.MARKDOWN_V2.
    """
    # Этот порядок важен: сначала экранируем обратный слэш
    text = text.replace('\\', '\\\\')
    # Затем остальные символы
    reserved_chars = '}{[]()>#+-=.:,!@/_'
    for char in reserved_chars:
        text = text.replace(char, f'\\{char}')
    return text


