<h1>Instruções de instalação do app</h1>
1. Na pasta do projeto, criar ambiente virtual python chamado (django-env) para o git não enviar o ambiente nos commits:<br>
<code>python -m venv django-env</code><br>

2. Ativar ambiente python no windows:<br>
<code>django-env\Scripts\activate</code><br>

3. instalar dependencias do projeto:<br>
<code>pip install -r requirements.txt</code><br>

4. acessar diretório mysite e executar:<br>
<code>py manage.py makemigrations</code><br>
<code>py manage.py migrate</code><br>

5. Iniciar servidor da aplicação:<br>
<code>python manage.py runserver</code>

user: admin<br>
password: 123 
