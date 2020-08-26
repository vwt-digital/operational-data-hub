from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Message Queue", graph_attr=graph_attr, show=False, filename="images/message_queue"):
    with Cluster("Producers"):
        pub_1 = Functions("Function")
        pub_2 = AppEngine("Application")

    with Cluster("Consumers"):
        sub_1 = Functions("Function")
        sub_2 = Firestore("Database")
        sub_3 = AppEngine("Application")

    with Cluster("Message queue"):
        sub_x = PubSub("Queue X")
        sub_y = PubSub("Queue Y")
        sub_z = PubSub("Queue Z")

    pub_1 >> sub_x >> [sub_1, sub_2]
    pub_1 >> sub_z >> sub_3
    pub_2 >> sub_y >> [sub_1, sub_3]
