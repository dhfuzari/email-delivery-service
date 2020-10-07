# Email delivery service

![alt](./mail-book.png)

## Basic overview

This project consists of 6 services (containers) described in a `docker-compose.yml` descriptor file that works together to send email messages, in a way that it is possible to scale the services as needed.

### Imagens individuais:

* **db** container([Postgres](https://hub.docker.com/_/postgres)) - Postgres database server for storing email messages sent by the application in the **app** contianer.

* **adminer** container([Adminer](https://hub.docker.com/_/adminer)) - Database management service, used in the project only to monitor the databased stored in the **db** service. It's an optional service and it's just for monitoring the inserted data from `emails` table.

* **frontend** container([Nginx](https://hub.docker.com/_/nginx)) - A web service that exposes in the door 80 a web form that allows user fill out an email message, and it also acts like a reverse proxy, routing the posted form message to the http://localhost/api route, which is the service described in the **app** container.

* **app** container([Python](https://hub.docker.com/_/python)) - It's the service that recieves a message via POST from **frontend** container, inserts the message at the **db** container database created earlier, and then send this message to the queue from **queue** container

* **queue** container([Redis](https://hub.docker.com/_/redis)) - Recieves the messages created by **app** container, then this messages are available to be retrieved by the **worker** container, which will trigger the emails later.

* **worker** container([Worker](https://hub.docker.com/_/python)) - A custom Python image with Redis, to read and recieve messages from **queue** container, and then send the email message throught a smtp server. This is the container that could be scaled as soon as needed, using the flag `--scale` as described in the next section "Up and running". 


## Up and running

1) Clone the repo: `git clone git@github.com:dhfuzari/email-delivery-service.git` 

2) Open the root folder: `cd email-delivery-service`

3) To execute the services in daemon mode, with only one **worker** container instance, run the command:  
    ```
    docker-compose up -d
    ```
    If you want to scalate the number of **worker** containers, then use the `--scale` flag and assign the number of containers you wish to the containers name. In the example, we'll have 3 **worker** containers working in parallel:
    ```
    docker-compose up -d --scale worker=3
    ```

4) Navigate to http://localhost:80

5) Fill the form with requested data and click on send 

4) The adminer service used to track email data stored in Postgres is available via the URL http://localhost:81. To authenticate in it, use the followind credentials:

    System: *Postgres*  
    Server: *localhost*  
    User: *postgres*  
    Password: *p@ssw0rd*  

### Useful commands:

To view logs for all running containers: 
```
docker-compose logs -f -t
```

List all available databases from **db** container
```
docker-compose exec db psql -U postgres -c '\l'
```

Run the check.sql script tha list all databases, set the current conexion to `email-sender` database, and displays a complete emails talbes description 
```
docker-compose exec db psql -U postgres -f /scripts/check.sql
```

Stop containers services defined in the compose file
```
docker-compose down
```

Performs a SELECT for all records at email's table in the email-sender database, at **db** container
```
docker-compose logs exec db psql -U postgres -d email_sender -c 'SELECT * FROM emails'
```

Displays logs information about a specific container. In the example displays logs from **worker** container
```
docker-compose logs -f -t worker
```

## Configuration

The volumes and networks are described in `docker-compose.yml` file, each one in it's own service details.

The default setup to run the web service in the **frontend** container is the door 80, therefore for Microsoft Windows system with IIS up and running at door 80, it'll be
necessary to stop it's execution, to release the door 80 to our Nginx container. To achieve this, you need to run the following command:
```
iisreset /stop
```

Important note: The initialization Postgres file `/docker-entrypoint-initdb.d/init.sql` is executed only when the path `/var/lib/postgresql/data` from instance is completely empty. Keep in mind that if you need to update the initialization script created earlier, it'll not execute again with the new update, because the path `/var/lib/postgresql/data` is no longer empty after the first **db** container execution, and after the `init.sql` file execution. It's necessary execute the following comand to remove containers and delete the volume created earlier:
```
docker-compose down -v
```

If necessary override some values, update then in `docker-compose.override.yml`

Environment variables:

* `DB_HOST=db`
* `DB_USER=postgres`
* `DB_PASSWORD=p@ssw0rd`
* `DB_NAME=email_sender`
* `REDIS_HOST=queue`
 
## Project status

The project implements all funcionallities, however it doesn't have an smtp server configured, so the sending of the email is being simulated by a function tha implements a random timer that mimic the email delivery. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)