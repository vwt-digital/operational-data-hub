from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.storage import Storage

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}


def generate_diagram(name):
    if name == 'service_pubsub':
        with Diagram("Cloud Pub/Sub", graph_attr=graph_attr, show=False, filename="images/service_pubsub"):
            with Cluster("Publishers"):
                pub_1 = Functions("Function")
                pub_2 = AppEngine("Application")

            with Cluster("Subscribers"):
                sub_1 = Functions("Function")
                sub_2 = Firestore("Database")
                sub_3 = AppEngine("Application")

            with Cluster("Pub/Sub"):
                with Cluster("Topic X"):
                    sub_x1 = PubSub("Subscription X.1")
                    sub_x2 = PubSub("Subscription X.2")

                with Cluster("Topic Y"):
                    sub_y1 = PubSub("Subscription Y.1")

            pub_1 >> sub_x1 >> [sub_1, sub_2]
            pub_1 >> sub_x2 >> sub_3
            pub_2 >> sub_y1 >> [sub_1, sub_3]

    if name == 'backup_pubsub':
        with Diagram("Pub/Sub backup", graph_attr=graph_attr, show=False, filename="images/backup_pubsub"):
            with Cluster("Backup process"):
                pub = PubSub("Pub/Sub Topic")
                func = Functions("Cloud Function")
                stg = Storage("Storage bucket")

            sch = Scheduler("Cloud Scheduler")

            pub >> Edge(label="Pull") >> func >> stg
            sch >> Edge(style="dashed", label="Subscription name") >> func


for diagram in ['service_pubsub', 'backup_pubsub']:
    generate_diagram(diagram)
