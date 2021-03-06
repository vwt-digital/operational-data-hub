<img src="https://img.shields.io/badge/status-final-green" alt="Status" title="Status">

# Operational Data Hub

The Operational Data Hub implements an enterprise application integration architecture in which a central data hub 
facilitates all applications to connect and exchange data. This central data hub serves as the all-inclusive source of 
truth, capturing all information and business events, enabling the data-driven enterprise.

## Table of contents
1. [Introduction](#introduction)
    1. [Pub/Sub](#pubsub)
    2. [Automation](#automation)
2. [Use cases](#use-cases)
    1. [Legacy ERP system](#legacy-erp-system)
    2. [Renewal of third-party licenses](#renewal-of-third-party-licenses)
    3. [Customer support mailbox](#customer-support-mailbox)
    4. [Data science](#data-science)
    5. [Current stock](#current-stock)
    6. [Available data](#available-data)
3. [Patterns](#patterns)
    1. [Ingest](#ingest)
    2. [Consume](#consume)

## Introduction
This documentation is meant to explain what the Operational Data Hub (hereafter "ODH") is, what it can provide and how 
it can be used.

As described above, the ODH is a central hub for an all-inclusive source of truth by facilitating applications to 
connect and exchange data. The exchange of this data is done via a so-called message queue.


<p align="center">
  <img src="diagrams/images/message_queue.png" width="400" title="Message queue" alt="Message queue">
</p>

As seen in the diagram above, functions, applications, databases and more can post messages to different queues, where 
other resources can retrieve them. This concept empowers users to unlock more possibilities by having the data at a 
centralised place. From here, the data can be analysed, more applications can be connected without creating a 
spaghetti-like IT landscape and all infrastructure components connect via one single access point: the ODH.

### Pub/Sub
Within the ODH, [Cloud Pub/Sub](https://cloud.google.com/pubsub/docs/overview) is used as the message queue. This 
phenomenon consists of two key components: Topics and Subscriptions. Topics are named resources to which messages are 
sent by publishers, where subscriptions are named resources representing the stream of messages from a specific topic to 
be delivered to the subscribing application. To elaborate: a topic can have multiple subscriptions, but a subscription 
can only be assigned to one topic. Each topic can be subscribed to by multiple applications, as seen in the 
example below.

<p align="center">
  <img src="diagrams/images/pubsub.png" width="400" title="Pub/Sub" alt="Pub/Sub">
</p>

### Automation
But creating a centralised place for all data is not the only strength of the ODH. The creation and 
maintenance of this hub are fully automated and manageable through data catalogs. These are detailed inventories of all 
data assets in an organization, designed to help data professionals quickly find the most appropriate data for any 
analytical or business purpose. But providing the location of the data is not the only reason, it also unlocks the 
automated deployment of these resources. The ODH can be fully managed by creating and editing these catalogs, where 
resources can be defined, security can be organized and data can be structured.

> To learn more about the automated deployment via data catalogs, visit our 
>[data-catalog deployment repository](https://github.com/vwt-digital/dcat-deploy).


## Use cases
To describe how the ODH can be used in different ways we’ve created some use cases which will provide handles for the 
usage of the ODH. The use cases are created for a fictional software license and computer parts webshop. The fictional 
webshop has a decentralised application landscape and must innovate to get more value from their data.

The following use cases describe how the ODH can improve efficiency and data-value based on the current webshop systems:
1. [Legacy ERP system](#legacy-erp-system)
2. [Renewal of third-party licenses](#renewal-of-third-party-licenses)
3. [Customer support mailbox](#customer-support-mailbox)
4. [Data science](#data-science)
5. [Current stock](#current-stock)
6. [Available data](#available-data)

### 1. Legacy ERP system
The original webshop was based around NaaB IV, an enterprise resource planning (ERP) system popular during the early 
nineties. During the transition to a new and more modern webshop, the connection with NaaB IV needed to be preserved 
because of the importance of the data. Within NaaB IV all logistic, administrative and financial business processes are 
processed and maintained. But because this is a legacy system, the data within NaaB IV is hard to reach and data science 
is second to none.

#### Architecture
This is where the ODH will come in. Because of the versatility of the hub, even the oldest legacy systems can still be a 
part of the application landscape. To provide you with an overview of how the ODH will be at the centre of this 
solution, the supposed schema is defined below.

<p align="center">
  <img src="diagrams/images/legacy_erp_system.png" width="100%" title="Legacy ERP system" alt="Legacy ERP system">
</p>

As the schema shows, the solution consists of seven components divided over two functionalities, ingest and consume, and the 
external NaaB IV server.

#### Functionality
##### Ingest
Within the ingesting part of the solution, the data will be retrieved from the server and posted towards a 
[Pub/Sub topic](https://cloud.google.com/pubsub/docs/overview) (the Google Cloud Platform message queue). But before the 
data is posted towards the topic, some steps have to be taken. At first, an automated 
[Cloud Scheduler](https://cloud.google.com/scheduler) will tell the Restingest function to go to work. This is a generic 
HTTP endpoint that can retrieve documents from an external server and store them on a 
[Google Cloud Storage Bucket](https://cloud.google.com/storage/docs/key-terms#buckets) (hereafter “GCS”). For a more 
detailed description of how to use this awesome function, please visit the 
[Restingest repository](https://github.com/vwt-digital/restingest). In this case, the Restingest will request data from 
NaaB IV and store it inside a GCS Bucket.

After the upload has finished, a [Bucket trigger](https://cloud.google.com/functions/docs/calling/storage) will trigger 
the [Produce delta event function](https://github.com/vwt-digital/event-sourcing-helpers/tree/develop/functions/produce_delta_event). 
This function retrieves the data it triggered on and will check the difference (a delta) between the last known file in 
the bucket. All changes will be published towards the Pub/Sub Topic as messages.

##### Consume
After the new data entities are published towards the Pub/Sub Topic, a [consume function](https://github.com/vwt-digital/event-sourcing-consumers) 
will retrieve these messages one at a time and inserts them into a database. In this example, a 
[Firestore database](https://cloud.google.com/firestore/docs) is used, but the function can be changed to any database 
available on the platform.

#### Components
Below is the list of components used in this solution with references to documentation.

Name | Type | Documentation
--- | --- | ---
Cloud Scheduler | Cloud Scheduler | https://cloud.google.com/scheduler
Restingest | Cloud Function | https://github.com/vwt-digital/restingest
GCS Bucket | GCS Bucket | https://cloud.google.com/storage/docs/key-terms#buckets
Produce delta event | Cloud Function | https://github.com/vwt-digital/event-sourcing-helpers/tree/develop/functions/produce_delta_event
Pub/Sub Topic | Pub/Sub Topic | https://cloud.google.com/pubsub/docs/overview
Event sourcing consumer | Cloud Function | https://github.com/vwt-digital/event-sourcing-consumers
Database | Firestore | https://cloud.google.com/firestore/docs


### 2. Renewal of third-party licenses
As described before, our fictional webshop sells third-party licenses that are controlled by third-party companies. One 
of these companies, Abode, has an API where new licenses can be requested and existing licenses can be renewed or 
cancelled. Currently, the requests for these licenses is done directly by the API used within the webshop and some form 
of auditing is limited. Furthermore, the API’s are fully intertwined with each other and potential changes are near to 
impossible.

#### Architecture
To show how the ODH can be a central place to request new and update existing licenses, we’ve created two schemas 
showing the potential infrastructure setups:
1. Posting towards the external API. E.g.: requesting a new license, updating existing licenses or cancelling 
a license;
2. Receiving from the external API. E.g.: receiving updates for a license.

###### Posting
<p align="center">
  <img src="diagrams/images/renewal_licenses_posting.png" width="100%" 
  title="Posting third-party license data" alt="Posting third-party license data">
</p>

###### Receiving
<p align="center">
  <img src="diagrams/images/renewal_licenses_receiving.png" width="100%" 
  title="Receive third-party license data" alt="Receive third-party license data">
</p>

#### Functionality
As described, there are two routes possible: posting or receiving data about licenses. As seen within the diagrams, both 
flows are nearly identical, where the only difference lies within the start and endpoints. When posting data, the
webshop is the initiator and the Abode API the receiver. When receiving data, the Abode API is the initiator and the 
webshop the receiver. Below, we described this flow according to the posting of third-part license data.

##### Ingest
Within the posting of data, the webshop requests a new license or an update or cancellation on an existing license. 
Within this example, we will request a new license. The user asks this to the webshop who in turn passes this on via a 
HTTP-request towards a [Restingest endpoint](https://github.com/vwt-digital/restingest). As described within the use 
case before, the Restingest works in combination with two other components; a [GCS Bucket](https://cloud.google.com/storage/docs/key-terms#buckets) 
and a [Produce Delta Event function](https://github.com/vwt-digital/event-sourcing-helpers/tree/develop/functions/produce_delta_event)
(hereafter “PDE”). This because the Restingest only saves the requested content towards a bucket. When saved, the PDE 
Function will receive the request and post it towards the [Pub/Sub Topic](https://cloud.google.com/pubsub/docs/overview).

##### Consume
This will then be picked up by an alternative [Consume Cloud Function](https://github.com/vwt-digital/event-sourcing-consumers)
that will communicate with the Abode API. Within this communication, the function will post a request for a new license,
where the Abode API will respond with either information about the new license or a message about a denied request.

#### Components
Below is the list of components used in both solutions with references to documentation.

Name | Type | Documentation
--- | --- | ---
Restingest | Cloud Function | https://github.com/vwt-digital/restingest
GCS Bucket | GCS Bucket | https://cloud.google.com/storage/docs/key-terms#buckets
Produce delta event | Cloud Function | https://github.com/vwt-digital/event-sourcing-helpers/tree/develop/functions/produce_delta_event
Pub/Sub Topic | Pub/Sub Topic | https://cloud.google.com/pubsub/docs/overview
Consume | Cloud Function | https://github.com/vwt-digital/event-sourcing-consumers


### 3. Customer support mailbox
A webshop is only as good as it’s customer support. Currently, an Outlook mailbox is where employees communicate with 
customers. Within this mailbox, these mails have to be manually connected to a certain order or inquiry, which costs 
employees a lot of time. An automated system processing and connecting these mails would certainly improve efficiency.

#### Architecture
The ODH can not only help to connect the mailbox with the other applications, but it can also provide a higher level of 
automation.

<p align="center">
  <img src="diagrams/images/mailbox.png" width="100%" 
  title="Customer support mailbox" alt="Customer support mailbox">
</p>

As seen in the diagram, the whole mail process is fully automated by a combination of a mail-ingest and a scheduler.

#### Functionality
##### Ingest
The implementation works fully automated as it is started by a [Cloud Scheduler](https://cloud.google.com/scheduler). 
This scheduler can run multiple times within the hour, to keep unloading the mailbox. The 
[EWS Mail Ingest](https://github.com/vwt-digital/ews-mail-ingest) pulls all emails from the mailbox and uploads them 
into a [GCS Bucket](https://cloud.google.com/storage/docs/key-terms#buckets). After uploading it will publish a message 
towards the [Pub/Sub Topic](https://cloud.google.com/pubsub/docs/overview) containing all meta-data and references 
towards the uploaded files.

##### Consume
After a [consume function](https://github.com/vwt-digital/event-sourcing-consumers) receives the message, it will 
request the necessary files from the [GCS Bucket](https://cloud.google.com/storage/docs/key-terms#buckets) where the 
files were initially uploaded to. Hereafter it can process the messages individually and upload this data into a 
[Firestore](https://cloud.google.com/firestore/docs) database. This can, for instance, be the connection between the 
received messages and certain order within the Webshop database.

#### Components
Below is the list of components used in this solution with references to documentation.

Name | Type | Documentation
--- | --- | ---
Cloud Scheduler | Cloud Scheduler | https://cloud.google.com/scheduler
EWS Mail Ingest | Cloud Function | https://github.com/vwt-digital/ews-mail-ingest
GCS Bucket | GCS Bucket | https://cloud.google.com/storage/docs/key-terms#buckets
Pub/Sub Topic | Pub/Sub Topic | https://cloud.google.com/pubsub/docs/overview
Consume | Cloud Function | https://github.com/vwt-digital/event-sourcing-consumers
Database | Firestore | https://cloud.google.com/firestore/docs
API | App Engine | https://cloud.google.com/appengine/docs/the-appengine-environments


### 4. Data science
Because the market for webshops is packed you have to stand out. Currently, the webshop does not have any unique selling 
point other than a wide range of licenses and computer parts. The solution for this is data science; analyzing and 
mapping user activity can help by expanding the business. Right now there is not any data science opportunity as the 
data is very fragmented.

#### Architecture
Unlocking a data science pattern within your organisation is not something that is done via a single method. The 
infrastructure below is one example where the ODH is the centre of the data and the dataflow.

<p align="center">
  <img src="diagrams/images/data_science.png" width="400" title="Data Science" alt="Data Science">
</p>

#### Functionality
##### Consume
The starting point of the data science flow is the [Pub/Sub instance](https://cloud.google.com/pubsub/docs/overview). 
Here, as shown and described in the use cases and documentation before, all data is passed through. So this hub of 
information is the perfect starting point. Within this example, we’re using [Dataflow](https://cloud.google.com/dataflow) 
— a fully managed streaming analytics service — to extract, transform and load the data and move it through different 
analysing tools. These analytical tools can practise different research methods to find new insights from the data. In 
this example, the tools [AI Platform](https://cloud.google.com/ai-platform), [BigQuery](https://cloud.google.com/bigquery) 
and a [Firestore](https://cloud.google.com/firestore/docs) database form a process of analytical operations that form a 
recurrent process until the intended result has been achieved.

##### Ingest
When this result is accomplished, the data can be exported from the BigQuery datasets towards Pub/Sub via an Ingest 
function. After moving this data towards a database, the webshop can learn and implement the research results.

#### Components
Below is the list of components used in this solution with references to documentation.

Name | Type | Documentation
--- | --- | ---
Pub/Sub | Pub/Sub |https://cloud.google.com/pubsub/docs/overview
Dataflow | Dataflow | https://cloud.google.com/dataflow
Database | Firestore | https://cloud.google.com/firestore/docs
AI Platform | AI Platform | https://cloud.google.com/ai-platform
BigQuery | BigQuery | https://cloud.google.com/bigquery
Backfill/reprocess | Dataflow | https://cloud.google.com/dataflow
Ingest | Cloud Function | https://github.com/vwt-digital/event-sourcing-helpers


### 5. Current stock
The stock of computer parts is controlled by the warehouse from third-party sellers and the sales on the webshop. The 
manufacturer where most of the parts are from has a system that notifies the current stock of the warehouse. At the 
moment the webshop shows the current stock, but this is done manually by employees based on the information of the 
third-party’s selling the products. By automating this, the employees can focus on improving other areas of the business.

#### Architecture
Receiving data from external servers and processing them within the ODH is one of its key components. As shown in the 
diagram below, the flow consists of three key parts; the ingest, ODH and consume of the ODH. These form the base of this 
flow and make sure data is saved within the hub.

<p align="center">
  <img src="diagrams/images/current_stock.png" width="100%" title="Current Stock" alt="Current Stock">
</p>

#### Functionality
##### Ingest
The most crucial part of this architecture is the [Restingest function](https://github.com/vwt-digital/restingest). This 
function will be the entrance towards the ODH and makes sure external data will be ingested into the ODH. As described 
before, it posts the received data towards a [GCS Bucket](https://cloud.google.com/storage/docs/key-terms#buckets) where 
the [Produce Delta Event Function](https://github.com/vwt-digital/event-sourcing-helpers/tree/develop/functions/produce_delta_event) 
will post this data towards the [Pub/Sub Topic](https://cloud.google.com/pubsub/docs/overview). Within this example, 
multiple third-party API’s have information to share. And because these third-party companies all sell different 
products, we use multiple Pub/Sub Topics to communicate the products.

##### Consume
After the function has ingested the data into the hub, a [consume function](https://github.com/vwt-digital/event-sourcing-helpers) 
will save the data into the database of the webshop, that in this case is a Firestore database. This ensures that the 
visitor of the webshop always has the most up-to-date information on product stock.

#### Components
Below is the list of components used in both solutions with references to documentation.

Name | Type | Documentation
--- | --- | ---
Restingest | Cloud Function | https://github.com/vwt-digital/restingest
GCS Bucket | GCS Bucket | https://cloud.google.com/storage/docs/key-terms#buckets
Produce delta event | Cloud Function | https://github.com/vwt-digital/event-sourcing-helpers/tree/develop/functions/produce_delta_event
Pub/Sub Topic | Pub/Sub Topic | https://cloud.google.com/pubsub/docs/overview
Consume | Cloud Function | https://github.com/vwt-digital/event-sourcing-consumers
API | App Engine | https://cloud.google.com/appengine/docs/the-appengine-environments


### 6. Available data
After making sure the data is reachable a new data scientist is hired to make use of the data. But before this employee 
can do his magic, a clear overview of the data is necessary. This to make it easier for the new employee but also to 
help to substantiate the use of data in line with the General Data Protection Regulation (GDPR).

#### Architecture
To make sure a clear overview of all data within the company is easily maintained, the ODH can help by providing a 
single access point and a data structure that is extremely diverse; the data catalogs. As shown below, this architecture 
is a combination of a tremendous flow and excellent data framework.

<p align="center">
  <img src="diagrams/images/available_data.png" width="100%" title="Available Data" alt="Available Data">
</p>

#### Functionality
The core of making data insightful lies within a strong data framework and a powerful visualiser. By using data catalogs, 
it is easy to create a vastly rich landscape of data and with using [CKAN](https://ckan.org/) — a powerful data management 
system — we keep it transparent of its contents. Logically, this is the starting point of creating the data overview.

##### Ingest
As described, the ODH is a fully automated platform, and using these catalogs is nothing different. These are maintained 
within a [GitHub repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/about-repositories), 
and with each change, a [Google Cloud Build Trigger](https://cloud.google.com/cloud-build/docs/automating-builds/create-manage-triggers) 
will make sure this will be automatically implemented. After these changes have been made, a 
[Google Cloud Build](https://cloud.google.com/cloud-build/docs/overview) will post the data catalog on a 
[Pub/Sub Topic](https://cloud.google.com/pubsub/docs/overview).

##### Consume
Hereafter, the [Consume Catalog](https://github.com/vwt-digital/ckan-control/tree/develop/functions/consume-catalog) 
function will add the catalog towards a [PostgreSQL database](https://cloud.google.com/sql/docs/features#postgres) for 
the [CKAN Virtual Machine](https://github.com/vwt-digital/ckan) to communicate with the user requesting the information. 
Eventually, you have an Open Source data portal platform containing all data catalogs originating from the GitHub 
repositories, that consist of up-to-date information of the platform as described within the 
“[Automation](#automation)”-chapter.

#### Components
Below is the list of components used in both solutions with references to documentation.

Name | Type | Documentation
--- | --- | ---
GitHub repo | GitHub Repository | https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/about-repositories
Cloud Build | Cloud Build | https://cloud.google.com/cloud-build/docs/overview
Pub/Sub Topic | Pub/Sub Topic | https://cloud.google.com/pubsub/docs/overview
Consume Catalog | Cloud Function | https://github.com/vwt-digital/ckan-control/tree/develop/functions/consume-catalog
PostgreSQL | PostgreSQL | https://cloud.google.com/sql/docs/features#postgres
CKAN VM | Virtual Machine | https://github.com/vwt-digital/ckan


## Patterns
The Operational Data Hub is something truly unique and innovation when it comes to data usage. To provide a more 
in-depth explanation, we turn ourselves towards the phenomenon “Event Sourcing”. This is a great way to atomically 
update state and publish events. Where the traditional way to persist an entity is to save its current state, the Event 
Sourcing method does this by storing a sequence of state-changing events. At any time an object’s state is changed, a 
new event will be appended to the sequence. If the current state of the entity is needed, this can be reconstructed by 
replaying its events. With this great model comes accurate audit logging and easy temporal queries, because it maintains 
the complete history of each entity.

To complete the Event Sourcing method, the ODH also uses two fundamental patterns called ingest and consume. The 
ingest-pattern is used — as the name suggests — to ingest data into the ODH and the consume-pattern is used to retrieve 
data from the ODH. These two concepts cover almost every aspect of the diversity within the hub.

### Ingest
Data ingestion is the transportation of data from assorted sources to a storage medium where it can be accessed, used, 
and analyzed by an organization. 

#### State to event
One of the patterns within an ingest flow used within the ODH is to transform state data into events. To explain this 
more clearly, we take a look at the diagram below.

<p align="center">
  <img src="diagrams/images/state_diagram.png" width="100%" 
    title="Simple State Machine Diagram Notation" alt="Simple State Machine Diagram Notation">
</p>
> Source: [Simple State Machine Diagram Notation](https://medium.com/@warren2lynch/state-diagram-comprehensive-guide-with-examples-e08b6d1c70fe) (2019)

This diagram shows a simple state flow. Here, the black lines are describing events and the blue boxes are states. As 
you can see, the state itself is something that is always existing, but its value changes. This on the contrary to the 
events that only exist at a certain moment and then disappear. These events only trigger a state change as such. In the 
example above, the payment state changes from “unpaid” to “paid” as the event “paying” is completed.

When we take a look at the ingestion of data into the ODH, we can see some similarities with the diagram above. Where 
the blue state boxes are mostly seen as data storage, for instance, a Firestore Database or a Google Cloud Storage 
Bucket, the black lines can be seen as the ODH itself; the Pub/Sub instances. The changes of the state are ingested into 
the ODH as events, so the next application can process them and update their state based on these.

### Consume
To unlock the ODH’s key strength — being a central data hub that facilitates all applications to connect and exchange 
data — the data within the hub has to be communicated towards the connected applications. This is done by the “consume” 
part of the ODH platform. This part retrieves the event data from the ODH and passes it on towards different parts 
within the platform.

#### CQRS query model
One of the consume-patterns within the ODH is a Query Model defined by the [CQRS pattern](https://martinfowler.com/bliki/CQRS.html)
from Martin Fowler. Within this pattern, he describes that communicating with a database is divided into two parts; the 
Query Model and the Command Model.

<p align="center">
  <img src="diagrams/images/cqrs_models.png" width="400" title="CQRS Models" alt="CQRS Models">
</p>

The Query Model, as seen in the diagram above, is used to provide the service interfaces with data. By separating the 
single integration point it allows you to separate the load from reads and writes to scale each independently. This is a 
massive performance improvement relative to the standard “Create, read, update and delete” (CRUD) model. The Query 
Model, in this case, reads and prepares the data presentation for the end-user. When changes within this presentation 
are requested, the Command Model checks and processes these changes and updates, if necessary, the database. Hereafter 
the Query Model can, once again, prepares the data presentation for the end-user.

<p align="center">
  <img src="diagrams/images/cqrs_odh_model.png" width="400" title="ODH CQRS integration" alt="ODH CQRS integration">
</p>

Within the ODH we use the CQRS Model to create the latest state within a database specifically for the appliance needed. 
As seen in the diagram above, data from the same Pub/Sub Topic will be read towards different projects. These projects 
have their own CQRS Models to create unique views for their distinct use-cases.
