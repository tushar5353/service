import argparse
import os
import sys
import json
import logging

from confluent_kafka import Consumer, KafkaException

from service.utils import utils
from service.utils.config import Config
from service.utils.logs import configure_logging
from service.lib import orders

config_obj = Config()
env_config = config_obj.get_config("environment")
configure_logging()
logger = logging.getLogger(os.environ["RUN_TYPE"])

def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    logger.info(f'KAFKA Stats: {stats_json}')


def print_usage_and_exit(program_name):
    sys.stderr.write('Usage: %s [options..] <bootstrap-brokers> <group> <topic1> <topic2> ..\n' % program_name)
    options = '''
 Options:
  -T <intvl>   Enable client statistics at specified interval (ms)
'''
    sys.stderr.write(options)
    sys.exit(1)

def start_consuming(consumer_config, topics):
    consumer = Consumer(consumer_config)

    def print_assignment(consumer, partitions):
        print('Assignment:', partitions)

    consumer.subscribe(topics, on_assign=print_assignment)

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                try:
                    job_id=None
                    # Proper message
                    logger.info(f"{msg.topic()} {msg.partition()} {msg.offset()} {msg.key()}")
                    event_data = json.loads(msg.value().decode('utf-8'))
                    logger.info(f"{event_data}")
                    info = event_data["context"]

                    event_type = event_data["event_type"]

                    if event_type = "new_order":
                        orders.new(info["user_id"], info["product"], info["quantity"])

                    # Store the offset associated with msg to a local cache.
                    # Stored offsets are committed to Kafka by a background thread every 'auto.commit.interval.ms'.
                    # Explicitly storing offsets after processing gives at-least once semantics.
                    logger.info(f"Commiting the offset for event")
                    consumer.store_offsets(msg)

                    logger.info(f"SUCCESS:  Time Taken - {execution_time} seconds")
                except Exception as e:
                    logger.error(f"Failed to process event. An exception occurred :: {e}", exc_info=True)
                    logger.info("commiting offset")
                    consumer.store_offsets(msg)

    except Exception as e:
        logger.info(f'Exception::{e}', exc_info=True)

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic-name", required=True) 
    args = parser.parse_args()
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {'bootstrap.servers': env_config["kafka"]["kafka_brokers"],
            'group.id': env_config[args.report_type]["kafka_config"]["group_id"],
            'session.timeout.ms': env_config[args.report_type]["kafka_config"]["session_timeout"],
            'auto.offset.reset': env_config[args.report_type]["kafka_config"]["auto_offset_reset"],
            'enable.auto.offset.store': env_config[args.report_type]["kafka_config"]["enable_auto_offset_store"],
            'max.poll.interval.ms': env_config[args.report_type]["kafka_config"]["max_poll"]}
    start_consuming(conf, env_config[args.report_type]["kafka_config"]["topics"])
