<img src="https://img.shields.io/badge/status-pending-orange" alt="Status" title="Status">

# Operational Data Hub

The Operational Data Hub implements an enterprise application integration architecture in which a central data hub 
facilitates all applications to connect and exchange data. This central data hub serves as the all-inclusive source of 
truth, capturing all information and business events, enabling the data-driven enterprise.

## Table of contents
1. [Introduction](#introduction)
2. [Use cases](#use-cases)
    1. [Legacy ERP system](#legacy-erp-system)
    2. [Renewal of third-party licenses](#renewal-of-third-party-licenses)
    3. [Customer support mailbox](#customer-support-mailbox)
    4. [Data science](#data-science)
    5. [Current stock](#current-stock)
    6. [Available data](#available-data)

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
centralised place. From here, the data can be analysed, more applications can be connected with each other without 
creating a spider web and all infrastructure components can be managed via one single access point: the ODH.

But creating a centralised place for all data is not the only strength of the ODH. In addition, the creation and 
maintenance of this hub are fully automated and manageable through data catalogs. These are detailed inventories of all 
data assets in an organization, designed to help data professionals quickly find the most appropriate data for any 
analytical or business purpose. But providing the location of the data is not the only reason, it also unlocks the 
automated deployment of these resources. The ODH can be fully managed by creating and editing these catalogs, where 
resources can be defined, security can be organized and data can be structured. 

> To learn more about the automated deployment via data catalogs, visit our 
<a href="https://github.com/vwt-digital/dcat-deploy" target="_blank">data catalog deployment repository</a>.


## Use cases
To describe how the ODH can be used in different ways we’ve created some use cases which will provide handles for the 
usage of the ODH. The use cases are created for a fictional software license and computer parts webshop. The fictional 
webshop has a decentralised application landscape and must innovate to get more value from their data. The use cases 
describe how the ODH can improve efficiency and data-value based on the current webshop systems.

### Legacy ERP system
The original webshop was based around BaaN IV, an ERP system popular during the early nineties. During the transition 
to a new more modern webshop, the connection with BaaN IV needed to be preserved because of the importance of the data. 
Within BaaN IV all logistic, administrative and financial business processes are processed and maintained. But because 
this is a legacy system, the data within BaaN IV is hard to reach and data science is second to none.

[TO BE CONTINUED]

### Renewal of third-party licenses
The webshop sells third-party licenses that are controlled by third-party companies. One of these companies, Adobe, has 
an API where new licenses can be requested and existing licenses can be renewed or cancelled. Currently, the requests 
for these licenses is done directly by the API used within the webshop and some form of auditing is limited. 
Furthermore, the API’s are fully intertwined with each other and potential changes are near impossible.

[TO BE CONTINUED]

### Customer support mailbox
A webshop is only as good as it’s customer support. Currently, a mailbox is used for the customer support where 
employees check and process incoming mails. These mails have to be manually connected to a certain order or inquiry, 
which costs employees a lot of time. An automated system processing and connecting these mails is desirable.

[TO BE CONTINUED]

### Data science
Because the market for webshops is packed you have to stand out. Currently, the webshop does not have any unique selling 
point other than a wide range of licenses and computer parts. The solution for this is data science; analyzing and 
mapping user activity can help by expanding the business. Right now there is not any data science opportunity as the 
data is very fragmented.

[TO BE CONTINUED]

### Current stock
The stock of computer parts is controlled by the warehouse from third-party sellers and the sales on the webshop. The 
manufacturer where most of the parts are from has a system that notifies the current stock of the warehouse. At the 
moment the webshop shows the current stock, but this is done manually by employees based on the information of the 
third-party’s selling the products. By automating this, the employees can focus on improving other areas of the business.

[TO BE CONTINUED]

### Available data
After making sure the data is reachable a new data scientist is hired to make use of the data. But before this employee 
can do his magic, a clear overview of the data is necessary. This to make it easier for the new employee but also to 
help to substantiate the use of data in line with the General Data Protection Regulation (GDPR).

[TO BE CONTINUED]
