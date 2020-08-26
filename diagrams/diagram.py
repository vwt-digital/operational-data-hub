from diagrams import Cluster, Diagram, Edge
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import Firestore
from diagrams.gcp.storage import Storage
from diagrams.gcp.devtools import Scheduler
from diagrams.onprem.compute import Server

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Message Queue", graph_attr=graph_attr, show=False, filename="images/message_queue"):
    with Cluster("Producers"):
        pub_1 = Functions("Function")
        pub_2 = AppEngine("Application")

    with Cluster("Consumers"):
        sub_1 = Functions("Function")
        sub_2 = Firestore("Database")
        sub_3 = AppEngine("Application")

    with Cluster("Message queue"):
        sub_x = PubSub("Queue X")
        sub_y = PubSub("Queue Y")
        sub_z = PubSub("Queue Z")

    pub_1 >> sub_x >> [sub_1, sub_2]
    pub_1 >> sub_z >> sub_3
    pub_2 >> sub_y >> [sub_1, sub_3]


with Diagram("Legacy ERP system", graph_attr=graph_attr, show=False, filename="images/legacy_erp_system"):
    dia_1_baan = Server("BaaN IV")

    with Cluster("Operational Data Hub"):
        dia_1_pubsub = PubSub("Pub/Sub Topic")

        with Cluster("Consume"):
            dia_1_rest = Functions("Restingest")
            dia_1_schedule = Scheduler("Cloud Scheduler")
            dia_1_storage = Storage("GCS Bucket")
            dia_1_delta = Functions("Produce delta event")

            dia_1_schedule - Edge(label="Trigger", style="dotted") - dia_1_rest
            dia_1_baan << Edge(label="GET", color="black") << dia_1_rest >> dia_1_storage
            dia_1_storage >> Edge(label="Bucket Trigger") >> dia_1_delta >> Edge(label="Publish") >> dia_1_pubsub

        with Cluster("Ingest"):
            dia_1_cons = Functions("Event sourcing consumer")
            dia_1_database = Firestore("Database")

            dia_1_pubsub >> Edge(label="Subscribe") >> dia_1_cons >> dia_1_database
