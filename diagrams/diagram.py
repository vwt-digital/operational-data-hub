from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Cloud Pub/Sub", graph_attr=graph_attr, direction="TB", show=False, filename="cloud_pubsub"):
    with Cluster("Publishers"):
        pub_1 = Functions("Function")
        pub_2 = AppEngine("Application")

    with Cluster("Subscribers"):
        sub_1 = Functions("Function")
        sub_2 = Firestore("Database")
        sub_3 = AppEngine("Application")

    with Cluster("Pub/Sub"):
        with Cluster("Topic X"):
            sub_x1 = PubSub("Subscription X.1")
            sub_x2 = PubSub("Subscription X.2")

        with Cluster("Topic Y"):
            sub_y1 = PubSub("Subscription Y.1")

    pub_1 >> sub_x1 >> [sub_1, sub_2]
    pub_1 >> sub_x2 >> sub_3
    pub_2 >> sub_y1 >> [sub_1, sub_3]
