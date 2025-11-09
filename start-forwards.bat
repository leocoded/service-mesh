@echo off
echo 🌐 Iniciando Port Forwards
echo.

echo Matando port-forwards anteriores...
taskkill /f /im kubectl.exe > nul 2>&1

echo Iniciando nuevos port-forwards...
start /B kubectl port-forward -n istio-system svc/kiali 20001:20001
start /B kubectl port-forward -n istio-system svc/grafana 3000:3000
start /B kubectl port-forward -n event-mesh svc/kafka-ui 30080:8080

echo Esperando conexiones...
timeout /t 5 /nobreak > nul

echo.
echo ✅ Port forwards activos!
echo.
echo 🌐 URLs disponibles:
echo   - Kiali:     http://localhost:20001
echo   - Grafana:   http://localhost:3000  
echo   - Kafka UI:  http://localhost:30080
echo.
pause