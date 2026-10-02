---
layout: page
title: Changes Between Versions 1.0 and 1.2
permalink: changes-1_2
---

This document lists changes between 
 * GA4GH AAI OIDC Profile [1.0.0](https://github.com/ga4gh/data-security/blob/AAIv1.0/AAI/AAIConnectProfile.md) and [1.2](https://ga4gh.github.io/data-security/aai-openid-connect-profile)
 * GA4GH Passport [1.0.0](https://github.com/ga4gh-duri/ga4gh-duri.github.io/blob/v1.0.0/researcher_ids/ga4gh_passport_v1.md) and 1.2

### Table of Contents
{:.no_toc}

* toc
{:toc}

## Terminology changes

* Removed double definitions of same concepts like “Claim Source” in AAI and “Passport Visa Assertion Source” in Passport.
* Made distinction between claim as an abstract assertion and a JWT/OIDC claim as a pair of a string key and a JSON value.
* Renamed “Data Owner” to “Data Controller” to be compatible with European GDPR 

### Changed terms

* **Claim Management System** removed, the term was not used
* claim → **Visa Assertion**
* **Claim Repository** → **Visa Assertion Repository**
* **Claim Source** → **Visa Assertion Source**
* **Claim Clearinghouse** → **Passport Clearinghouse**
* **Embedded Token** → **Visa**
* **Embedded Token Issuer** → **Visa Issuer**
* **Embedded Access Token** → **Visa Access Token**
* **Embedded Document Token** → **Visa Document Token**
* **Flow of Claims** → **Flow of Assertions**
* **Passport Bearer Token** → **Passport-Scoped Access Token**
* **Data Owner** → **Data Controller**

### New terms

* **Passport** - A signed and verifiable JWT container for holding Visas.
* **Passport Issuer** - a service that creates and signs Passports.
* **Token Endpoint** – as defined by OIDC
* **UserInfo Endpoint** - as defined by OIDC

## Introduced Token Exchange mechanism

The standardized mechanism for exchanging access tokens for other tokens defined in [RFC 8693 OAuth 2.0 Token Exchange](https://www.rfc-editor.org/info/rfc8693)
was added and used for releasing Passports. 

## Redefined Passport as a JWT containing Visas

In version 1.0, Passport was defined as ”*GA4GH-compatible access token along with the Passport Claim that is returned from Passport Broker service endpoints using such an access token*“,
thus as a tuple of an access token and a list of Visas that can be obtained from UserInfo endpoint using the access token.

In version 1.2, Passport is defined as “*a signed and verifiable JWT container for holding Visas*“, thus as a token that can be passed among systems.

For backward compatibility with version 1.0, list of Visas is still provided as a claim value from UserInfo endpoint.

## Defined Passport Issuer

A **Passport Issuer** is a service that creates and signs Passports.
A **Broker** is an OIDC Provider service that collects Visas from Visa Issuers and provides them to Passport Clearinghouses.


Broker may optionally become a Passport Issuer by supporting Token Exchange for issuance of Passports.

Brokers conforming to version 1.0 are still compatible with version 1.2, because Token Exchange support is optional.

## Added more signing algorithms

The version 1.0 allowed only **RS256** algorithm for JWT signing.
It is RSA-based algorithm using keys of size 2048 bits or larger and SHA-256 hash function.

The AAI specification version 1.2 allows also the **ES256** algorithm which is
ECDSA-based using P-256 elliptic curve and SHA-256 hash function.

Elliptic Curve Cryptography allows much shorter keys and signatures than RSA.
A short Elliptic Curve key of around 256 bits provides the same security as a 3072 bit RSA key.

For a detailed discussion of signing algorithms, see the article
[JWTs: Which Signing Algorithm Should I Use?](https://www.scottbrady91.com/jose/jwts-which-signing-algorithm-should-i-use)

## Media types for JWTs

In version 1.0, all the mentioned JWTs (access tokens, visas) used in their `typ` (media type) header parameter
the generic value `JWT` that marks a generic JWT.

In version 1.2, the `typ` header parameter is used to distinguish the various types of JWTs:

- access tokens conforming to [RFC9038](https://datatracker.ietf.org/doc/html/rfc9068#section-2.1)
  use the value `at+jwt`
- Passports use the value `vnd.ga4gh.passport+jwt`
- Visas are recommended to use the value `vnd.ga4gh.visa+jwt` but allowed to use `JWT`
  for backward compatibility with version 1.0

## Proposed Deprecations

### Visa Access Tokens (also referred to as Embedded Access Tokens)

It is proposed that the 1.x versions of this specification will be the last to support
Visa Access Tokens. New implementations should issue Visas
as Visa Document Tokens.
