import psycopg2
import redis
import json
import os
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)

        redis_host = os.getenv('REDIS_HOST')
        self.redisQueue = redis.StrictRedis(host=redis_host, port=6379, db=0)

        db_host = os.getenv('DB_HOST')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')
        dsn = f'dbname={db_name} user={db_user} password={db_password} host={db_host}'

        self.conn = psycopg2.connect(dsn)

    def register_mensage(self, assunto, mensagem):
        SQL = 'INSERT INTO emails(assunto, mensagem) VALUES(%s, %s)'
        cur = self.conn.cursor()
        cur.execute(SQL, (assunto, mensagem))
        self.conn.commit()
        cur.close()
        
        # Send mensage to redis
        msg = { 'assunto': assunto, 'mensagem': mensagem }
        self.redisQueue.rpush('sender', json.dumps(msg))

        print('Mensagem registrada no SQL e no Redis')

    def send(self):
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')
        self.register_mensage(assunto, mensagem)
        return 'Mensagem enfileirada! Assunto: {} Mensagem: {}'.format(assunto, mensagem)

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)