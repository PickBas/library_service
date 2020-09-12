# Git

## Что такое Git?
### Git - система контроля версий.
#### Если бы Git не существовал
Представим, что есть файл N.txt, в котором мы напишем "*Это первая запись в файле N*" и сохраним его. Второй раз мы напишем в нем "*Это пятая запись в файле N*" и сохраним его.
И получается, что мы совершили ошибку, ведь это лишь вторая запись, нужно было написать "*Это вторая запись в файле N*". А как теперь вернуть изменения? Получается - никак.
Нужно было сохранить вторую запись в файле N_second.txt, и у нас уже было бы 2 файла: N.txt и N_second.txt - в первом файле была бы первая версия текста,
то есть "Это первая запись в файле N", а во втором "Это пятая запись в файле N".

#### С использованием Git
А теперь рассмотрим ситуацию с Git. У нас также есть файл N.txt, в котором мы напишем "*Это первая запись в файле N*", скажем: "*Git, проследи за этим файлом и сохрани его текущее состояние, я буду называть текущее состояние данного файла '**Первая версия**'*". Теперь в файле N.txt хранится текст "*Это первая запись в файле N*".
Второй раз мы напишем в нем "*Это пятая запись в файле N*", и скажем: "*Git, сохрани измененное состояние файлая буду называть текущее состояние данного файла '**Вторая версия**'*". Теперь в файле хранится текст "*Это пятая запись в файле N*".
Что произошло? У нас остался один единственный файл, но Git хранит две его версии. Первая версия - "**Первая версия**". Вторая - "**Вторая версия**".
А теперь мы осознаем, что мы допустили ошибку во второй версии файла. Но это совсем не страшно, так как мы можем попросить Git: "Git, верни файл N.txt к первой версии".
И теперь мы открываем файл N.txt и видим текст "*Это первая запись в файле N*". И таких сохранений могут быть сотни.

Да, у нас файл был небольшой, можно было бы просто открыть файл и исправить это одно слово с *пятая* на *вторая*,
но файл так же мог содержать сотни тысяч строк кода, в котором какой-то программист изменил бы 50 строк, которые неверные. И тут было бы уже очень сложно откатить изменения вручную.

## Переходим к практике
Для демонстрации будет использоваться тестовый репозиторий, созданный заранее.

### Клонирование репозитория
* Репозиторий - папка, содержащая код, контролируемая Git, грубо говоря. Сокращенно говорят "*repo*"
* Клонирование - скачивание текущей версии данного репозитория
* Команда для клонирования: git clone https://ссылка_на_репу

#### 1. Копируем сылку 
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/1.png)
#### 2. Переходим в рабочую дерикторию, кликаем правой кнопкой мыши, выбираем *Git bash here*
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/2.png)
#### 3. Пишем команду для клонирования репы в терминал, ждем, пока клонирование завершится
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/3.png)
#### 4. Переходим в репозиторий, в нашем случае он называется *"test"*. Видим, что он пуст
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/4.png)
#### 5. Открываем в нем терминал (см. пункт 2). Проверим его статус командой git status. На данный момент сохранять нечего

### Создание версии
* Создадим файл для демонстрации
* Скажем Git проследить за нашим новым файлом
* Скажем Git создать версию
* Попросим Git проверить, не поступило ли изменений в наш репозиториев от других программистов
* Скажем Git отослать новую версию на удаленное хранилище, в нашем случае - **GitHub**

#### 1. Создаем файл, сохраняем
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/5.png)
#### 2. Проверяем, увидел ли Git наличие нового файла в репе
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/6.png)
#### 3. Говорим Git проследить за этим файлом командой "git add ." (. - текущая дериктория)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/7.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/8.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/9.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/10.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/11.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/12.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/13.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/14.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/15.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/16.png)
![alt text](https://github.com/2048-IT-Engineers/library_service/blob/master/docs/assets/git_tutor/17.png)
