from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore

from diagrams.onprem.compute import Server

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Current Stock", graph_attr=graph_attr, show=False, filename="images/current_stock"):
    server_1 = Server("Third-party API")
    server_2 = Server("Third-party API")
    server_3 = Server("Third-party API")

    with Cluster("Operational Data Hub"):
        with Cluster("Core"):
            pubsub_1 = PubSub("Pub/Sub Topic")

        with Cluster("Ingest"):
            function_1 = Functions("Restingest")

        with Cluster("Consume"):
            function_2 = Functions("Consume")

    with Cluster("Webshop"):
        firestore_1 = Firestore("Database")
        appengine_1 = AppEngine("API")
        appengine_2 = AppEngine("Client")

    server_1 >> Edge(label="REST") >> function_1
    server_2 >> Edge(label="REST") >> function_1
    server_3 >> Edge(label="REST") >> function_1
    function_1 >> pubsub_1 >> function_2 >> firestore_1
    firestore_1 >> appengine_1 >> Edge(label="HTTPS") >> appengine_2
