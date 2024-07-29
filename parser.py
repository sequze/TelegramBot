from bs4 import BeautifulSoup
import requests


def find_abiturient(
    snils: str,
    url: str
):
    # Загрузка HTML-файла
    response = requests.get(url)
    response.encoding = 'windows-1251'

    if response.status_code == 200:
        html_content = response.text

    # Создание объекта BeautifulSoup
    soup = BeautifulSoup(html_content, "lxml")

    # Поиск
    rows = soup.find_all('tr', style="font-weight:normal;", valign="top",
                         align="center", bgcolor="#ffffff")
    for row in rows:
        cells = row.find_all('td')
        if cells[1].text.strip() == snils:
            return cells[0].text.strip()
    return "СНИЛС не найден"

