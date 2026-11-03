---
layout: page
title: GA4GH Passport
permalink: ga4gh-passport
---

# GA4GH Passport

**Version**: 1.2.1

**Work Stream Name**: Data Use and Researcher Identity (DURI)

**Product Name**: GA4GH Passport

**Product Description:** This document provides the GA4GH technical
specification for a GA4GH [Passport](#term-passport) to be
consumed by [Passport Clearinghouses](#term-passport-clearinghouse) in a
standardized approach to determine whether or not data access should be
granted. Additionally, the specification provides guidance on encoding
specific [use cases](#encoding-use-cases), including
[Visas](#term-visa) for [Registered Access](#registered-access) as
described in the "[Registered access: authorizing data
access](https://www.nature.com/articles/s41431-018-0219-y)" publication.
**Refer to the [Overview](#overview) for an introduction to how data
objects and services defined in this specification fit together.**

### Table of Contents
{:.no_toc}

* toc
  {:toc}

## Terminology

### Inherited Definitions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

This specification inherits terminology from the
[GA4GH AAI OIDC Profile](aai-openid-connect-profile#terminology)
specification, namely these terms:

* <a name="term-passport"></a>**[Passport](aai-openid-connect-profile#term-passport)**
* <a name="term-passport-scoped-access-token"></a>**[Passport-Scoped Access Token](aai-openid-connect-profile#term-passport-scoped-access-token)**
* <a name="term-passport-clearinghouse"></a>**[Passport Clearinghouse](aai-openid-connect-profile#term-passport-clearinghouse)**
* <a name="term-visa-assertion"></a>**[Visa Assertion](aai-openid-connect-profile#term-visa-assertion)**
* <a name="term-visa-assertion-source"></a>**[Visa Assertion Source](aai-openid-connect-profile#term-visa-assertion-source)**
* <a name="term-visa-issuer"></a>**[Visa Issuer](aai-openid-connect-profile#term-visa-issuer)**
* <a name="term-visa"></a>**[Visa](aai-openid-connect-profile#term-visa)**
* <a name="term-jwt"></a>**[JWT](aai-openid-connect-profile#term-jwt)**
* <a name="term-ga4gh-claim"></a>**[GA4GH Claim](aai-openid-connect-profile#term-ga4gh-claim)**
* <a name="term-broker"></a>**[Broker](aai-openid-connect-profile#term-broker)**

### Term Definitions

#### Passport Claim

-   The `ga4gh_passport_v1` claim. It is a [GA4GH Claim](#term-ga4gh-claim)
    with a claim value being a list of [Visas](#term-visa).

-   Visas from multiple [Visa Issuers](#term-visa-issuer) can be bundled together in the
    same `ga4gh_passport_v1` claim.

-   For example, the following structure encodes a Passport Claim:

    ```
    "ga4gh_passport_v1" : [
        <Visa>,
        <Visa (if more than one)>,
        ...
    ]
    ```
#### Visa Claim

-   The `ga4gh_visa_v1` claim. It is a [GA4GH Claim](#term-ga4gh-claim)
    with a claim value being a [Visa Object](#visa-object).

-   For example, the following structure encodes a Visa Claim:

    ```
    "ga4gh_visa_v1" : {
        "type": "<visa-type>",
        "asserted": <seconds-since-epoch>,
        "value": "<value-string>",
        "source": "<source-URL>",
    }
    ```

#### Visa Identity

-   The {`sub`, `iss`} pair of JWT standard claims ([RFC7519 section
    4.1.1](https://tools.ietf.org/html/rfc7519#section-4.1.1)) that are
    included within a [Visa](#term-visa) that represents a
    given user (`sub` for subject) within the issuer's (`iss`) system.

#### Visa Object

- A claim value for
    the `ga4gh_visa_v1` claim name. The claim value is a JSON object
    that provides claims that describe [Visa](#term-visa)'s
    properties that cannot be described by the standard JWT claims like `sub` or `exp`.

- The `ga4gh_visa_v1` claim is required to define a GA4GH v1 visa and
    contains controlled vocabulary as defined in this document. This object
    is not the entire visa, and there are other important claims within
    Visa JWTs that MAY be specific to its visa type as well as other
    JWT claims that are required as per this specification and the GA4GH
    AAI OIDC specification.

- For claim definitions, refer to the [Visa Object Claims](#visa-object-claims) section of this specification.

#### Visa Type

-   The "[type](#type)" claim value of a [Visa Object](#visa-object)
    that represents the semantics of the assertion and informs all parties
    involved in the authoring or handling the assertion how to interpret
    other [Visa Object Claims](#visa-object-claims).

-   For example, a Visa Type of "AffiliationAndRole" per the
    [Standard Visa Type Definitions](#ga4gh-standard-visa-type-definitions)
    specifies the semantics of the Visa as well as the
    expected encoding of the "[value](#value)" claim value for this purpose.

-   In addition to Standard Visa Type Definitions, there
    MAY also be Visas with [Custom Visa Types](#custom-visa-types).

## Overview

Please see the [Flow of Assertions](aai-openid-connect-profile#flow-of-assertions)
section in the GA4GH AAI OIDC Profile specification for an overview of interaction among the specified parties.


### General Requirements

1.  Each Visa may have a different expiry.

2.  Visas MUST have an indication of
    which organization made the [Visa Assertion](#term-visa-assertion) (i.e. the
    "[source](#source)" claim), but Visas do not generally indicate
    individual persons involved in making the assertion (i.e. who assigned/signed
    the assertion) as detailed identity information is not needed to make an
    access decision.

3.  Additional information about identity
    that is not needed to make an access decision SHOULD not be included in the
    Visas. Identity description, encoding audit details, other data
    for non-access purposes are not the intent of these Visas,
    and must be handled via other means beyond the scope of this specification
    should they be needed for entities and systems with sufficient authority to
    process such information.

4.  The [Passport Claim](#passport-claim)
    MUST only be present in a response when [Passport-Scoped Access Token](#term-passport-scoped-access-token) is provided.

5.  If the [Broker](#term-broker) is the [Visa Issuer](#term-visa-issuer),
    it MUST set the `iss` to itself and sign such Visas with an
    appropriate private key as described in the GA4GH AAI OIDC specification.

6.  Visas are designed for machine
    interpretation only in order to make an access decision and is a non-goal to
    support rich user interface requirements nor do these claims fully encode the
    audit trail.

7.  A [Visa Object](#visa-object) MAY
    contain the "[conditions](#conditions)" claim to restrict the Visa
    to only be valid when the conditions are met.

    -   For example, an identity can have several affiliations and a
        Visa with type "ControlledAccessGrants" MAY establish a
        dependency on one of them being present in the Passport by using the
        `conditions` claim.

8. Processing a Passport within a Passport Clearinghouse MUST abide by the following:

    1.  Passport Clearinghouses MUST reject all requests that include Passports
        that fail the necessary checks as described in the GA4GH AAI OIDC specification.

    2.  A Passport Clearinghouse MUST ignore all Visas it does not
        need to process a particular request.

    3.  Passport Clearinghouses MUST ignore Passports and Visas
        unless:

        1.  The Passport Clearinghouse has sufficient trust relationships
            with all of: the [Broker](#term-broker), [Visa Assertion Source](#term-visa-assertion-source),
            [Visa Issuer](#term-visa-issuer); or

        2.  The Passport Clearinghouse can rely on a trusted service that
            provides sufficient trust of any of the Broker,
            Visa Assertion Source and/or Visa Issuer
            such that the Passport Clearinghouse can establish trust of all
            three such parties.

    4.  When combining Visas with multiple [Visa Identities](#visa-identity) for the purposes of evaluating
        authorization, a Passport Clearinghouse MUST check the
        [LinkedIdentities](#linkedidentities) Visas by trusted issuers
        and ensure that trusted sources have asserted that these
        Visa Identities represent the same end user.

### Support for User Interfaces

(e.g. mapping a URI string to a human-readable description for a user
interface.)

For example, a user interface mapping of
"<https://doi.org/10.1038/s41431-018-0219-y>" to a human readable description
such as "this person is a bona fide researcher as described by the 'Registered
access: authorizing data access' publication".

It is a non-goal for this specification to consider the processes and data for
the purpose of supporting user interfaces.

## Passport Claim Format

The [Passport Claim](#passport-claim) name maps to an array of [Visas](#term-visa).

Non-normative example of a set of Visas, encoded as JWS Compact Serialization strings:

```
{
  "ga4gh_passport_v1": [
    "<eyJhbGciOiJI...aaa>",
    "<eyJhbGciOiJI...bbb>"
  ]
}
```

For a more reader-friendly example, see the [Example Passport
Claim](#example-passport-claim) section of the specification.

### Visa Requirements

-   Visas MUST conform to one of the
    [GA4GH AAI Specification Visa formats](aai-openid-connect-profile#visa-issued-by-visa-issuer)
    as JWS Compact Serialization strings as defined by [RFC7515 section
    7.1](https://tools.ietf.org/html/rfc7515#section-7.1).

-   Visa Issuers, Brokers, and Passport Clearinghouses
    MUST conform to the
    [GA4GH AAI Specification](aai-openid-connect-profile)
    requirements for Visas in their use of Visas.

-   Validation, as outlined elsewhere in this specification and the
    GA4GH AAI Specification, MUST be performed before Visas are
    used for identity or authorization.

## Visa Format

Visas are signed JWTs encoded into strings using JWS Compact Serialization.
When decoded, their structure is:

```
{
  ["typ": "vnd.ga4gh.visa+jwt | at+jwt | JWT",]
  "alg": "<signing-algorithm>",
  ["jku": "<json-web-keys-set-URL>",]
  "kid": "<signing-key-identifier>"
}.
{
  "iss": "<issuer-URL>",
  "sub": "<subject-identifier>",
  ["scope": "openid ...",]
  "jti": "<token-identifier>",
  "iat": <seconds-since-epoch>,
  "exp": <seconds-since-epoch>,
  "ga4gh_visa_v1": {
    "type": "<visa-type>",
    "asserted": <seconds-since-epoch>,
    "value": "<value-string>",
    "source": "<source-URL>",
    ["conditions": [...],]
    ["by": "<by-identifier>"]
  }
}.<signature>
```
The standard JWT payload claims `iss`, `sub`, `iat`, `exp` are all REQUIRED.

One of `scope` or `jku` MUST be present as described in
[Conformance for Visa Issuers](aai-openid-connect-profile#conformance-for-visa-issuers)
within the AAI specification.

Claims within the `ga4gh_visa_v1` [Visa Object](#visa-object) are as described
in the [Visa Object Claims](#visa-object-claims) section of this specification.

#### "**typ**"

- OPTIONAL. The value of the `typ` header claim is RECOMMENDED to be `vnd.ga4gh.visa+jwt`
  for [Visa Document Token Format](aai-openid-connect-profile#visa-document-token-format)
  visas. The value `JWT` marking  general JWTs MAY also be used.
- For [Visa Access Token Format](aai-openid-connect-profile#visa-access-token-format)
  visas the value is unspecified, but it would likely be `at+jwt` as required by [section 2.1 of RFC 9068](https://datatracker.ietf.org/doc/html/rfc9068#section-2.1)
  for JWT access tokens.
- The `typ` header claim is specified by [section 5.1 of JWT RFC](https://datatracker.ietf.org/doc/html/rfc7519#section-5.1)
  to contain media type of the JWT for disambiguation.
  The full recommended media type for GA4GH Visas is `application/vnd.ga4gh.visa+jwt` where the subtype consist of
  the "vendor tree" prefix `vnd`, the "producer name" `ga4gh`, and the "product designation" `visa`
  followed by the `+jwt` structured syntax suffix (specified in [section 3.2](https://datatracker.ietf.org/doc/html/rfc6838#section-3.2)
  and [section 4.2.8  of RFC 6838](https://datatracker.ietf.org/doc/html/rfc6838#section-4.2.8)).
  Then [section 4.1.9 of JWS RFC](https://www.rfc-editor.org/rfc/rfc7515.html#section-4.1.9) recommends to omit the prefix
  `application/` to keep messages compact.

#### "**alg**"

- REQUIRED.The section [Signing Algorithms](aai-openid-connect-profile#signing-algorithms)
in the AAI specification lists possible algorithms used in the `alg` header claim.


#### "**exp**"

-   REQUIRED. Generally, it is seconds since unix epoch of when the
    [Visa Assertion Source](#term-visa-assertion-source)
    requires such an assertion to be no longer valid. A Visa
    Assertion Source MAY choose to make an assertion very long lived.
    However, a [Visa Issuer](#term-visa-issuer) MAY
    choose an earlier timestamp in order to limit the assertion’s duration
    within downstream Passport Clearinghouses.

-   Access is NOT necessarily removed by the `exp` timestamp. Instead,
    this timestamp may be viewed as a cut-off after which no new access
    will be granted and action to remove any existing access may
    commence anytime shortly after this cut-off period.

-   Its use by a Passport Clearinghouse is described in the
    [Visa Expiry](#visa-expiry) section and
    [Token Revocation](#token-revocation) section.

## Visa Object Claims

Although standard claims within a [Visa Object](#visa-object)
are defined in this section, other claims MAY exist within the object
and should be ignored by any Passport Clearinghouse that is not familiar
with the use of such claims. Claim names are reserved for definition by
GA4GH (or a body it elects).

#### "**type**"

-   REQUIRED. A [Visa Type](#visa-type) string that is
    either a [Standard Visa Type](#ga4gh-standard-visa-type-definitions) name, or a
    [Custom Visa Type](#custom-visa-types) name.

#### "**asserted**"

- REQUIRED. Seconds since unix epoch that represents when the
    [Visa Assertion Source](#term-visa-assertion-source) made the claim.

- Note that the standard `iat` JWT claim on the Visa reflects the timestamp
    of when the Visa was minted whereas the `asserted` claim
    reflects when the [Visa Assertion Source](#term-visa-assertion-source) made the assertion.

- `asserted` MAY be used by a Passport Clearinghouse as described in the
    [Visa Expiry](#visa-expiry) section.

- If a Visa Assertion repository does not include enough
    information to construct an `asserted` timestamp, a [Visa Issuer](#term-visa-issuer) MAY use a recent timestamp (for
    example, the current timestamp) if the Visa Assertion repository
    is kept up to date such that the Visa Issuer can ensure that
    the assertion is valid at or near the time of minting the Visa.
    However, generally it is RECOMMENDED to have the
    Visa Assertion repository provide more accurate `asserted` information.

#### "**value**"

- REQUIRED. A string that represents any of the scope, process, identifier and
    version of the assertion. The format of the string can vary by the
    [Visa Type](#visa-type).

- For example, `value: "https://doi.org/10.1038/s41431-018-0219-y"` when `type: "ResearcherStatus"`
    represents a version of Registered Access Bona Fide
    researcher status. Note that Registered Access requires more than one
    [Visa](#passport-visa) as outlined in the [Registered
    Access](#registered-access) section.

- For the purposes of enforcing its policies for access, a Passport
    Clearinghouse evaluating the `value` claim MUST:

    -   Validate URL strings as per the [URL Claim](#url-claims)
        requirements if the Visa Type definition indicates the value
        is a URL (as indicated by the `type` claim).

    -   Value strings MUST be full string case-sensitive matches
        unless the Visa Type defines a safe and reliable format for
        partitioning the value into substrings and matching on the various
        substrings. For example, the standard
        [AffiliationAndRole](#affiliationandrole) Visa Type can be
        reliably partitioned by splitting the string at the first “@” sign if such
        exists, or otherwise producing an error (i.e. denying permission).

#### "**source**"

-   REQUIRED. A [URL Claim](#url-claims) that provides at a minimum the
    organization that made the assertion. If there is no organization
    making the assertion, the `source` claim value MUST be set to
    "https\://no.organization".

-   For complex organizations that may require more specific information
    regarding which part of the organization made the assertion, this claim MAY
    also encode some substructure to the organization that represents the
    origin of the authority of the assertion. When this approach is chosen, then:

    -   The additional substructure MUST only encode the sub-organization or
        department but no other details or variables that would make it
        difficult to enumerate the full set of possible values or cause Passport
        Clearinghouses confusion about which URLs to whitelist.

    -   The additional information SHOULD be encoded into the subdomain or path
        whenever possible and SHOULD generally avoid the use of query parameters
        or anchors to represent the sub-organization.

    -   Some organizations MAY wish to attribute the `source` to a particular
        Data Access Committee (DAC), especially for
        [ControlledAccessGrants](#controlledaccessgrants) Visa Types.
        For example:

        `source: "https://www.ebi.ac.uk/ega/dacs/EGAC00000000001"`

        could represent one particular logical "DAC" organization as referred
        to by the EBI organization, and could be maintained by the EBI as a
        permanent identifier for this DAC.

#### "**conditions**"

-   OPTIONAL. A set of conditions on a
    [Visa Object](#visa-object) indicates that the Visa is
    only valid if the clauses of the conditions match other Visas
    elsewhere in the [Passport](#term-passport) and such content is both valid
    (e.g. hasn’t expired; signature of Visa has been verified against
    the public key; etc.) and if such content is accepted by the Passport
    Clearinghouse (e.g. the issuer is trusted; the `source` claim meets any
    policy criteria that has been established, etc.).

-   A Passport Clearinghouse MUST always check for the presence of
    the `conditions` claim and if present it MUST only accept the
    Visa if it can confirm that the conditions have been met.

-   Although it is RECOMMENDED to always implement full condition checking
    capabilities as described in this section, if a Passport Clearinghouse will be
    deployed for a more limited purpose where it is not expected to ever receive
    Visas with conditions, then such a Passport Clearinghouse MAY choose to
    not implement full condition checking. However, even in this case it MUST
    still check for the presence of the `conditions` claim on Visa
    Objects and reject (ignore) any Visas that contain a non-empty
    `conditions` claim value. Likewise if not all condition matching algorithms
    are implemented, it MUST reject any Visas that contain patterns
    that are not supported.

-   Format:

    ```
    "conditions": [
      [
        { // Condition clause 1
          "type": "<visa-type>",
          "<visa-object-claim-name-1>": "<match-type>:<match-value>",
          "<visa-object-claim-name-2>": "<match-type>:<match-value>",
          ...
        }, // AND
        { // Condition clause 2
          ...
        }
      ], // OR
      [
        { // Condition clause 3
          "type": "<visa-type>",
          "<visa-object-claim-name>": "<match-type>:<match-value>",
          ...
        }
      ],
      ...
    ]
    ```

-   The `conditions` value is a two-nested-lists structure in Disjunctive
    Normal Form:

    -   The outer level list is a set of OR clauses

    -   The inner level list is a set of AND clauses that contain "Condition
        Clauses"

    -   A Condition Clause MUST specify a "type" claim with a value as a
        Visa Type plus it MUST include at least one other claim with a
        name that matches a valid Visa Object claim name.

    -   The values of Condition Clause claims MUST have a string prefix followed
        by a colon and then string suffix, except for `type` where it MUST be
        assumed to be "const" and is not specified.

        -   If prefix is "const", then suffix MUST use case sensitive full string
            matching.

        -   If prefix is "pattern", then suffix MUST use full string [Pattern
            Matching](#pattern-matching) to match input.

        -   If prefix is "split_pattern", then the full suffix MUST use full
            string [Pattern Matching](#pattern-matching) on each full
            substring from splitting the corresponding Visa Object
            claim value that is being compared by the ";" character. If any one
            full substring matches, then the Condition Clause claim has found a
            match. "split_pattern" SHOULD only be used on claims where the
            Visa Type has been specified in a format that makes splitting
            on this character to be reliable, such as URI-encoded substrings with
            semicolon separators (see [LinkedIdentities](#linkedidentities) as an
            example).

            -   For example: a Condition Clause claim value of
                "split_pattern:123,https:%2F%2Fexample?.org" will match a
                Visa Object claim value of
                "001,https::%2F%2Fexample1.org;123,https::%2F%2Fexample2.org;456,https::%2F%2Fexample3.org"
                because this comparison value will be split into:
                ```
                [
                  "001,https::%2F%2Fexample1.org",
                  "123,https::%2F%2Fexample2.org",
                  "456,https::%2F%2Fexample3.org"
                ]
                ```
                and the second entry in that list is a match using the Pattern
                Matching definition with `123,https:%2F%2Fexample?.org` as the
                pattern to use.

        -   If prefix is unknown or unsupported, then the Condition Clause must
            fail to match.

-   Condition Clause claims are restricted to only [Visa Object Claims](#visa-object-claims)
    (e.g. `value`, `source`, etc.) with string value
    definitions.

    -   It MUST NOT include `conditions` (i.e. a condition cannot be placed on
        another condition)

    -   It MUST NOT contain a timestamp claim such as `asserted`.

-   The Passport Clearinghouse MUST verify that for each Condition Clause
    present, there exists a valid single corresponding
    [Visa Object](#visa-object) such that:

    -   Checking the correctness of the Condition Clause MUST be performed first.
        For example, a `type` claim MUST be present.

    -   Ignore Visa Objects that have the `conditions` claim present.
        This will avoid deep nesting of condition evaluation (i.e. avoid condition
        loops, stack overflows, etc).

    -   A Condition Clause claim matches when the `<match-type>` algorithm
        matches a corresponding Visa Object’s claim in the Passport.

    -   [Visa Object Claims](#visa-object-claims) that are not specified
        in the Condition Clause are not required to match (i.e. any value will be
        accepted within that claim, including if the claim is not present in the
        Visa Object).

    -   All Condition Clause claims that are specified within one Condition
        Clause MUST match the same Visa Object in the Passport.

-   Non-normative example:

    ```
    "conditions": [
      [
        {
          "type": "AffiliationAndRole",
          "value": "const:faculty@uni-heidelberg.de",
          "by": "const:so"
        }, // AND
        {
          "type": "ResearcherStatus",
          "value": "const:https://doi.org/10.1038/s41431-018-0219-y",
        }
      ], // OR
      [
        {
          "type": "AffiliationAndRole",
          "value": "pattern:faculty@*",
          "source": "const:https://visas.elixir.org"
          "by": "const:system"
        }
      ]
    ]
    ```

    Would match a corresponding AffiliationAndRole assertion within the same
    Visa Object that has **any** of the following:

    -   On "Visa match 1":

        -   `type` = "AffilationAndRole"; AND

        -   `value` = "faculty\@uni-heidelberg.de"; AND

        -   `by` = "so"

        AND on any other Visa as well as checking "Visa match 1":

        -   `type` = "ResearcherStatus"; AND

        -   `value` = "<https://doi.org/10.1038/s41431-018-0219-y>"

    -   OR, alternative acceptance is matching just one Visa:

        -   `type` = "AffilationAndRole"; AND

        -   `value` starts with "faculty\@"; AND

        -   `source` = "https://visas.elixir.org"; AND

        -   `by` = "system"

##### Pattern Matching

-   Pattern Matching is only for use as specified by
    "[conditions](#conditions)".

-   MUST Use full string case-sensitive character pattern comparison.

-   MUST support special meaning characters as the specification of patterns:

    -   `?` : A `<question-mark>` is a pattern that SHALL match any single
        character.

    -   `*` : An `<asterisk>` is a pattern that SHALL match multiple characters:

        -   Match any string, including the empty string and null string.

        -   Match the greatest possible number of characters that still allows
            the remainder of the pattern to match the string.

-   There is no escape character for special characters such as patterns.
    `?` is always treated as the `<question-mark>` pattern and `*` is always
    treated as the `<asterisk>` pattern.

-   A method evaluating a pattern on a string of input SHALL return a true if
    the input has found one or more possible ways to match or false if it does
    not.

#### "**by**"

-   OPTIONAL. The level or type of authority within the "source" organization
    of the assertion.

-   A Passport Clearinghouse MAY use this claim as part of an authorization
    decision based on the policies that it enforces.

-   Fixed vocabulary values for this claim are:

    -   **self**: The Visa Identity for which the assertion is being made
        and the person who made the assertion is the same person.

    -   **peer**: A person at the `source` organization has made this assertion on
        behalf of the Visa Identity's person, and the person who is making
        the assertion has the same Visa Type and `value` in that `source`
        organization. The `source` claim represents the peer’s
        organization that is making the assertion, which is not necessarily
        the same organization as the Visa Identity's organization.

    -   **system**: The `source` organization’s information system has made the
        assertion based on system data or metadata that it stores.

    -   **so**: The person (also known as "signing official") making the assertion
        within the `source` organization possesses direct authority (as part of
        their formal duties) to bind the organization to their assertion that the
        Visa Identity did possess such authority at the time the
        assertion was made.

    -   **dac**: A Data Access Committee or other authority that is responsible
        as a grantee decision-maker for the given `value` and `source` claims
        pair.

-   If this claim is not provided, then none of the above values can be assumed
    as the level or type of authority and the authority MUST be assumed to be
    "unknown". Any policy expecting a specific value as per the list above MUST
    fail to accept an "unknown" value.

### URL Claims

A [Visa Object Claim](#visa-object-claims) that is defined as being of URL
format (see [RFC3986 section
1.1.3](https://tools.ietf.org/html/rfc3986?#section-1.1.3)) with the following
limitations:

1.  For the purposes of evaluating access, the URL MUST be treated as a simple
    unique persistent string identifier.

2.  The URL is a canonical identifier and as such it is important that Passport
    Clearinghouses MUST match this identifier consistently using a
    case-sensitive full string comparison.

    -   If TLS is available on the resource, then its persistent identifier URL
        SHOULD use the "https" scheme even if the resource will also resolve using
        the "http" scheme.

    -   When the URL is being used to represent an organization or a well defined
        child organization within a "[source](#source)" claim, it is RECOMMENDED
        to use a URL as a persistent organizational ontology identifier, whether
        managed directly or by a third-party service such as
        [GRID](https://grid.ac/institutes) when reasonable to do so.

3.  The URL SHOULD also be as short as reasonably possible while avoiding
    collisions, and MUST NOT exceed 255 characters.

4.  The URL MUST NOT be fetched as part of policy evaluation when making an
    access decision. For policy evaluation, it is considered an opaque string.

5.  URLs SHOULD resolve to a human readable document for a policy maker to
    reason about.

## GA4GH Standard Visa Type Definitions

Note: in addition to these GA4GH standard Visa Types, there is also
the ability to for a Visa Issuer to encode [Custom Visa Types](#custom-visa-types).

### AffiliationAndRole

-   The [Visa Identity](#visa-identity)’s role within the identity’s affiliated institution
    as specified by one of the following:

    -   [eduPersonScopedAffiliation](http://software.internet2.edu/eduperson/internet2-mace-dir-eduperson-201602.html#eduPersonScopedAffiliation)
        attributed value of: faculty, student, or member. \
        This term is defined by eduPerson by the affiliated organization
        (organization after the \@-sign).

        -   Example: "faculty\@cam.ac.uk"

        -   Note: based on the eduPerson specification, it is possible that
            institutions use a different definition for the meaning of "faculty"
            ranging from "someone who does research", to "someone who teaches",
            to "someone in education that works with students".

    -   A custom role that includes a `namespace` prefix followed by a dot (".")
        where implementers introducing a new custom role MUST coordinate
        with GA4GH (or a body it elects) to align custom role use cases in order
        to maximize interoperability and avoid fragmentation across
        implementations.

        -   Non-normative example: "ega.researcher\@med.stanford.edu" where "ega"
            is the namespace and "researcher" is the custom role within that
            namespace.

        -   Custom roles and their prefixes MUST be limited to characters: a-z,
            dash ("-"), underscore ("_"), digits (0-9). Custom roles and prefixes
            MUST start with characters a-z.

-   If there is no affiliated institution associated with a given assertion, the
    affiliation portion of AffliationAndRole MUST be set to "no.organization".

    -   Example: "public.citizen-scientist\@no.organization"

-   AffiliationAndRole can be safely partitioned into a {role, affiliation} pair
    by splitting the value string at the first "@" sign.

### AcceptedTermsAndPolicies

- The [Visa Identity](#visa-identity) or the
    "[source](#source)" organization has acknowledged the specific terms,
    policies, and conditions (or meet particular criteria) as indicated by the
    `value` claim.

- The `value` claim value conforms to [URL Claim](#url-claims) format.

- The URL SHOULD resolve to a public-facing, human readable web page that
    describe the terms and policies.

- Example `value: "https://doi.org/10.1038/s41431-018-0219-y"`
    acknowledges ethics compliance for a particular version of [Registered
    Access](#registered-access). Note that more
    [Visas](#term-visa) are needed to meet the requirements for Registered
    Access status.

- MUST include the "[by](#by)" claim.

### ResearcherStatus

-   The person has been acknowledged to be a researcher of a particular type or
    standard.

-   The `value` claim conforms to [URL Claim](#url-claims) format, and it
    indicates the minimum standard and/or type of researcher that describes
    the person represented by the given [Visa Identity](#visa-identity).

-   The URL SHOULD resolve to a human readable web page that describes the
    process that has been followed and the qualifications this person has met.

-   Example `value: "https://doi.org/10.1038/s41431-018-0219-y"`
    acknowledges a particular version of the registration process as needed
    for [Registered Access](#registered-access) Bona Fide researcher
    status. Note that more [Visas](#term-visa) are needed to meet
    the requirements for Registered Access status.

### ControlledAccessGrants

-   A dataset or other object for which controlled access has been granted to
    this [Visa Identity](#visa-identity).

-   The `value` claim conforms to [URL Claim](#url-claims) format.

-   The `source` claim contains the access grantee organization.

-   MUST include the "[by](#by)" claim.

### LinkedIdentities

-   The identity as indicated by the {"sub", "iss"} pair (aka
    [Visa Identity](#visa-identity)) of the
    [Visa](#term-visa) is the same as the identity or identities listed
    in the "[value](#value)" claim.

-   The "[value](#value)" claim format is a semicolon-delimited list of
    "&lt;uri-encoded-sub>,&lt;uri-encoded-iss>" entries with no added whitespace
    between entries.

    -   The "sub" and "iss" that are used to encode the "value" claim do
        not need to conform to [URL Claim](#url-claims)
        requirements since they must match the corresponding Visa
        "sub" and "iss" claims that may be issued.

    -   By URI encoding ([RFC 3986](https://tools.ietf.org/html/rfc3986)) the
        "iss", special characters (such as "," and ";") are encoded within the URL
        without causing parsing conflicts.

    -   Example:
        "123456,https%3A%2F%2Fexample.org%2Fa%7Cb%2Cc;7890,https%3A%2F%2Fexample2.org".

-   The "[source](#source)" claim refers to the [Visa Assertion
    Source](#term-visa-assertion-source) that is making the assertion. This is
    typically the same organization as the [Visa
    Issuer](#term-visa-issuer) (`iss`) that signs the Visa, but the
    `source` MAY also refer to another Visa Assertion Source depending
    on which organization collected the information.

-   As a non-normative example, if a policy needs 3 Visas and
    there are three Visas that meet the criteria on one Passport
    but they use 3 different `sub` values ("1234", "567", "890123"), then
    **any** of the following, if from a trusted issuers and sources, may
    allow these Visas to be combined (shown with JSON payload only
    and without the REQUIRED URI-encoding in order to improve readability of
    the example).

    1. One Visa that links 3 Visa Identities together.

       ```
       {
         "iss": "https://example1.org/oidc",
         "sub": "1234",
         "ga4gh_visa_v1": {
           "type": "LinkedIdentities",
           "value": "567,https://example2.org/oidc;890123,https://example3.org/oidc",
           "source": "https://example1.org/oidc"
           ...
         }
       }
       ```

       or

    2. One Visa that links a superset of Visa
       Identities together.

       ```
       {
         "iss": "https://example0.org/oidc",
         "sub": "00001",
         "ga4gh_visa_v1": {
           "type": "LinkedIdentities",
           "value":
             "1234,http://example1.org/oidc;567,http://example2.org/oidc;890123,http://example3.org/oidc;sub4,http://example4.org/oidc"
           "source": "https://example0.org/oidc"
           ...
         }
       }
       ```

       or

    3. Multiple Visas that chain together a set or superset
       of Visa Identities.

       ```
       {
         "iss": "https://example1.org/oidc",
         "sub": "1234",
         "ga4gh_visa_v1": {
           "type": "LinkedIdentities",
           "value": "567,https://example2.org/oidc",
           "source": "https://example1.org/oidc"
           ...
         }
       },
       {
         "iss": "https://example2.org/oidc",
         "sub": "567",
         "ga4gh_visa_v1": {
           "type": "LinkedIdentities",
           "value": "890123,https://example3.org/oidc",
           "source": "https://example2.org/oidc"
           ...
         }
       }
       ```

## Custom Visa Types

-   In addition to the
    [GA4GH Standard Visa Type Definitions](#ga4gh-standard-visa-type-definitions),
    Visas MAY be added using custom `type` names so long as the
    encoding of these Visas will abide by the requirements described
    elsewhere in this specification.

-   Custom Visa Types MUST limit personally identifiable information
    to only that which is necessary to provide authorization.

-   The custom `type` name MUST follow the format prescribed in the
    [URL Claims](#url-claims) section of the specification.

-   Implementers introducing a new custom `type` name MUST coordinate with the
    GA4GH (or a body it elects) to align custom `type` use cases to maximize
    interoperability and avoid unnecessary fragmentation across implementations.

    -   To review the custom visa registry, including any visa descriptions,
        examples and links that have been provided through proposals using this
        process, visit the [Custom Visa Type Registry](ga4gh_custom_visas.md)
        page.

    -   Documentation on encoding and interpreting the claims SHOULD
        be provided as part of the proposal and for inclusion in a public custom
        visa type registry maintained by GA4GH. This documentation SHOULD also include
        examples and links to relevant documentation and/or open source software
        that MAY be available.

-   Passport Clearinghouses MUST ignore all Visas containing a custom
    `type` name that they do not support.

-   Non-normative example custom `type` name:\
    `type: "https://example.org/passportVisaTypes/researcherStudies"`.

## Encoding Use Cases

Use cases include, but are not limited to the following:

### Registered Access

-   To meet the requirements of Registered Access to data as defined by
    publication <https://doi.org/10.1038/s41431-018-0219-y> as a specific
    version of Registered Access, a user needs to have **all** of the following
    Visas:

    1.  Meeting the ethics requirements is represented by:

        -   `type: "AcceptedTermsAndPolicies"`; and

        -   `value: "https://doi.org/10.1038/s41431-018-0219-y"`

    2.  Meeting the bona fide status is represented by:

        -   `type: "ResearcherStatus"`; and

        -   `value: "https://doi.org/10.1038/s41431-018-0219-y"`

-   If other versions of Registered Access are introduced, then the `value`
    claims for AcceptedTermsAndPolicies as well as ResearcherStatus MAY
    refer to the document or publication or sections thereof to act as the
    permanent identifiers for such versions of Registered Access.

-   The [Passport Clearinghouse](#term-passport-clearinghouse) (e.g. to
    authorize a registered access beacon) needs to evaluate the
    multiple Visas listed above to ensure their values match
    before granting access.

    -   If combining Visas from multiple
        [Visa Identities](#visa-identity), the Passport
        Clearinghouse MUST also check the
        [LinkedIdentities](#linkedidentities) Visas and
        determine if combining these identities came from a trusted
        [Visa Issuer](#term-visa-issuer).

### Controlled Access

-   Controlled Access to data utilizes the following [Visa Types](#visa-type):

    -   MUST utilize one or more
        [ControlledAccessGrants](#controlledaccessgrants) and/or custom
        controlled access visa type(s) for permissions associated with specific
        data or datasets. There MAY be more standard visa types introduced for
        encoding controlled access in future revisions of the Passport
        specification.

    -   MAY utilize the [conditions](#conditions) claim on
        "ControlledAccessGrants" to cause such a grant to require
        a Visa from a trusted Visa Assertion Source to
        assert that the identity has a role within a specific organization.
        This can be achieved by using the
        [AffiliationAndRole](#affiliationandrole) Visa Type on
        the `conditions`.

    -   MAY utilize any other valid Visa Type or `conditions` claim
        that may be required to meet controlled access policies.

## Visa Expiry

In addition to any other policy restrictions that a Passport Clearinghouse
may enforce, Passport Clearinghouses that provide access for a given
duration provided by the user (excluding any revocation policies) MUST
enforce one of the following algorithm options to ensure that Visa
expiry is accounted for:

**Option A**: use the following algorithm to determine if the Visa
is valid for the entire duration of the requested duration:

```
now()+requestedTTL < min(token.exp, token.ga4gh_visa_v1.asserted+maxAuthzTTL)
```

Where:

-   `requestedTTL` represents the duration for which access is being requested.
    Alternatively a solution may choose to have a stronger revocation policy
    instead of requiring such a duration.

-   `maxAuthzTTL` represents any additional expiry policy that the Passport
    Clearinghouse may choose to enforce. If this is not needed, it can
    effectively ignored by using a large number of years or otherwise have
    `token.ga4gh_visa_v1.asserted+maxAuthzTTL` removed and simplify the right
    hand side expression accordingly.

**Option B**: if tokens are sufficiently short lived and/or the authorization
system has an advanced revocation scheme that does not need to specify a
maxAuthzTTL as per Option A, then the check can be simplified:

```
now()+accessTokenTTL < token.exp
```

Where:

-   `accessTokenTTL` represents the duration for which an access token will be
    accepted and is bounded by the next refresh token cycle or [Access Token
    Polling](aai-openid-connect-profile#at-polling)
    cycle or any larger propagation delay before access is revoked, which
    needs to be assessed based on the revocation model.

    -   For example, `accessTokenTTL` may be set to one hour, after which time
        more access tokens may be minted using a corresponding refresh token if
        it has not yet been revoked.

**Expiry when using multiple Visas**: if multiple Visas are
required as part of an access policy evaluation, then the expiry to be used MUST
be the minimum expiry timestamp, as calculated by the appropriate option above,
across all Visas (`token` set) that were accepted as part of evaluating
the access policy.

## Token Revocation

As per the [GA4GH AAI Specification on Token
Revocation](aai-openid-connect-profile#token-revocation),
the following mechanisms are available within Visa:

1.  Visa Objects have an "[asserted](#asserted)" claim to allow
    downstream policies to limit the life, if needed, of how long assertions
    will be accepted for use with access and refresh tokens.

2.  Visas have an "[exp](#exp)" claim to allow Brokers and
    Passport Clearinghouses to limit the duration of access.

At a minimum, these Visa Claims MUST be checked by all Passport
Clearinghouses and systems MUST be in place to begin to take action to remove access
by the expiry timestamp or shortly thereafter. Propagation of these permission
changes may also require some reasonable delay.

Systems employing Visas MUST provide mechanisms to
limit the life of access, and specifically MUST conform to the GA4GH AAI
Specification requirements in this regard. Systems utilizing Visas MAY also
employ other mechanisms outlined in the GA4GH AAI Specification, such as [Access
Token Polling](aai-openid-connect-profile#at-polling)
if the Visa is encoded as a [Visa Access Token](aai-openid-connect-profile#term-visa-access-token-format).

## Example Passport Claim

This non-normative example illustrates a [Passport Claim](#passport-claim)
that has Visas representing Registered Access bona fide researcher
status along with other Visas for access to specific Controlled Access
data. The [Visa Types](#visa-type) for this example are:

-   **AffiliationAndRole**: The person is a member of faculty at Stanford
    University as asserted by a Signing Official at Stanford.

-   **ControlledAccessGrants**: The person has approved access by the DAC at the
    Example Institute for datasets 710 and approval for dataset 432 for a dataset
    from EGA.

    -   In this example, assume dataset 710 does not have any
        "[conditions](#conditions)" based on the
        AffiliationAndRole because the system that is asserting the assertion has an
        out of band process to check the researcher’s affiliation and role and
        withdraw the dataset 710 claim automatically, hence it does not need the
        `conditions` claim to accomplish this.

    -   In this example, assume that dataset 432 does not use an out of band
        mechanism to check affiliation and role, so it makes use of the
        "[conditions](#conditions)" claim mechanism to
        enforce the affiliation and role. The dataset 432 assertion is only valid if
        accompanied with a valid AffiliationAndRole claim for
        "faculty\@med.stanford.edu".

-   **AcceptedTermsAndPolicies**: The person has accepted the Ethics terms and
    conditions as defined by Registered Access. They took this action
    themselves.

-   **ResearcherStatus**: A Signing Official at Stanford Medicine has asserted
    that this person is a bona fide researcher as defined by the [Registered
    Access](#registered-access) model.

-   **LinkedIdentities**: A Broker at example3.org has provided
    software functionality to allow a user to link their own accounts together.
    After the user has successfully logged into the two accounts and passed all
    auth challenges, the Broker added the
    [LinkedIdentities](#linkedidentities) Visa for those two accounts:
    (1) "10001" from example1.org, and (2) "abcd" from example2.org.
    Since the Broker is signing the "LinkedIdentities"
    [Visa](#term-visa), it is acting as the [Visa Issuer](#term-visa-issuer).

Normally a Passport like this would include [Visa
Format](#visa-format) entries as JWS Compact Serialization strings,
however this example shows the result after the Visas have been
unencoded into JSON (and reduced to include only the payload) to be more
reader-friendly.

```
"ga4gh_passport_v1": [
    {
        "iat": 1580000000,
        "exp": 1581208000,
        ...
        "ga4gh_visa_v1": {
            "type": "AffiliationAndRole",
            "asserted": 1549680000,
            "value": "faculty@med.stanford.edu",
            "source": "https://grid.ac/institutes/grid.240952.8",
            "by": "so"
        }
    },
    {
        "iat": 1580000100,
        "exp": 1581168872,
        ...
        "ga4gh_visa_v1": {
            "type": "ControlledAccessGrants",
            "asserted": 1549632872,
            "value": "https://example-institute.org/datasets/710",
            "source": "https://grid.ac/institutes/grid.0000.0a",
            "by": "dac"
        }
    },
    {
        "iat": 1580000200,
        "exp": 1581168000,
        ...
        "ga4gh_visa_v1": {
            "type": "ControlledAccessGrants",
            "asserted": 1549640000,
            "value": "https://ega-archive.org/datasets/EGAD00000000432",
            "source": "https://ega-archive.org/dacs/EGAC00001000205",
            "by": "dac"
            "conditions": [
                [
                    {
                        "type": "AffiliationAndRole",
                        "value": "const:faculty@med.stanford.edu",
                        "source": "const:https://grid.ac/institutes/grid.240952.8",
                        "by": "const:so"
                    }
                ],
                [
                    {
                        "type": "AffiliationAndRole",
                        "value": "const:faculty@med.stanford.edu",
                        "source": "const:https://grid.ac/institutes/grid.240952.8",
                        "by": "const:system"
                    }
                ]
            ],
        }
    },
    {
        "iss": "https://issuer.example1.org/oidc",
        "sub": "10001",
        "iat": 1580000300,
        "exp": 1581208000,
        ...
        "ga4gh_visa_v1": {
            "type": "AcceptedTermsAndPolicies",
            "asserted": 1549680000,
            "value": "https://doi.org/10.1038/s41431-018-0219-y",
            "source": "https://grid.ac/institutes/grid.240952.8",
            "by": "self"
        }
    },
    {
        "iss": "https://other.example2.org/oidc",
        "sub": "abcd",
        "iat": 1580000400,
        "exp": 1581208000,
        ...
        "ga4gh_visa_v1": {
            "type": "ResearcherStatus",
            "asserted": 1549680000,
            "value": "https://doi.org/10.1038/s41431-018-0219-y",
            "source": "https://grid.ac/institutes/grid.240952.8",
            "by": "so"
        }
    },
    {
        "iss": "https://broker.example3.org/oidc",
        "sub": "999999",
        "iat": 1580000500,
        "exp": 1581208000,
        ...
        "ga4gh_visa_v1": {
            "type": "LinkedIdentities",
            "asserted": 1549680000,
            "value": "10001,https:%2F%2Fissuer.example1.org%2Foidc;abcd,https:%2F%2Fother.example2.org%2Foidc",
            "source": "https://broker.example3.org/oidc",
            "by": "system"
        }
    }
]
```
