from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import Bigquery, Dataflow, PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.database import Firestore
from diagrams.gcp.ml import AIPlatform

from diagrams.onprem.client import Client

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Data Science", graph_attr=graph_attr, show=False, filename="images/data_science"):
    webshop_1 = Client("Webshop")

    with Cluster("Operational Data Hub Platform"):
        with Cluster("Ingest Project"):
            function_1 = Functions("Ingest")

        with Cluster("Operational Data Hub"):
            with Cluster("Pub/Sub Topic X"):
                pubsub_1_1 = PubSub("Subscription XA")

            with Cluster("Pub/Sub Topic Z"):
                pubsub_2_1 = PubSub("Subscription ZA")

        with Cluster("Consume Project"):
            dataflow_1 = Dataflow("Dataflow")

            with Cluster("Analyze"):
                bigquery_1 = Bigquery("BigQuery")
                aiplatform_1 = AIPlatform("AI Platform")
                firestore_2 = Firestore("Database")
                dataflow_2 = Dataflow("Backfill/reprocess")

    pubsub_1_1 >> dataflow_1
    dataflow_1 >> bigquery_1 >> dataflow_2
    dataflow_1 >> aiplatform_1 >> dataflow_2
    dataflow_1 >> firestore_2 >> dataflow_2
    bigquery_1 >> Edge(label="Results", color="orange") >> function_1 >> Edge(color="orange") >> pubsub_2_1
    pubsub_2_1 >> Edge(label="Results", color="orange") >> webshop_1
