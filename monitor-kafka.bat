@echo off
echo 🔍 Monitor de Eventos Kafka - Service Mesh
echo.

echo 📋 Topics disponibles:
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list
echo.

echo 🎯 Creando topics necesarios si no existen...
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic medicine.lote.created --partitions 1 --replication-factor 1 --if-not-exists
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic oracle.validation.completed --partitions 1 --replication-factor 1 --if-not-exists
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic blockchain.record.created --partitions 1 --replication-factor 1 --if-not-exists
echo.

echo 🚀 Iniciando monitores en ventanas separadas...
echo.

start "Kafka - Lotes Creados" cmd /k "docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic medicine.lote.created --from-beginning"

start "Kafka - Validaciones Oracle" cmd /k "docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic oracle.validation.completed --from-beginning"

start "Kafka - Registros Blockchain" cmd /k "docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic blockchain.record.created --from-beginning"

echo ✅ Monitores iniciados!
echo.
echo 💡 Ahora ejecuta ./generar-trafico.bat para ver los eventos en tiempo real
echo.
pause