# Alpha Home
[OUR WEBSITE](https://home.umtechn.ru)
<br>
[OUR ANDROID APP](https://bit.do/alpha_home_dev)
<br>
To load fixture execute:
<br>
python manage.py loaddata -e contenttypes home/fixtures/default.json
To dump fixture execute:
<br>
python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission > home/fixtures/test.json
<br>
Если вы хотите загрузить settings.py напишите
<br>
git add -f alpha_home/settings.py
