# Задача 1. Инициализация рабочего окружения

* **Мягкий дедлайн**: --
* **Жёсткий дедлайн**: 14.02.2024, 23:59
* Полный балл: 5

## Задача

- [X] Сделать `fork` данного репозитория.
- [X] Добавить ссылку на ваш `fork` в [таблицу](https://docs.google.com/spreadsheets/d/1zVPStPIwvrCY2cZBLypZyCMgZ5yB2RLS0TCkwR7JfXo/edit?usp=sharing).
- [X] Добавить в совладельцы форка одного из ассистентов (чтобы узнать, кого именно, нужно посмотреть в [таблицу](https://docs.google.com/spreadsheets/d/1zVPStPIwvrCY2cZBLypZyCMgZ5yB2RLS0TCkwR7JfXo/edit?usp=sharing))
- [X] Реализовать модуль, предоставляющий перечисленные ниже возможности. Для работы с графами использовать [cfpq-data](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#graphs). Данный модуль в дальнейшем будет расширяться. Функции, которые необходимо реализовать:
  - [X] По имени графа вернуть количество вершин, рёбер и перечислить различные метки, встречающиеся на рёбрах. Для получения графа по имени использовать [эту функцию](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/tutorial.html#get-a-real-graph).
  - [X] По количеству вершин в циклах и именам меток строить [граф из двух циклов](https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.generators.labeled_two_cycles_graph.html#cfpq_data.graphs.generators.labeled_two_cycles_graph) и сохранять его в указанный файл в формате DOT (использовать pydot).
- [X] Добавить необходимые тесты.
- [X] Добавить запуск тестов с помощью `pytest` в `.github/workflows/`.
