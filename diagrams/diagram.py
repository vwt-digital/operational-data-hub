from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Functions

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Cloud Pub/Sub", graph_attr=graph_attr, show=False, filename="cloud_pubsub"):
    pubsub = PubSub("pubsub")

    with Cluster("Input"):
        input = [Functions("App"),
                 Functions("App"),
                 Functions("App")]

    with Cluster("Output"):
        output = [Functions("App"),
                  Functions("App"),
                  Functions("App")]

    input >> pubsub >> output
