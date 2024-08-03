from typing import Any, Dict, List, Union, Optional
from bs4 import BeautifulSoup
from app.handlers.api_handler import ApiHandler
from app.resources.errors import CRASH
import requests

api = ApiHandler("https://hentai20.io")

async def get_panels(*, chapter_id: str) -> Union[Dict[str, Any], int]:
    response: Any = await api.get(endpoint=f"/{chapter_id}",  html=True)
    
    if type(response) is int:
        return CRASH

    soup: BeautifulSoup = get_soup(response)
    panel_eles: List = soup.select('.alignnone')
    chapter_title: str = soup.select('.entry-title')[0].text
    panels: List[Dict[str, str]] = []

    for panel in panel_eles:
        image_url = panel.get("src")

        panels.append({
            "image_url": image_url,
        })

    return {
        "chapter_id": chapter_id,
        "chapter_title": chapter_title,
        "panels": panels,
    }


def get_soup(html) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')


def download_image_from_url(image_url: Optional[str]) -> Union[None, bytes]:
    if not image_url:
        return None

    headers = {
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'Referer': 'https://chapmanganato.to/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Linux"'
     }

    try:
        response = requests.get(image_url, headers=headers)
        pass
    except Exception as e:
        print(e)
        return None
    else:
        return response.content