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

with Diagram("Current Stock", graph_attr=graph_attr, show=False, filename="images/current_stock"):
    server_1 = Server("Third-party API")
    server_2 = Server("Third-party API")
    server_3 = Server("Third-party API")
    webshop_1 = Client("Webshop")

    with Cluster("Operational Data Hub Platform"):
        with Cluster("Operational Data Hub"):
            with Cluster("Pub/Sub Topic X"):
                pubsub_1 = PubSub("Subscription XA")

            with Cluster("Pub/Sub Topic Y"):
                pubsub_2 = PubSub("Subscription YA")

        with Cluster("Ingest Project"):
            function_1 = Functions("Restingest")
            function_2 = Functions("Produce delta event")
            storage_1 = Storage("GCS Bucket")

            function_1 >> storage_1
            storage_1 - Edge(label="Bucket Trigger", style="dashed") - function_2

        with Cluster("Consume Project"):
            function_3 = Functions("Consume")

    server_1 >> Edge(label="REST - POST", color="blue") >> function_1
    server_2 >> Edge(label="REST - POST", color="orange") >> function_1
    server_3 >> Edge(label="REST - POST", color="orange") >> function_1
    function_2 >> Edge(label="Publish", color="blue") >> pubsub_1 >> Edge(label="Subscribe", color="blue") >> function_3
    function_2 >> Edge(label="Publish", color="orange") >> pubsub_2 >> Edge(label="Subscribe", color="orange") >> function_3
    function_3 >> Edge(label="REST - POST", color="black") >> webshop_1
