from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.database import Firestore

from diagrams.onprem.client import Client
from diagrams.gcp.compute import Functions
from diagrams.generic.storage import Storage

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("CQRS models", graph_attr=graph_attr, show=False, filename="images/cqrs_models"):
    with Cluster("Operational Data Hub platform"):
        firestore_1_1 = Firestore("Database")

        with Cluster("API"):
            with Cluster("CQRS Model"):
                cqrs_1_1 = Storage("Query Model")
                cqrs_1_2 = Storage("Command Model")

    webshop_1 = Client("Webshop")

    firestore_1_1 >> Edge(color="orange") >> cqrs_1_1 >> Edge(color="orange") >> \
        Edge(label="Presentation updates", color="orange") >> webshop_1
    webshop_1 >> Edge(label="User changes") >> cqrs_1_2 >> firestore_1_1

with Diagram("ODH CQRS integration", graph_attr=graph_attr, show=False, filename="images/cqrs_odh_model"):
    with Cluster("Operational Data Hub Platform"):
        with Cluster("Operational Data Hub"):
            with Cluster("Pub/Sub Topic Z"):
                pubsub_2_1 = PubSub("Subscription ZX")
                pubsub_2_2 = PubSub("Subscription ZY")

        with Cluster("Consume Project X"):
            consume_2_1 = Functions("Consume X")
            firestore_2_1 = Firestore("Database X")

            with Cluster("CQRS Model"):
                cqrs_2_1 = Storage("Query Model")

            consume_2_1 >> firestore_2_1 >> cqrs_2_1

        with Cluster("Consume Project Y"):
            consume_2_2 = Functions("Consume Y")
            firestore_2_2 = Firestore("Database Y")

            with Cluster("CQRS Model"):
                cqrs_2_2 = Storage("Query Model")

            consume_2_2 >> firestore_2_2 >> cqrs_2_2

    pubsub_2_1 >> consume_2_1
    pubsub_2_2 >> consume_2_2
