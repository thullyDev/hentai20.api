from typing import Any, Dict, List, Union, Optional
from bs4 import BeautifulSoup
from requests import auth
from app.handlers.api_handler import ApiHandler
from app.resources.errors import CRASH
import requests

api = ApiHandler("https://hentai20.io")

async def get_panels(chapter_id: str) -> Union[Dict[str, Any], int]:
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

async def get_manga(manga_id) -> Union[Dict[str, Any], int]:
    response: Any = await api.get(endpoint=f"/manga/{manga_id}", html=True)

    if type(response) is int:
        return CRASH

    soup: BeautifulSoup = get_soup(response)
    image_ele = soup.select('.attachment-.size-.wp-post-image')[0]
    title = image_ele.get("alt")
    image_url = image_ele.get('src')
    description = soup.select('.entry-content.entry-content-single > p')[0].text.strip()
    chapter_eles = soup.select('.eph-num > a')

    ticks = {}
    tick_eles = soup.select(".imptdt")

    for tick in tick_eles:
        tick_type = tick.text.replace("Posted On", "created_at").replace("Updated On", "updated_at").split(" ")[0].lower().strip()

        if tick_type == "type":
            ticks["type"] = tick.select("a")[0].text 

        if tick_type in [ "updated_at", "created_at", "author" ]:
            ticks[tick_type] = tick.select("i")[0].text 

    chapters: List[Dict[str, str]] = []

    for i in range(1, len(chapter_eles)): #! skipping the first element
        chapter_ele = chapter_eles[i]
        href: Any = chapter_ele.get("href") 
        name: Any = chapter_ele.select(".chapternum")[0].text
        _date: Any = chapter_ele.select(".chapterdate")[0].text
        chapter_id = href.replace("https://hentai20.io/", "")
        
        chapters.append({
            "name": name,
            "chapter_id": chapter_id,
            "date": _date,
        })

    # TODO: add rating score

    return {
        "manga": {
            "manga_id": manga_id,
            "image_url": image_url,
            "title": title,
            **ticks,
            "description": description,
            "chapters": chapters,
        }
    }


async def get_filter_mangas(params: Dict[str, str], **kwargs) -> Union[Dict[str, Any], int]:
    response: Any = await api.get(**kwargs, params=params, html=True)
    page = params["page"]

    if type(response) is int:
        return CRASH

    soup: BeautifulSoup = get_soup(response)
    mangas: List[Dict[str, Any]] = []
    items: List = soup.select('.listupd .bsx > a')

    for manga in items:
        image_url = manga.select("img")[0].get("src")
        title = manga.get("title")
        href_chunks = manga.get("href").split("/")
        chunks_length = len(href_chunks)
        slug = href_chunks[chunks_length - 2]
        colored_ele = manga.select(".colored")
        colored = True if colored_ele else False
        latest_chapter = manga.select(".epxs")[0].text
        score = manga.select(".numscore")[0].text

        mangas.append({
            "title": title,
            "image_url": image_url,
            "colored": colored, 
            "slug": slug,
            "latest_chapter": latest_chapter,
            "score": score, 
        })

    return {
        "mangas": mangas,
        "pagination": {
            "page": page,
        }
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