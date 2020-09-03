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

with Diagram("Legacy ERP system", graph_attr=graph_attr, show=False, filename="images/legacy_erp_system"):
    server_1 = Server("NaaB IV")

    with Cluster("Operational Data Hub"):
        with Cluster("Core"):
            pubsub_1 = PubSub("Pub/Sub Topic")

        with Cluster("Ingest"):
            function_1 = Functions("Restingest")
            function_2 = Functions("Produce delta event")
            scheduler_1 = Scheduler("Cloud Scheduler")
            storage_1 = Storage("GCS Bucket")

            scheduler_1 - Edge(label="Trigger", style="dotted") - function_1
            server_1 << Edge(label="GET", color="black") << function_1 >> storage_1
            storage_1 >> Edge(label="Bucket Trigger") >> function_2 >> Edge(label="Publish") >> pubsub_1

        with Cluster("Consume"):
            function_3 = Functions("Event sourcing consumer")
            database_1 = Firestore("Database")

            pubsub_1 >> Edge(label="Subscribe") >> function_3 >> database_1
