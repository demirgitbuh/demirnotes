@echo off
echo ================================
echo DemirNotes EXE Builder
echo ================================

REM Install dependencies
pip install customtkinter cryptography Pillow fpdf2 pyinstaller

REM Build EXE
echo Building EXE...
pyinstaller --noconfirm --onefile --windowed --name demirnotes --icon=Demnote.ico --add-data "Demnote.ico;." demirnotes.py

REM Copy to Desktop
echo Copying to Desktop...
copy /Y dist\demirnotes.exe "%USERPROFILE%\Desktop\demirnotes.exe"

REM Create data folder on Desktop
if not exist "%USERPROFILE%\Desktop\demirnotes" mkdir "%USERPROFILE%\Desktop\demirnotes"

echo ================================
echo Done! demirnotes.exe is on Desktop
echo ================================
pause
