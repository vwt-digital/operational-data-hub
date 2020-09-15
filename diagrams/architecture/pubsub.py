from diagrams import Cluster, Diagram

from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import AppEngine, Functions

graph_attr = {
    "bgcolor": "transparent",
    "pad": "0"
}

with Diagram("Pub/Sub", graph_attr=graph_attr, direction="TB", show=False, filename="images/pubsub"):
    with Cluster("Publishers"):
        publisher_a = AppEngine("Publisher A")
        publisher_b = AppEngine("Publisher B")
        publisher_c = Functions("Publisher C")

    with Cluster("Subscribers"):
        subscriber_x = AppEngine("Subscriber X")
        subscriber_y = Functions("Subscriber Y")
        subscriber_z = Functions("Subscriber Z")

    with Cluster("Cloud Pub/Sub"):
        with Cluster("Topic A"):
            topic_a = PubSub("Topic A")
            subscription_ay = PubSub("Subscription AY")
            subscription_az = PubSub("Subscription AZ")

        with Cluster("Topic B"):
            topic_b = PubSub("Topic B")
            subscription_bx = PubSub("Subscription BX")

        with Cluster("Topic C"):
            topic_c = PubSub("Topic C")
            subscription_cx = PubSub("Subscription CX")

        publisher_a >> topic_a
        topic_a >> subscription_ay >> subscriber_y
        topic_a >> subscription_az >> subscriber_z
        publisher_b >> topic_b >> subscription_bx >> subscriber_x
        publisher_c >> topic_c >> subscription_cx >> subscriber_x
