from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import Bigquery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore
from diagrams.gcp.ml import AIPlatform

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Data Science", graph_attr=graph_attr, show=False, filename="images/data_science"):
    with Cluster("Webshop"):
        appengine_1 = AppEngine("Client")
        appengine_2 = AppEngine("API")
        firestore_1 = Firestore("Database")

    with Cluster("Operational Data Hub"):
        with Cluster("Ingest"):
            function_1 = Functions("Ingest")

        with Cluster("Core"):
            pubsub_1 = PubSub("Pub/Sub")

        with Cluster("Consume / enrich"):
            dataflow_1 = Dataflow("Dataflow")

    with Cluster("Analyze"):
        bigquery_1 = Bigquery("BigQuery")
        aiplatform_1 = AIPlatform("AI Platform")
        firestore_2 = Firestore("Database")
        dataflow_2 = Dataflow("Backfill/reprocess")

    pubsub_1 >> dataflow_1
    dataflow_1 >> bigquery_1 >> dataflow_2
    dataflow_1 >> aiplatform_1 >> dataflow_2
    dataflow_1 >> firestore_2 >> dataflow_2
    bigquery_1 >> Edge(label="Results", color="orange") >> function_1 >> Edge(color="orange") >> pubsub_1
    pubsub_1 >> Edge(color="orange") >> firestore_1
    appengine_1 << Edge(label="HTTPS", color="orange") << appengine_2 << Edge(color="orange") << firestore_1
