from diagrams import Cluster, Diagram, Edge

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import ComputeEngine, Functions
from diagrams.gcp.database import SQL
from diagrams.gcp.devtools import Build
from diagrams.onprem.vcs import Github

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Available Data", graph_attr=graph_attr, show=False, filename="images/available_data"):
    github_1 = Github("GitHub repo")

    with Cluster("Operational Data Hub Platform"):
        with Cluster("Operational Data Hub"):
            with Cluster("Pub/Sub Topic"):
                pubsub_1 = PubSub("Subscription")

        with Cluster("Ingest Project"):
            function_1 = Build("Cloud Build")

        with Cluster("Consume Project"):
            function_2 = Functions("Consume catalog")

            with Cluster("CKAN"):
                computeengine_1 = ComputeEngine("CKAN VM")
                sql_1 = SQL("PostgreSQL")

    github_1 >> Edge(label="Build Trigger", color="black") >> function_1 >> Edge(label="Publish") >> pubsub_1
    pubsub_1 >> Edge(label="Subscribe") >> function_2 >> sql_1
    sql_1 >> Edge(label="SSL") >> computeengine_1
