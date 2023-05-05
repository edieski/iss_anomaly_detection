@echo off
:loop
python "C:\Users\litle\repos\iss_anomaly_detection\iss_data.py"
timeout /t 10 /nobreak
goto loop