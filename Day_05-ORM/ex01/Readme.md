## Afin d'appliquer les models dans la db 
`python manage.py makemigrations ex01`

## Puis les Maj
`python manage.py migrate ex01`

## Verif Migration
`python manage.py showmigrations ex01`
->  Doit avoir [X] 0001_initial 
    ( La croix [X] doit être présente )