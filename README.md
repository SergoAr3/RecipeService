# RecipeService

Этот API позволяет управлять рецептами, включая создание, чтение, обновление и удаление рецептов, а также загрузку и управление изображениями для рецептов. API использует интеграцию с Google Drive для хранения изображений.

## Эндпоинты

- **Рецепты**
  - [Получить рецепт](#получить-рецепт)
  - [Получить все рецепты](#получить-все-рецепты)
  - [Получить отфильтрованные рецепты](#получить-отфильтрованные-рецепты)
  - [Создать рецепт](#создать-рецепт)
  - [Обновить рецепт](#обновить-рецепт)
  - [Удалить рецепт](#удалить-рецепт)
  - [Оценить рецепт](#оценить-рецепт)
  - [Загрузить изображение для рецепта](#загрузить-изображение-для-рецепта)
  - [Получить изображение рецепта](#получить-изображение-рецепта)

- **Шаги приготовления**
  - [Создать шаг приготовления](#создать-шаг-приготовления)
  - [Обновить шаг приготовления](#обновить-шаг-приготовления)
  - [Удалить шаг приготовления](#удалить-шаг-приготовления)
  - [Загрузить изображение для шага](#загрузить-изображение-для-шага)
  - [Получить изображение шага](#получить-изображение-шага)

- **Ингредиенты**
  - [Создать ингредиент](#добавить-ингредиент)
  - [Обновить ингредиент](#обновить-ингредиент)
  - [Удалить ингредиент](#удалить-ингредиент)




### Получить рецепт

Описание: Возвращает один рецепт по его ID.<br>  
Метод: <b>GET</b><br> 
URL: /recipe/{recipe_id}<br>  
Пример ответа:<br>
```json
{
  "recipe": {
    "id": 1,
    "title": "Название рецепта",
    "description": "Описание рецепта",
    "total_time": 1200,
    "average_rating": 4.5,
    "image_id": "1oLoIjxkUwZ4SHTEHpG61-btzfHT9m9Bt",
    "ingredients": [
      {
        "recipe_id": 1,
        "quantity": "Количество",
        "name": "Название ингредиента",
        "id": "ID ингредиента"
      }
    ],
    "steps": [
      {
        "step_time": 600,
        "description": "Описание шага",
        "id": 1,
        "number": 1,
        "image_id": null,
        "recipe_id": 5
      }
    ]
  }
}
```
```sh
recipe: Основной объект, содержащий информацию о рецепте.

	•	id: Уникальный идентификатор рецепта.
	•	title: Название рецепта.
	•	description: Описание рецепта.
	•	total_time: Общее время на приготовление рецепта в секундах.
	•	average_rating: Средний рейтинг рецепта.
	•	image_id: ID изображения рецепта в Google drive.
  
```
```sh
ingredients: Массив объектов, каждый из которых представляет один ингредиент рецепта.

	•	recipe_id: ID рецепта, к которому относится ингредиент.
	•	quantity (строка): Количество ингредиента.
	•	name: Название ингредиента.
	•	id: Уникальный идентификатор ингредиента.
```
```sh
steps: Массив объектов, каждый из которых представляет шаг в рецепте.

	•	step_time: Время выполнения шага в секундах.
	•	description: Описание шага.
	•	id: Уникальный идентификатор шага.
	•	number: Порядковый номер шага.
	•	image_id: ID изображения шага в Google drive.
	•	recipe_id: ID рецепта, к которому относится этот шаг.
```

### Получить все рецепты

Описание: Возвращает все доступыне рецепты<br>   
Метод:  <b>GET</b><br>
URL: /recipe/all  
Пример ответа:
```json
{
  "recipes": [
    {
      "id": 1,
      "title": "Название рецепта",
      "description": "Описание рецепта",
      "total_time": 1200,
      "average_rating": 3.3,
      "ingredients": [
        {
          "recipe_id": 1,
          "quantity": "Количество",
          "name": "Название ингредиента",
          "id": 1
        }
      ],
      "steps": [
        {
          "step_time": 600,
          "description": "Описание шага",
          "id": 1,
          "number": 1,
          "image_id": null,
          "recipe_id": 5
        }
      ]
    }
  ]
}
```
```sh
recipes: Массив содержащий в себе все рецепты.

	•	id: Уникальный идентификатор рецепта.
	•	title: Название рецепта.
	•	description: Описание рецепта.
	•	total_time: Общее время на приготовление рецепта в секундах.
	•	average_rating: Средний рейтинг рецепта.
	•	image_id: ID изображения рецепта в Google drive.
  
```
```sh
ingredients: Массив объектов, каждый из которых представляет один ингредиент рецепта.

	•	recipe_id: ID рецепта, к которому относится ингредиент.
	•	quantity (строка): Количество ингредиента.
	•	name: Название ингредиента.
	•	id: Уникальный идентификатор ингредиента.
```
```sh
steps: Массив объектов, каждый из которых представляет шаг в рецепте.

	•	step_time: Время выполнения шага в секундах.
	•	description: Описание шага.
	•	id: Уникальный идентификатор шага.
	•	number: Порядковый номер шага.
	•	image_id: ID изображения шага в Google drive.
	•	recipe_id: ID рецепта, к которому относится этот шаг.
```

### Получить отфильтрованные рецепты

Описание: Возвращает список рецептов с возможностью фильтрации по ингредиентам, времени приготовления, рейтингу, а также сортировки по времени и рейтингу<br>
URL: /recipe<br>
Метод: <b>GET</b><br>
Параметры запроса:<br>

	•	ingredient_name (строка, необязательный): Название ингредиента для фильтрации рецептов.
	•	min_time (время, необязательный): Минимальное время приготовления рецепта (формат HH:MM:SS).
	•	max_time (время, необязательный): Максимальное время приготовления рецепта (формат HH:MM:SS).
	•	min_rating (float, необязательный, от 1 до 5): Минимальный рейтинг рецепта.
	•	max_rating (float, необязательный, от 1 до 5): Максимальный рейтинг рецепта.
	•	sort_time (строка, необязательный): Сортировка по времени приготовления (desc или asc).
	•	sort_rating (строка, необязательный): Сортировка по рейтингу (desc или asc).
Пример ответа:<br>
```json
{
  "recipe": {
    "id": 1,
    "title": "Название рецепта",
    "description": "Описание рецепта",
    "total_time": 1200,
    "average_rating": 4.5,
    "image_id": "1oLoIjxkUwZ4SHTEHpG61-btzfHT9m9Bt",
    "ingredients": [
      {
        "recipe_id": 1,
        "quantity": "Количество",
        "name": "Название ингредиента",
        "id": "ID ингредиента"
      }
    ],
    "steps": [
      {
        "step_time": 600,
        "description": "Описание шага",
        "id": 1,
        "number": 1,
        "image_id": null,
        "recipe_id": 5
      }
    ]
  }
}
```
```sh
recipe: Основной объект, содержащий информацию о рецепте.

	•	id: Уникальный идентификатор рецепта.
	•	title: Название рецепта.
	•	description: Описание рецепта.
	•	total_time: Общее время на приготовление рецепта в секундах.
	•	average_rating: Средний рейтинг рецепта.
	•	image_id: ID изображения рецепта в Google drive.
  
```
```sh
ingredients: Массив объектов, каждый из которых представляет один ингредиент рецепта.

	•	recipe_id: ID рецепта, к которому относится ингредиент.
	•	quantity (строка): Количество ингредиента.
	•	name: Название ингредиента.
	•	id: Уникальный идентификатор ингредиента.
```
```sh
steps: Массив объектов, каждый из которых представляет шаг в рецепте.

	•	step_time: Время выполнения шага в секундах.
	•	description: Описание шага.
	•	id: Уникальный идентификатор шага.
	•	number: Порядковый номер шага.
	•	image_id: ID изображения шага в Google drive.
	•	recipe_id: ID рецепта, к которому относится этот шаг.
```

### Создать рецепт.
Описание: Создает рецепт<br>
URL: /recipe<br>
Метод: <b>POST</b><br>
Тело запроса:
```json
{
  "title": "Название рецепта",
  "description": "Описание рецепта",
  "ingredients": [
    {
      "name": "Название ингредиента",
      "quantity": "Количество"
    }
  ],
  "steps": [
    {
      "description": "Описание шага",
      "step_time": "00:10:00",
      "number": 1
    }
  ]
}
```
```sh
	•	title: Название рецепта.
	•	description: Описание рецепта.  
```
```sh
ingredients: Массив объектов, каждый из которых представляет один ингредиент рецепта.

	•	name: Название ингредиента.
	•	quantity (строка): Количество ингредиента.
```
```sh
steps: Массив объектов, каждый из которых представляет шаг в рецепте.

	•	description: Описание шага.
	•	step_time: Время выполнения шага в формате "HH:MM:SS".
	•	id: Уникальный идентификатор шага.
	•	number: Порядковый номер шага.
```

### Обновить рецепт.
Описание: Обновляет рецепт по его ID<br>
URL: /recipe/{recipe_id}<br>
Метод: <b>PATCH</b><br>
Тело запроса:
```json
{
  "title": "Название рецепта",
  "description": "Описание рецепта",
}
```
```sh
	•	title: Название рецепта. (опционально)
	•	description: Описание рецепта. (опционально)  
```
 
### Удалить рецепт.
Описание: Удаляет рецепт по ID<br>
URL: /recipe/{recipe_title}<br>
Метод: <b>PUT</b><br>


### Оценить рецепт.
Описание: Поставить оценку рецепту<br>
URL: /recipe/{recipe_id}<br>
Метод: <b>DELETE</b><br>
Параметр запроса:<br>
```sh
 •	rating (вещественное число): Рейтинг.
```
### Загрузить изображение для рецепта
Описание: Загрузить изображение для рецепта по его названию<br>
URL: /recipe/image<br>
Метод: <b>POST</b><br>
Параметр запроса:<br>
```sh
 •	recipe_title: Название рецепта.
```
Данные:<br>
```sh
 •	file (UploadFile, обязательный): Файл изображения, который будет загружен.
```

### Получить изображение рецепта
Описание: Получить изображение для рецепта по его названию<br>
URL: /recipe/image/{recipe_title}<br>
Метод: <b>GET</b><br>
Ответ:<br>
```sh
 •	потоковое изображение в формате image/jpeg
```



### Создать шаг приготовления.
Описание: Создать шаг приготовления для рецепта по его ID<br>
URL: /step<br>
Метод: <b>POST</b><br>
Параметр запроса:<br>
```sh
 •	recipe_id (целое число): ID рецепта.
```
Тело запроса:
```json
{
  "description": "Описание шага."
  "step_time": "00:10:00",
  "number": 1
}
```
```sh
	•	description: Описание шага. 
	•	step_time: Время выполнения шага в формате "HH:MM:SS".
	•	number: Порядковый номер шага.
```


### Обновить шаг приготовления.
Описание: Обновить шаг приготовления для рецепта по его ID<br>
URL: /step/{recipe_id}<br>
Метод: <b>PATCH</b><br>
Параметр запроса:<br>
```sh
 •	step_number (целое число):  Номер шага.
```
Тело запроса:
```json
{
  "description": "Порезать мелко овощи",
  "step_time": "00:10:00",
  "number": 1
}
```
```sh
	•	description: Описание шага. (опционально)
	•	step_time: Время выполнения шага в формате "HH:MM:SS". (опционально)
	•	number: Порядковый номер шага. (опционально)
```

### Удалить шаг приготовления.
Описание: Удалить шаг приготовления для рецепта по его ID<br>
URL: /step/{recipe_id}<br>
Метод: <b>DELETE</b><br>
Параметр запроса:<br>
```sh
 •	step_number (целое число): номер шага 
```


### Загрузить изображение для шага
Описание: Загрузить изображение для определенного шага приготовления по его номеру и названию рецепта<br>
URL: /step/image<br>
Метод: <b>POST</b><br>
Параметры запроса:<br>
```sh
 •	recipe_title (строка): название рецепта.
 •	step_number (целое число): номер шага.
```
Данные:<br>
```sh
 •	file (UploadFile, обязательный): Файл изображения, который будет загружен.
```

### Получить изображение шага
Описание: Получить изображение для определенного шага приготовления по его номеру и названию рецепта<br>
URL: /recipe/image/{recipe_title}/{step_number}<br>
Метод: <b>GET</b><br>
Ответ:<br>
```sh
 •	потоковое изображение в формате image/jpeg
```

### Создать ингредиент.
Описание: Создать ингредиент для рецепта по его ID<br>
URL: /ingredient<br>
Метод: <b>POST</b><br>
Параметр запроса:<br>
```sh
 •	recipe_id (целое число): ID рецепта.
```
Тело запроса:
```json
{
  "name": "Название ингредиента",
  "quantity": "Количество"
}
```
```sh
	•	name: Название ингредиента.
	•	quantity (строка): Количество ингредиента.
```


### Обновить ингредиент.
Описание: Обновить ингредиент для рецепта по его ID<br>
URL: /ingredient/{recipe_id}<br>
Метод: <b>PATCH</b><br>
Параметр запроса:<br>
```sh
 •	ingredient_name (строка):  Название ингредиента.
```
Тело запроса:
```json
{
  "name": "Название ингредиента",
  "quantity": "Количество"
}
```
```sh
	•	name: Название ингредиента. (опционально)
	•	quantity (строка): Количество ингредиента. (опционально)
```

### Удалить ингредиент.
Описание: Удалить ингредиент для рецепта по его ID<br>
URL: /ingredient/{recipe_id}<br>
Метод: <b>DELETE</b><br>
Параметр запроса:<br>
```sh
 •	ingredient_name (строка):  Название ингредиента.
```

