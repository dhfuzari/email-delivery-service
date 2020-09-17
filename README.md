# worker-email-sender
E-mail worker sender

Comando para parar a execução do serviço de internet no windows que ouve a porta 80 por padrão: 
iisreset /stop

DB container
run.sh -> Script para subir um serviço de banco de dados e inspecionar os databases disponíveis
docker-compose up -d
docker-compose ps
echo "Aguardando a carga do postgres"
sleep 5
docker-compose exec db psql -U postgres -c '\l'
docker-compose down

DB container
run.sh -> Script de verificação do banco de dados criado
docker-compose up -d
docker-compose ps
echo "Aguardando a carga do postgres"
sleep 5
docker-compose exec db psql -U postgres -f /scripts/check.sql
docker-compose down

COMPOSE
run.sh -> Script para executar os logs de todos os containers
docker-compose up -d
docker-compose logs -f -t





