@echo off
timeout /t 5 /nobreak
start "" /MAX "C:\Program Files\Google\Chrome\Application\chrome.exe" "https://pancakeswap.finance/prediction?token=BNB&chain=bsc"

timeout /t 5 /nobreak
call python "CORE\AUTORUN\B_log_in.py"

