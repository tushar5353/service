import json
import os
import logging

import asyncio
import confluent_kafka
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
from fastapi import FastAPI, HTTPException
from threading import Thread

from service.utils.config import Config

logger = logging.getLogger(os.environ["RUN_TYPE"])

config_obj = Config()
config = config_obj.get_config("environment")
kafka_config = {
    "bootstrap.servers": config["kafka"]["kafka_brokers"]    
        }
topic_info = config["kafka"]["topics"]

def create_topics():
    admin_client = AdminClient(kafka_config)
    print("Creating Kafka Topics")
    for key, value in topic_info.keys():
        new_topic = NewTopic(topic=value["name"][0],
                             num_partitions=value["partitions"],
                             replication_factor=value["replication_factor"])

        # Create topic if it does not exist
        futures = admin_client.create_topics([new_topic])
        
        for topic, f in futures.items():
            try:
                f.result()  # The result itself is None
                print(f"Topic {value['name']} created")
            except Exception as e:
                if "TopicAlreadyExistsError" in str(e):
                    print(f"Topic {value['name']} already exists")
                else:
                    print(f"Failed to create topic {value['name']}: {e}")

class AIOProducer:
    def __init__(self, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._producer = confluent_kafka.Producer(kafka_config)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value):
        """
        An awaitable produce method.
        """
        value = json.dumps(value).encode("utf-8")
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(result.set_exception, KafkaException(err))
            else:
                self._loop.call_soon_threadsafe(result.set_result, msg)
        self._producer.produce(topic, value, on_delivery=ack)
        return result

    def produce_with_delivery_notification(self, topic, value, on_delivery):
        """
        A produce method in which delivery notifications are made available
        via both the returned future and on_delivery callback (if specified).
        """
        logger.info(f"sending Event::{value} -> topic({topic})")
        value = json.dumps(value).encode("utf-8")
        result = self._loop.create_future()

        def ack(err, msg):
            if err:
                self._loop.call_soon_threadsafe(
                    result.set_exception, KafkaException(err))
            else:
                self._loop.call_soon_threadsafe(
                    result.set_result, msg)
            if on_delivery:
                self._loop.call_soon_threadsafe(
                    on_delivery, err, msg)
        self._producer.produce(topic, value, on_delivery=ack)
        return result
