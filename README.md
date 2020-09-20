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

Dados de acesso para o adminer
POSTGRES_PASSWORD: p@ssw0rd
POSTGRES_USER: postgres

COMPOSE
run.sh -> Script para executar os logs de todos os containers
docker-compose up -d
docker-compose logs -f -t

run.sh -> Script para verificar se o e-mail foi registrado no banco de dados
docker-compose up -d
docker-compose logs exec db psql -U postgres -d email_sender -c 'SELECT * FROM emails'

run.sh -> Script para executar o compose com 3 instancias do container  "worker"
docker-compose up -d --scale worker=3


Obs importante: o arquivo de inicialização do postgres /docker-entrypoint-initdb.d/init.sql só é 
executa quando o diretório /var/lib/postgresql/data da instancia estiver completamente vazio. Tenha
em mente que se precisar fazer alguma altração no script de inicialização criado, ele não executará 
novamente, pois o diretório /var/lib/postgresql/data não estará maia vazio dois da primeira execução
do container postgres e da execução do arquivo init.sql. Será necessário executar o comando 
docker-compose down -v para remover os containers e deletar o volume criado anteriormente






