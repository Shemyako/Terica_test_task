def overlay(first_array, second_array, is_checking = True):
    '''
    Наложение интервалов. 
    is_checking - пересечение ли
    Возвращаем список с интервалами
    '''
    # Список для ответов
    tutor_intervals = []
    
    # Начало конец для интервалов с ответами
    strart = 0
    end = 0

    # Проходимся по нижнему списку
    for i in range(0,len(second_array),2):

        # Для нижнего списка перебираем все верхние
        for j in range(0,len(first_array),2):
            # Если интервалы не пересекаются
            # (начало нижнего позже конца верхнего) => пока не дошли до нужного => continue
            if (second_array[i] > first_array[j+1]):
                continue
            # (конец нижнего раньше начала верхнего) => уже прошли нужный => break
            elif (second_array[i+1] < first_array[j]):
                break

            # Начало выбираем большее если пересечение
            # Если объединение - меньшее
            if (second_array[i] > first_array[j]) == is_checking:
                start = second_array[i]
            else:
                start = first_array[j]

            # Конец выбираем меньший если пересечение
            # Если объединение - большее
            if (second_array[i+1] > first_array[j+1]) == is_checking:
                end = first_array[j+1]
            else:
                end = second_array[i+1]

            # Добавляем ответ, обнуляем начало, конец
            tutor_intervals.append(start)
            tutor_intervals.append(end)
            start, end = 0, 0
    
    return tutor_intervals


def checking_overlay(array):
    '''
    Объединение интервалов
    array - список для объединения
    Возвращаем объединённый где можно список
    '''
    i = 0
    # Перебираем попарно интервалы
    while (i< len(array)-2):
        j = i + 2

        while j <len(array):
            # Пытаемся объединить два интервала
            answer = overlay([array[i], array[i+1]], [array[j], array[j+1]], False)
            
            # Если успешно (ответ - 1 интервал),
            # то заменяем i-ый, удаляем j-ый
            if (len(answer) == 2):
                array[i], array[i+1] = answer
                del array[j:j+2]
            else: # иначе идём дальше
                j += 2

        i += 2
    
    return array


def appearance(intervals):
    '''
    Основная функция. Последовательно накладывает функции и объединяет результаты
    '''
    # Пересечение урока и посещения учеников
    first_intervals = overlay(intervals['lesson'],intervals['pupil'])
    # Пересечение предыдущего шага с учителем
    first_intervals = overlay(first_intervals, intervals['tutor'])
    # Объединение (удаление повторений)
    first_intervals = checking_overlay(first_intervals)

    # Поиск ответа (длины итоговых интервалов)
    answer = 0
    # Попарно из конца вычитаем начало
    for i in range(0,len(first_intervals),2):
        answer += first_intervals[i+1] - first_intervals[i]

    return answer

# Тестовые данные с интервалами уроков
tests = [
    {'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'data': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]


if __name__ == '__main__':
    for i, test in enumerate(tests):
        # Получаем продолжительность занятия
        test_answer = appearance(test['data'])
        print(test_answer)
        # print('_______________________________')
        # Проверяем, есть ли ошибка
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
