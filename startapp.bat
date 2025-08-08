@echo off
cd /d C:\projetos\pdf_splitter_app
call .venv\Scripts\activate.bat
set FLASK_APP=app.py
set FLASK_ENV=production
python -m flask run --host=127.0.0.1 --port=5000 --no-reload