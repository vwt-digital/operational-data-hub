from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.storage import Storage

from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Legacy ERP system", graph_attr=graph_attr, show=False, filename="images/legacy_erp_system"):
    server_1 = Server("NaaB IV")
    webshop_1 = Client("Webshop")

    with Cluster("Operational Data Hub Platform"):
        with Cluster("Operational Data Hub"):
            with Cluster("Pub/Sub Topic"):
                pubsub_1 = PubSub("Subscription")

        with Cluster("Ingest Project"):
            function_1 = Functions("Restingest")
            function_2 = Functions("Produce delta event")
            scheduler_1 = Scheduler("Cloud Scheduler")
            storage_1 = Storage("GCS Bucket")

            scheduler_1 - Edge(label="Trigger", style="dotted") - function_1
            server_1 << Edge(label="GET", color="black") << function_1 >> storage_1
            storage_1 >> Edge(label="Bucket Trigger") >> function_2 >> Edge(label="Publish") >> pubsub_1

        with Cluster("Consume Project"):
            function_3 = Functions("Event sourcing consumer")
            database_1 = Firestore("Database")
            appengine_1 = AppEngine("API")

            pubsub_1 >> Edge(label="Subscribe") >> function_3 >> database_1

    database_1 << Edge(label="GET") << appengine_1 << Edge(label="REST - GET", color="black") << webshop_1
