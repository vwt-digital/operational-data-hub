from diagrams import Cluster, Diagram

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Message Queue", graph_attr=graph_attr, show=False, filename="images/message_queue"):
    with Cluster("Operational Data Hub"):
        with Cluster("Ingest"):
            publisher_1 = Functions("Function")
            publisher_2 = AppEngine("Application")

        with Cluster("Consume"):
            subscriber_1 = Functions("Function")
            subscriber_2 = Firestore("Database")
            subscriber_3 = AppEngine("Application")

        with Cluster("Core"):
            queue_1 = PubSub("Queue X")
            queue_2 = PubSub("Queue Y")
            queue_3 = PubSub("Queue Z")

    publisher_1 >> queue_1 >> [subscriber_1, subscriber_2]
    publisher_1 >> queue_3 >> subscriber_3
    publisher_2 >> queue_2 >> [subscriber_1, subscriber_3]
