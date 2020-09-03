from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.database import Firestore
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.storage import Storage

from diagrams.onprem.compute import Server

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Customer support mailbox", graph_attr=graph_attr, show=False, filename="images/mailbox"):
    server_1 = Server("Mail server")

    with Cluster("Operational Data Hub"):
        with Cluster("Core"):
            pubsub_1 = PubSub("Pub/Sub Topic")

        with Cluster("Ingest"):
            schedule_1 = Scheduler("Cloud Scheduler")
            function_1 = Functions("EWS Mail Ingest")
            storage_1 = Storage("GCS Bucket")

        with Cluster("Consume"):
            function_2 = Functions("Consume")
            firestore_1 = Firestore("Database")

    schedule_1 - Edge(label="Trigger", style="dotted") - function_1
    function_1 >> Edge(label="REST - GET", color="black") >> server_1
    function_1 >> Edge(label="Publish", color="orange") >> pubsub_1
    function_1 >> Edge(label="POST") >> storage_1 >> Edge(label="GET", color="orange") >> function_2
    pubsub_1 >> Edge(label="Subscribe", color="orange") >> function_2 >> Edge(color="orange") >> firestore_1
