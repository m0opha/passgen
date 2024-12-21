virtualenv .env
source .env/bin/activate
echo "start virutalenv"
pip install pyinstaller
pyinstaller --onefile -i NONE passgen.py
cp dist/passgen ~/bin
echo "[+]build done."
