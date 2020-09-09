create database worker_email_sender;

\c worker_email_sender

create table emails(
    id serial not null,
    data timestamp not null default current_timestamp,
    assunto varchar(100) not null,
    mensagem varchar(250) not null
)