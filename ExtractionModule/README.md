I used Python 3.5 (should be fine for any Python 3 version)

You need to install pdfminer.six package first using the command:
pip install pdfminer.six

To run the code:

chcp 65001 (To activate the codec, it's a Windows thing, you only need to do it if you want to display the text on terminal for debugging purpose)
python extraction.py

For now, just use the files from "Well_technical_data/Daily Drilling Report - PDF Version" only
