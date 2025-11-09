@echo off
echo ========================================
echo TRAFICO CON PUERTOS 8XXX CORRECTOS
echo ========================================

echo.
echo Esperando que los pods se inicien...
timeout /t 20 /nobreak >nul

echo.
echo Generando trafico intensivo con puertos 8xxx...
for /l %%i in (1,1,100) do (
    echo [%%i/100] Trafico intensivo...
    curl -s "http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-producto:8003/proxy/" > nul
    curl -s "http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-bodega:8001/proxy/" > nul
    curl -s "http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-lote:8002/proxy/" > nul
    curl -s "http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-blockchain:8007/proxy/" > nul
    curl -s "http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-analytics:8010/proxy/" > nul
    timeout /t 0.5 /nobreak >nul
)

echo.
echo ========================================
echo URLs FINALES 8XXX:
echo MS-Producto: http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-producto:8003/proxy/
echo MS-Bodega: http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-bodega:8001/proxy/
echo MS-Lote: http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-lote:8002/proxy/
echo MS-Blockchain: http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-blockchain:8007/proxy/
echo MS-Analytics: http://localhost:8001/api/v1/namespaces/service-mesh/services/ms-analytics:8010/proxy/
echo.
echo Kiali: http://localhost:20001
echo ========================================
echo REVISA KIALI - Deberia mostrar VERDE
echo ========================================
pause