% prepara el repositorio para su despliegue. 
release: sh -c 'cd bookrecommendations && python manage.py migrate'
% especifica el comando para lanzar Decide
web: sh -c 'cd bookrecommendations && gunicorn bookrecommendations.wsgi --log-file -'