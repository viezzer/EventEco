<h1>EventEco</h1>
<h2>Instruções de instalação do app</h2>
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

<h2>Configuração do Banco de Dados</h2>
O projeto está configurado para usar PostgreSQL. Certifique-se de ter as credenciais corretas no arquivo settings.py.<br>

<h2>Funcionalidades</h2>

Gerenciamento de eventos<br>
Interface de administração personalizada<br>
Integração com TinyMCE para edição de texto rico<br>

<h2>Estrutura do Projeto</h2>
mysite/: Diretório principal do projeto Django<br>
eventos/: Aplicativo Django para gerenciamento de eventos<br>
static/: Arquivos estáticos (CSS, JavaScript, etc.)<br>
templates/: Templates HTML<br>

<h2>Tecnologias Utilizadas</h2>
Django<br>
PostgreSQL<br>
TinyMCE<br>
MailerSend (para envio de e-mails)<br>
