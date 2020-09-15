from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.storage import Storage

from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram(
        "Posting third-party license data", graph_attr=graph_attr, show=False,
        filename="images/renewal_licenses_posting"):
    webshop_1 = Client("Webshop")
    server_1_1 = Server("Abode API")

    with Cluster("Operational Data Hub Platform"):
        with Cluster("Operational Data Hub"):
            with Cluster("Pub/Sub Topic"):
                pubsub_1_1 = PubSub("Subscription")

        with Cluster("Ingest Project"):
            function_1_1 = Functions("Restingest")
            function_1_2 = Functions("Produce delta event")
            storage_1_1 = Storage("GCS Bucket")

            function_1_1 >> storage_1_1
            storage_1_1 - Edge(label="Bucket Trigger", style="dashed") - function_1_2 >> Edge(label="Publish") >> pubsub_1_1

        with Cluster("Consume Project"):
            function_1_3 = Functions("Consume")

    webshop_1 >> Edge(label="POST", color="black") >> function_1_1
    pubsub_1_1 >> Edge(label="Subscribe") >> function_1_3 >> Edge(label="POST", color="black") >> server_1_1


with Diagram(
        "Receive third-party license data", graph_attr=graph_attr, show=False,
        filename="images/renewal_licenses_receiving"):
    webshop_2 = Client("Webshop")
    server_2_1 = Server("Abode API")

    with Cluster("Operational Data Hub Platform"):
        with Cluster("Operational Data Hub"):
            with Cluster("Pub/Sub Topic"):
                pubsub_2_1 = PubSub("Subscription")

        with Cluster("Ingest Project"):
            function_2_1 = Functions("Restingest")
            function_2_2 = Functions("Produce delta event")
            storage_2_1 = Storage("GCS Bucket")

            function_2_1 >> storage_2_1
            storage_2_1 - Edge(label="Bucket Trigger", style="dashed") - function_2_2 >> Edge(label="Publish") >> pubsub_2_1

        with Cluster("Consume Project"):
            function_2_3 = Functions("Consume")

    server_2_1 >> Edge(label="POST", color="black") >> function_2_1
    pubsub_2_1 >> Edge(label="Subscribe") >> function_2_3 >> Edge(label="POST", color="black") >> webshop_2
