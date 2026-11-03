### GA4GH: Access Product Line

**Product Line Mandate:**

In principle, groups around the world are making datasets available to bona fide
researchers through data sharing repositories such as EGA and dbGaP. Researchers
can login to these resources, identify datasets of interest, apply for access,
be granted access, and then copy data sets to their local environments.

In practice, however, this process is fraught with difficulties due to the
human-intensive nature of each step. This leads to the following shortcomings in
our current access framework:

-   It is inconsistent: different Data Access Committees (DACs) may reach
    different conclusions regarding appropriate secondary data uses. For
    example, it is not uncommon for a consent form to state that a dataset can
    be reused for “diabetes and related conditions”; different repositories may
    interpret what constitutes a “related condition” differently.

-   It is not scalable: Researchers fill out forms that articulate their
    research purpose, and DACs review these forms to see if they are consistent
    with the terms of the informed consent. The number of requests for access to
    human subjects data is growing at a supralinear rate, and it is growing
    increasingly difficult for DACs to keep up.

-   It is cumbersome: DACs have a difficult time identifying who a bona fide
    researcher is, and have difficulty validating their identity. Similarly,
    researchers have difficulty understanding what datasets can be used to
    support their research endeavor. For example it is impossible to answer even
    simple questions such as, “What samples in your repository can be used as
    controls for my study?”

*The mandate of this group is to develop machine-readable standards that will
facilitate access to data sets by addressing these challenges.*

At a concrete level, data from human subjects has two axes of access control:

![fig 1](aai%20background%20fig%201.JPG)

1.  Authentication and Authorization Infrastructure (AAI) - These specify the
    collection of researchers that may access the dataset at any given time. For
    example, it may be the case that only researchers that are members of a
    consortium may access a dataset for the first year after generation.

2.  Data Use - when human subjects are consented as participants in the study,
    the informed consent form specifies appropriate restrictions on secondary
    data use. For example, it may stipulate that the data may be used only for
    “cancer research in a non-profit setting.” Similarly, data owners may place
    additional restrictions on data use.

Each of these axes are independent--for example a researcher may have permission
to access a dataset but, because her research purpose is inconsistent with the
data use restrictions specified in the informed consent form, she may not be
able to use it for her investigation. Similarly, a researcher’s purpose may be
entirely consistent with the data use restrictions specified by the informed
consent form but, because she is not a member of the consortium, she may not be
able to access it. *Only when permissions and data use are both appropriate can
a researcher access a given dataset.*

Thus, our mandate can be restated as

1.  Establish researcher identities - The world is in need of a consistent
    system for i) defining who a bona fide researcher is, ii) an identity
    provider that respects this definition of a bona fide researcher to provide
    an electronic identity that can travel with the researcher across various
    data sharing repositories (in effect, the “Library Card” model that is
    already initiated within GA4GH).

2.  Specify a data use ontology - This ontology will be used to both state the
    secondary data use restrictions for datasets, as well as researchers’
    purposes for wishing to access them. By expressing them in an ontology, it
    becomes possible to *compute* whether a given researcher’s purpose is
    consistent with a given data use restriction.

**Relationship to “Data Discovery” Product Line:**

The mandate of this group could potentially overlap with the “Data Discovery”
product line, which charged with efforts such as Beacon/Matchmaker, Library
Cards for Registered Access Data, and data use oversight systems. As an initial
strawman, we propose that this group focus on developing the standards for AAI
and Data Use, whereas the mandate of the discovery group is to see them reduced
to practice in various driver projects such as Beacon.

**2022 Vision:**

Our vision for the future is to create the standards that will enable the
following User Story to become a reality by 2022:

-   Jane is a new graduate student in the Birney lab at EBI, working on complex
    trait genetics.

-   On her first day in the lab, she obtains a GA4GH-compliant researcher
    identity that is recognized by data sharing repositories around the world.
    She obtains this by showing proof of identity (passport) to the EBI
    Compliance Officer (or perhaps a centralized compliance office), who issues
    her the identity.

-   She joins a consortium lead out of the University of Michigan on diabetes
    genetics, and is told that the group has placed the main dataset on the
    Microsoft cloud (Azure). The Project Manager adds her to a public whitelist
    of researchers that can access the data, and Jane is informed that it has
    only been consented for non-commercial type2-diabetes research purposes, as
    this was a requirement of the funding disease foundation.

-   Jane logs into Azure, authenticates with her “*GA4GH compliant researcher
    identity*”, and initially states that her research purpose is “diabetes” and
    she is blocked from accessing the dataset. She realizes her error and states
    “type2-diabetes” and is granted access.

-   She begins to do her research, deploying batch processing jobs using the
    GA4GH-compliant workflow execution service on Azure. She notices that one of
    the samples has a particularly interesting combination of traits (diabetes
    and hyperphosphatemia)

-   She attempts to expand the access controls on this sample to include her lab
    mate who is interested in the genetics of electrolyte abnormalities. She is
    blocked, however, as the labmate is not part of the consortia.

**Authentication and Authorization Infrastructure (AAI)**

Our aim is to build upon and extend the fruitful groundwork of the Security
Working Group, the Regulatory and Ethics Working Group, The Library Card team
and ADA-M in this domain.

As an initial strawman, we propose that the goals of this group should be to
work through the following issues:

1.  Develop an ethical and legal framework for establishing who a bona-fide
    researcher is. This will involve addressing the following

    1.  Define what it means to be a bona fide researcher. This definition will
        need to encompass not just individuals at academic institutions, but
        also people working in companies, as well as citizen scientists.

    2.  Establish a researcher code of conduct (e.g., agree not to attempt to
        re-identify research participants).

    3.  Clarify the roles of institutions and companies in validating the
        researcher and shouldering their liability. Also, understand who will
        stand behind the citizen scientist that is not based at an institution.

    4.  Articulate the repercussions of any wrongdoing and who will adjudicate
        them.

    5.  Establish a governing body that is empowered to update and modify the
        above policies.

2.  Establish a system of electronic identities that will travel with the
    researcher across repositories.

    1.  How do we leverage existing identity providers such as EGA and eRA
        Commons, and harmonize between them?

    2.  Who is able to give out identities to bona fide researchers?

3.  Encourage utilization of this system of identities by data-sharing
    repositories

    1.  Provide reference implementations for AuthN and AuthZ that respect these
        identities.

    2.  Protocols for logging researcher behavior so that it can be audited.

**Data Use Ontology:**

Stephanie Dyke et al. has developed an initial set of “consent codes” that
provide a foundation for future work. These were developed in consultation GA4GH
working groups and by reviewing dbGaP and EGA guidelines and categorization
framework . That work was also based on an examination of \~130 data user
letters processed by the Broad Institute as part of uploading data to dbGaP. It
demonstrated that \~95% of them could be structured into an ontology that
contained the following 5 main categories

1.  Disease-specific restrictions (e.g., “this dataset can only be used for
    diabetes research)

2.  Commercial restrictions (e.g., “not available for commercial use”)

3.  Restrictions to special populations (i.e., only available for studies of
    pediatric diseases, or diseases affecting a certain gender or ethnicity)

4.  Restrictions on research use (e.g., methods development).

5.  General Research Use.

![fig 2](aai%20background%20fig%202.png)

We propose that this effort be used as the starting point for developing a
full-blown data use ontology that can be reduced to practice and used by data
sharing repositories such as EGA and dbGaP. The “consent codes” are available
via [Data Use Ontology (DUO)](https://github.com/EBISPOT/DUO).

