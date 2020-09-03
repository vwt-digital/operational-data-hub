from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore

from diagrams.onprem.compute import Server

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram(
        "Posting third-party license data", graph_attr=graph_attr, show=False,
        filename="images/renewal_licenses_posting"):
    server_1_1 = Server("Abode API")

    with Cluster("Webshop"):
        with Cluster("Ingest"):
            appengine_1_1 = AppEngine("Client")
            appengine_1_2 = AppEngine("API")
            firestore_1_1 = Firestore("Database")

    with Cluster("Operational Data Hub"):
        with Cluster("Core"):
            pubsub_1_1 = PubSub("Pub/Sub Topic")

        with Cluster("Consume"):
            function_1_1 = Functions("Consume")

        appengine_1_1 >> Edge(label="HTTPS") >> appengine_1_2 >> firestore_1_1
        appengine_1_2 >> pubsub_1_1 >> function_1_1 >> \
            Edge(label="REST") >> server_1_1


with Diagram(
        "Receive third-party license data", graph_attr=graph_attr, show=False,
        filename="images/renewal_licenses_receiving"):
    server_2_1 = Server("Abode API")

    with Cluster("Operational Data Hub"):
        with Cluster("Core"):
            pubsub_2_1 = PubSub("Pub/Sub Topic")

        with Cluster("Ingest"):
            function_2_1 = Functions("Restingest")

        with Cluster("Consume"):
            function_2_2 = Functions("Consume")

    with Cluster("Webshop"):
        firestore_2_1 = Firestore("Database")
        appengine_2_1 = AppEngine("API")
        appengine_2_2 = AppEngine("Client")

    server_2_1 >> Edge(label="REST") >> function_2_1 >> pubsub_2_1
    pubsub_2_1 >> function_2_2 >> firestore_2_1
    firestore_2_1 >> appengine_2_1 >> Edge(label="HTTPS") >> appengine_2_2
