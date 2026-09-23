""" import random
import uuid
import json
from datetime import datetime, timedelta

from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
import logging
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
import os

# Pulling Data Generator Function
from data import generate_uber_ride_confirmation

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
EVENT_HUBNAME = os.getenv("EVENT_HUBNAME")




def send_to_event_hub(ride_data=None, batch_size=1):

    try:
        # Initialize Event Hub Producer Client
        producer = EventHubProducerClient.from_connection_string(
            CONNECTION_STRING,
            eventhub_name=EVENT_HUBNAME
        )
        
        # Prepare ride records
        ride_json = json.dumps(ride_data) 
        
        # Create batch of events
        event_batch = producer.create_batch()

            
        # Create event with ride data 
        event = EventData(ride_json)
            
        # Add event to batch
        event_batch.add(event)

        # Send batch to Event Hub
        producer.send_batch(event_batch)
        
        producer.close()

        return "Successfully sent to Event Hub"
        
    except Exception as e:
        print(f"Error sending data to Event Hub: {str(e)}")
        return False



if __name__ == "__main__":
    
    print("=" * 80)
    print("SINGLE RIDE CONFIRMATION")
    print("=" * 80)
    ride = generate_uber_ride_confirmation()
    print(json.dumps(ride, indent=2))

    
    print("\n" + "=" * 80)
    print("SENDING SINGLE RIDE TO EVENT HUB")
    result = send_to_event_hub(ride)
    print(f"Single ride sent to Event Hub: {result}")
    
    """

"""
import random
import uuid
import json
import time
from datetime import datetime, timedelta

from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
import logging
from dotenv import load_dotenv

load_dotenv()

import os

# Pulling Data Generator Function
from data import generate_uber_ride_confirmation


CONNECTION_STRING = os.getenv("CONNECTION_STRING")
EVENT_HUBNAME = os.getenv("EVENT_HUBNAME")


def send_to_event_hub(producer, ride_data=None, batch_size=1):

    try:
        # Prepare ride record
        ride_json = json.dumps(ride_data)

        # Create batch of events
        event_batch = producer.create_batch()

        # Create event with ride data
        event = EventData(ride_json)

        # Add event to batch
        event_batch.add(event)

        # Send batch to Event Hub
        producer.send_batch(event_batch)

        return True

    except Exception as e:
        print(f"Error sending data to Event Hub: {str(e)}")
        return False


if __name__ == "__main__":

    print("=" * 80)
    print("UBER RIDE DATA GENERATOR")
    print("Target Rate: 1000 EVENTS PER SECOND")
    print("Press Ctrl+C to stop")
    print("=" * 80)

    # Initialize Event Hub Producer ONCE
    producer = EventHubProducerClient.from_connection_string(
        CONNECTION_STRING,
        eventhub_name=EVENT_HUBNAME
    )

    count = 0

    try:

        while True:

            # Start time for this 1-second window
            start_time = time.time()

            # Send 1000 events
            for i in range(1000):

                # Generate Uber ride data
                ride = generate_uber_ride_confirmation()

                # Send to Event Hub
                result = send_to_event_hub(
                    producer,
                    ride
                )

                if result:
                    count += 1

            # Calculate how long sending took
            elapsed_time = time.time() - start_time

            # If sending took less than 1 second,
            # wait for the remaining time
            if elapsed_time < 1:
                time.sleep(1 - elapsed_time)

            print(
                f"Events sent in current second: 1000 | "
                f"Total events sent: {count}"
            )

    except KeyboardInterrupt:

        print("\nStopping data generator...")

    finally:

        producer.close()

        print("=" * 80)
        print("DATA GENERATOR STOPPED")
        print(f"Total events sent: {count}")
        print("=" * 80)
        """
import random
import uuid
import json
import time
from datetime import datetime, timedelta

from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
import logging
from dotenv import load_dotenv

load_dotenv()

import os

# Pulling Data Generator Function
from data import generate_uber_ride_confirmation


CONNECTION_STRING = os.getenv("CONNECTION_STRING")
EVENT_HUBNAME = os.getenv("EVENT_HUBNAME")


def send_to_event_hub(producer, ride_data=None, batch_size=1):

    try:
        # Prepare ride record
        ride_json = json.dumps(ride_data)

        # Create batch of events
        event_batch = producer.create_batch()

        # Create event with ride data
        event = EventData(ride_json)

        # Add event to batch
        event_batch.add(event)

        # Send batch to Event Hub
        producer.send_batch(event_batch)

        return True

    except Exception as e:
        print(f"Error sending data to Event Hub: {str(e)}")
        return False


if __name__ == "__main__":

    print("=" * 80)
    print("UBER RIDE DATA GENERATOR")
    print("Target Rate: 1 EVENT EVERY 5 SECONDS")
    print("Press Ctrl+C to stop")
    print("=" * 80)

    # Initialize Event Hub Producer ONCE
    producer = EventHubProducerClient.from_connection_string(
        CONNECTION_STRING,
        eventhub_name=EVENT_HUBNAME
    )

    count = 0

    try:

        while True:

            # Generate Uber ride data
            ride = generate_uber_ride_confirmation()

            # Send event to Event Hub
            result = send_to_event_hub(
                producer,
                ride
            )

            if result:
                count += 1
                print(
                    f"Event sent successfully | "
                    f"Total events sent: {count}"
                )

            # Wait 5 seconds before sending next event
            time.sleep(5)

    except KeyboardInterrupt:

        print("\nStopping data generator...")

    finally:

        producer.close()

        print("=" * 80)
        print("DATA GENERATOR STOPPED")
        print(f"Total events sent: {count}")
        print("=" * 80)