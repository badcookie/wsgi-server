# WSGI сервер

### Коротко о том, как это работает

```
from apps import my_app
from server import WSGIServer

server = WSGIServer('localhost', 8000)
server.run(my_app)
```

---


```WSGIServer.__init__(host, port)```

Создаёт главный сокет, привязывает его к адресу ```(host, port)``` и переводит в режим прослушивания.

<br>

```WSGIServer._parse_request(data)```

Извлекает HTTP данные из декодированного запроса.

<br>

```WSGIServer._to_environ(request_data)```

Использует HTTP данные в качестве переменных среды для 
приложения, передавая их в словарь environ.

<br>

```WSGIServer.run(app)``` 

Сокет принимает входящие запросы, приводит их к стандартному словарю environ
и передаёт приложению ``app``. Ответ от приложения передаётся сокету клиента.

<br>

```WSGIServer._start_response(status, headers)```

Обработчик ответа от приложения. Вызывается самим приложением.

<br>

```WSGIServer.stop()```

Сокет сервера посылает сигналы на закрытие соединения и уничтожается.


### Запуск 

```sh
$ make run H=[host] P=[port] A=[app]
```

Параметр | Значение
---------| -------------
host     | localhost (default)
port     | 8000 (default)
app      | django, flask, custom

### Тесты
```sh
$ make test
```

