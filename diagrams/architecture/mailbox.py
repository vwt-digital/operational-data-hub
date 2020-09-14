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

with Diagram("Customer support mailbox", graph_attr=graph_attr, show=False, filename="images/mailbox"):
    server_1 = Server("Mail server")
    webshop_1 = Client("Webshop")

    with Cluster("Operational Data Hub Platform"):
        with Cluster("Operational Data Hub"):
            with Cluster("Pub/Sub Topic"):
                pubsub_1 = PubSub("Subscription")

        with Cluster("Ingest Project"):
            schedule_1 = Scheduler("Cloud Scheduler")
            function_1 = Functions("EWS Mail Ingest")
            storage_1 = Storage("GCS Bucket")

        with Cluster("Consume Project"):
            function_2 = Functions("Consume")
            firestore_1 = Firestore("Database")
            appengine_1 = AppEngine("API")

    schedule_1 - Edge(label="Trigger", style="dotted") - function_1
    function_1 >> Edge(label="REST - GET", color="black") >> server_1
    function_1 >> Edge(label="Publish", color="orange") >> pubsub_1
    function_1 >> storage_1 << Edge(label="GET", color="orange") << function_2
    pubsub_1 >> Edge(label="Subscribe", color="orange") >> function_2 >> Edge(color="orange") >> firestore_1
    firestore_1 << Edge(label="GET") << appengine_1 << Edge(label="REST - GET", color="black") << webshop_1
