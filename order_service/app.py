
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import pika

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)

    class Order(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer)
        product = db.Column(db.String(50))
        quantity = db.Column(db.Integer)

    @app.route('/orders', methods=['POST'])
    def create_order():
        data = request.get_json()
        new_order = Order(user_id=data['user_id'], product=data['product'], quantity=data['quantity'])
        db.session.add(new_order)
        db.session.commit()
        # Send message to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='orders')
        channel.basic_publish(exchange='', routing_key='orders', body=str(data))
        connection.close()
        return jsonify({'message': 'Order created'}), 201

    return app
