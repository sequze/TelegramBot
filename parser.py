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
    place = 1  # Место по оригиналам
    place_with_priority = 1  # Место с учетом приоритетов
    rows = soup.find_all('tr', valign="top",
                         align="center", bgcolor="#ffffff")
    for row in rows:
        cells = row.find_all('td')
        if cells[1].text.strip() == snils:
            return (f"Ваше место в списке: {cells[0].text.strip()}\n"
                    f"По оригиналам: {place}\n"
                    f"С учетом оригиналов и приоритетов: "
                    f"{place_with_priority}")
        if cells[15].text.strip() == "да":
            place += 1
            if cells[14].text.strip() == "1":
                place_with_priority += 1
    return "СНИЛС не найден"
