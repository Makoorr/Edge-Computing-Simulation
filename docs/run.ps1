# Stop-Process -Name mosquitto

Start-Process -FilePath "C:\Program Files\mosquitto\mosquitto.exe" -ArgumentList '-v -c "C:\Program Files\mosquitto\mosquitto.conf"' -NoNewWindow -Wait
