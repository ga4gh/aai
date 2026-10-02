# Authentication and Authorization Infrastructure

## [Link to Specification]()

## Introduction

The Authentication and Authorizations Infrastructure (AAI) specification
leverages OpenID Connect (OIDC) to authenticate researchers
desiring to access clinical and genomic resources from data
holders adhering to GA4GH standards. Beyond standard OIDC authentication, AAI enables
data holders to obtain security-related attributes and authorizations of those
researchers. In parallel, the Data Use and Researcher Identity (DURI) Work Stream has developed a standard
representation for researcher authorizations and attributes known as Researcher-ID.
At its core, the AAI specification defines cryptographically secure tokens for exchanging
these researcher attributes called Visas and how various
participants can interact to authenticate researchers, and obtain and validate Visas.

This specification also provides for federated multilateral authorization infrastructure for greater
interoperability between biomedical institutions sharing restricted datasets.  

### What is OpenID Connect?

OpenID Connect is a simple identity layer, on top of the OAuth 2.0 protocol, that supports identity verification and the ability to 
obtain basic profile information about end users. The AAI specification extends this to define tokens, 
endpoints, and flows that enable an OIDC provider (called a Broker) to
provide Passports and Visas to downstream consumers called Passport Clearinghouses. Passports can then be used for
authorization purposes by downstream systems.

## Passports specification
The AAI and Passports specifications rely on each other for full functionality and will likely be merged in a future version. The Passports specification from the Data Use and Researcher Identities Work Stream can be found [here](https://ga4gh-duri.github.io/researcher_ids/ga4gh_passport_v1.html).

## Version history 

[Changelog](changes-1_2) for v1.2

Full version history available [here](aai-openid-connect-profile#specification-revision-history)


## Contributors

GA4GH is an open community and contribution is not limited to those named below.
Names listed alphabetically by surname. Repository maintainers listed [here](./MAINTAINER.md).

### Core Developers for v1.2

- Max Barkley - DNAstack
- Tom Conner - Broad Institute
- Martin Kuba - ELIXIR Czech Republic
- Andrew Patterson - The University of Melbourne Centre for Cancer Research
- Kurt Rodarmer - National Center for Biotechnology Information - NIH

### Reviewers for v1.2

- Francis Jeanson - Peter Munk Cardiac Centre and Ted Rogers Centre for Heart Research
- David Glazer - Verily Life Sciences
- Timothy Slade - RTI International
- Dylan Spalding - ELIXIR Finland

### Technical Programme Manager

- Fabio Liberante - Global Alliance for Genomics and Health

## Work Stream Leadership

### Data Security

- David Bernick - Broad Institute
- Lucila Ohno-Machado - Yale University School of Medicine 
- Previously - Jean-Pierre Hubaux - Swiss Federal Institute of Technology Lausanne

### Data Use and Researcher Identities

- Jaime Guidry-Auvil - National Cancer Institute - NIH
- Tommi Nyrönen - ELIXIR Finland


## Demonstration Implementation

[Life Science RI](https://lifescience-ri.eu/) have implemented this v1.2 specification from the finalised draft for use across the Life Science RI platforms. 
Information on creating an account is available [here](https://lifescience-ri.eu/ls-login/users/how-to-get-and-use-life-science-id.html).
With an account, the test service [here](https://echo.aai.elixir-czech.org/) will return a technical view of the various tokens created and shared in an example flow using Passport/AAI 1.2. 