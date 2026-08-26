Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c python -m streamlit run app.py --server.headless true", 0, False