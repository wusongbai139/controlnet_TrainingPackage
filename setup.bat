@echo off

python3.8 -m venv convenv
call convenv\Scripts\activate
pip install -r requirements.txt

echo Dependencies installed.
echo Virtual environment is ready and activated.

call convenv\Scripts\deactivate

cd %~dp0
npm install

cd %~dp0contrain-ui
npm install

cd ..

cd %~dp0nodelink
npm install

echo Setup complete.
pause