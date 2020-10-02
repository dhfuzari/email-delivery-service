# Email delivery service

## Basic overview

Este projeto é composto por 6 serviços(containers) descritos em um arquivo descritor docker-compose.yml que trabalham em conjunto para fazer o envio de mensagens de email, de uma forma que seja possível escalar os serviços conforme necessário.

### Imagens individuais:

**db** container - [Imagem Postgres]() - Servidor de banco de dados Postgres para armazenamento das
mensagens de email enviadas pela aplicação no contianer app

**adminer** container - [Imagem Adminer]() - Serviço para gerencimanento de banco de dados, usado no projeto apenas
para acompanhamento dos dados armazenados no serviço de Banco de Dados. Este container
é opcional para o funcionamento dos serviços que compõem o descritor docker-compose.yml e
serve apenas para acompanhamento dos dados inseridos na tabela de emails

**frontend** container - [Imagem Nginx]() - Serviço que expoe na porta 80 um formulário web para preenchimento da
mensagem de e-mail e que atua como proxy reverso fazendo o roteamento da mensagem no
POST do formulário para a rota http://localhost/api, que é o serviço descrito na
Imagem Python(passo 4)

**app** container - [Imagem Python]() - É o serviço que recebe a mensagem via POST da aplicação web do container frontend,
insere a mensagem no Banco de dados criado no container 1, e envia essa mensagem para a fila criada do container queue

**queue** container - [Imagem Redis]() que está na mesma rede dos containers 4 e 6. Recebe as mensagens enviadas pelo
Serviço criado no container app e disponibiliza essa mensagens que são recuperadas pelo container worker que
faz o disparo dos emails.

**worker** container - [Imagem Worker]() - Imagem Python customizada com a instalação do Redis para leitura da fila de mensagens criada 
anteriormente no serviço do Redis(Container queuec

## Up and running

Clone the repo: 

Na pasta raiz do projeto, onde se encontra o arquivio docker-compose.yml, execute o comando: 
```
git clone git@github.com:dhfuzari/worker-email-sender.git
cd worker-email-sender
```
Para executar em modo daemon, com apenas umas instância do serviço worker, execute o comando:
```
docker-compose up -d
```
Se deseja escalar o serviço de email, com mais de um container, passe o numero de container necessários para o container worker:
```
docker-compose up -d --scale worker=3
```


### Comandos uteis

Para visualizar os logs de todos os containers em execução, execute o comando:
```
docker-compose logs -f -t
```

Lista todas as base de dados disponíveis no container db criado anteriormente
```
docker-compose exec db psql -U postgres -c '\l'
```

Executa o script de verificação check.sql que lista todas as base de dados, alterna a conexão para a base de dados email-sender, e exibe uma descrição da tabela emails
```
docker-compose exec db psql -U postgres -f /scripts/check.sql
```

Parar a execução de todos os containers listados no `docker-compose.yml` do diretório atual
```
docker-compose down
```

Faz um SELECT em todos os registros da tabela email no banco de dados email-sender no container db
```
docker-compose logs exec db psql -U postgres -d email_sender -c 'SELECT * FROM emails'
```

Exibe os logos de um container específico. No exemplo exibe os logs do container worker
```
docker-compose logs -f -t worker
```

Obs importante: o arquivo de inicialização do postgres /docker-entrypoint-initdb.d/init.sql só é 
executa quando o diretório /var/lib/postgresql/data da instancia estiver completamente vazio. Tenha
em mente que se precisar fazer alguma altração no script de inicialização criado, ele não executará 
novamente, pois o diretório /var/lib/postgresql/data não estará maia vazio depois da primeira execução
do container postgres e da execução do arquivo init.sql. Será necessário executar o comando 
docker-compose down -v para remover os containers e deletar o volume criado anteriormente

## Configuration

Os volumes e redes configurados estão descritos no prórpio arquivo docker-compose.yml. 

A porta padrão configurada para rodar
o serviço web no container frontend é a porta 80, portanto para sistemas Windows que possuem o IIS
habilitado rodando na porta 80 é necessário parar a execução do mesmo, para que a porta 80 seja
liberada para subir nosso servidor web Nginx 
Para isso, execute o seguinte comando para parar a execução do serviço de internet no windows
iisreset /stop

If necessary override some values, update then in `docker-compose.override.yml`

## Usage

Para iniciar o serviço com todos os containers, na pasta raiz do projeto execute o comando:




O serviço do adminer utilizado para acompanhamento dos dados inseridos no postgre pode está disponível atravéz da URL 
http://localhost:81. Os dados para acesso da instacia do Postgre criada no container adminer são:

System: Postgres
Server: localhost
User: postgres
Password: p@ssw0rd


## Authors and acknowledgment

## Project status

O projeto implementa todas as funcionalidades, porém não possui um servidor de smpt configurado e o envio do email está sendo simulado por uma 
função que implementa um temporizador randômico que faz a simulação da funcionalidade.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)





