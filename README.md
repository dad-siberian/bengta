# bengta
 Загрузка комиксов xkcd

Программа для публикации случайного комикса [xkcd](https://xkcd.com/) в вашем сообществе социальной сети ВКонтакте

## Запуск бота

Для запуска программы требуется Python 3.

- Скачайте код `git clone https://github.com/dad-siberian/bengta.git`
- Установите зависимости командой `pip install -r requirements.txt`
- Создать в корне проекта переменную окружения `.env` и внести настройки. Подробнее в разделе настройка переменной окружения.
- Запустите скрипт командой `python3 main.py`

## Настройка переменной окружения

```
ACCESS_TOKEN={access token vk}
GROUP_ID={group id vk}
```

- ACCESS_TOKEN ключ доступа к API VK. [Инструкция](https://vk.com/dev/implicit_flow_user) Implicit Flow для получения ключа доступа пользователя
- GROUP_ID: Узнать group id vk для вашей группы можно [здесь](https://regvk.com/id/)

## Предварительные условия

Для работы скрипта у вас должен быть установлен python версии 3.8 и выше.


## Цель проекта

Получение уведомлений о готовности ревью кода
