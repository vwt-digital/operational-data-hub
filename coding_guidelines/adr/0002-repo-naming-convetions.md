# 2. repo naming convetions

Date: 2021-02-01

## Status

Accepted

## Context

We feel the need to use a naming convention fot github repos.

## Decision

We identify three kinds of repositories:

### 1. config VWT DAT repositories

Config repositories are repositories containing configurations of a specific Google Cloud Project (GCP) project.

* Should have the same name as the GCP project they're connected to minus the customer, environment and location
* name ends with `-config`

### 2.  solutions VWT DAT repositories
Solutions repositories are repositories containing solutions, they can belong to multiple domains.
* Their names should always start with the domain they belong
* If the repository will handle multiple facets of the service, the name should end in `-handlers`
* Sometimes, two repositories are connected because they are the frontend and backend of a service. Their names should be the same except for the ending. Frontend repositories should end in `-tool` and backend repositories should end in `-api`

### 3. "normal" VWT DAT repositories
"Normal" repositories are repositories not belonging to a solution. They contain code used specifically for the Operational Data Hub (ODH).
* Repo naming is equal to naming convetion for solution repos. Domains for these repos is limited to `dat` and `odh`.
* If the repository is forked from another repository, its name should contain the name of the repository it forked from.

## Consequences
