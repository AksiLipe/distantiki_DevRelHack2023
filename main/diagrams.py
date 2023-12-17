import datetime
import random

from matplotlib import pyplot as plt

from devrelhack.settings import BASE_DIR


def create_diagram(categories: dict):
    categories_count = len(categories.keys())
    all_members_count = sum(len(value) for k, value in categories.items())
    labels = []

    sizes = []
    for k, members in categories.items():
        labels.append(f'{k} - {len(members)} чел.')
        sizes.append(len(members) / all_members_count * 100)
    print(sizes)
    print(len(sizes))
    # Цвета для сегментов диаграммы
    colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(categories_count)]

    plt.clf()

    # Создание круговой диаграммы
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)

    # Настройка аспектов диаграммы для получения круга
    plt.axis('equal')
    filename = f'diagrams/{datetime.datetime.now()}-diagram.png'
    plt.savefig(BASE_DIR / 'main/static/' / filename)  # Сохранение диаграммы в файл
    return filename
