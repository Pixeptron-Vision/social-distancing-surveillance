@echo OFF
::Replace the below path with the absolute path where the script is present
::Create a shortcut of this file and paste it in Startup folder of StartMenu > Programs
::To go to startup folder run "shell:startup" in Run window. Then copy the shortcut of this file in that folder

cd "C:\Users\shouv\Desktop\Tata Steel\Projects\Version 0"
call venv\Scripts\activate.bat
::cd "Project Path"
python main.py