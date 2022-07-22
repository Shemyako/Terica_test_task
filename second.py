import requests

def find_amount():
    '''
    Поиск животных по буквам
    Перехожу на следующую влкдаку по ссылке из html
    '''
    # Начальный адрес
    url = ("https://ru.wikipedia.org/w/index.php?title=Категория%3AЖивотные_по_алфавиту&from=А")

    # Отпралвяем запрос
    response = requests.get(url)

    # Начальная буква
    cur_letter = "А"

    # С какого индекса искать
    start_index = 0

    # Количество животных
    count = 0
    
    # Пока есть две кнопки на следующую страницу
    # (на последней странице это просто текст, без <a>)
    while response.text.count('" title="Категория:Животные по алфавиту">Следующая страница') == 2:
        # Количество букв кроме первой на странице
        amount = response.text.count('</a></li></ul></div><div class="mw-category-group"><h3>')
        # print(amount)

        # Если страница начинается не с предыдущей буквы
        if response.text[response.text.find("<div class=\"mw-category mw-category-columns\"><div class=\"mw-category-group\"><h3>") + 80] != cur_letter:
            # Выводим, обнуляем счётчик, ищем новую текущую букву
            print(f"{cur_letter}: {count}")
            count = 0
            cur_letter = response.text[response.text.find("<div class=\"mw-category mw-category-columns\"><div class=\"mw-category-group\"><h3>") + 80]

        # Если несколько букв на странице (кроме начальной)
        if amount != 0:
            # Ищем сначала до первой буквы после начальной
            end_index = response.text.find('</a></li></ul></div><div class="mw-category-group"><h3>')
            for i in range(amount):
                # Счётчик, вывод
                count += response.text.count("<li><a href=", start_index, end_index)
                print(f"{cur_letter}: {count}")
                
                # Начало - бывшый конец; Находим текущую букву и конечный индекс (до которого искать)
                start_index = end_index
                cur_letter = response.text[end_index+55]
                end_index = response.text.find('</a></li></ul></div><div class="mw-category-group"><h3>',start_index+1)

                count = 0
            # return
        
        # Искать до конца текста
        end_index = len(response.text)
        # Ищем животных
        count += response.text.count("<li><a href=", start_index, end_index)

        # Обнуляем начало
        start_index = 0

        # Ишём ссылку на следующую страницу
        a = response.text.rindex('" title="Категория:Животные по алфавиту">Следующая страница')
        b = response.text.rindex('(<a href="', 0, a) + 10
        url = response.text[b:a]

        # Отправляем запрос на следующую страницу
        response = requests.get('https://ru.wikipedia.org'+url.replace("amp;",""))
    
    # Последний проход для последней страницы
    count += response.text.count("<li><a href=", start_index, end_index)
    print(f"{cur_letter}: {count}")

# Запуск функции
find_amount()