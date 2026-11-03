from bs4 import BeautifulSoup
import os
from pprint import pprint
import re

anchors = set()
local_hrefs = set()
external_hrefs = set()

for root, dirs, files in os.walk('build'):
    for relpath in files:
        if 'htm' in relpath:
            with open(os.path.join(root, relpath)) as fh:
                content = fh.read()
                
            if relpath == 'index.html':
                base = ''

            base = relpath.replace('.html','')

            soup = BeautifulSoup(content, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                name = link.get('name')
                if href is None:
                    anchors.add(f"{base}#{name}")
                    #print("No href: "+str(link))
                else:
                    if href in ['/local/',
                                    '/local/aai-openid-connect-profile',
                                    '/local/aai-faq',
                                    '/local/changes-1_2']:
                        pass
                    elif href.startswith('#'):
                        local_hrefs.add(f"{base}{href}")
                    else:
                        external_hrefs.add(href)

            for heading in ['h1','h2','h3', 'strong']:
                for link in soup.find_all(heading):
                    id = link.get('id')
                    if id is not None:
                        anchors.add(f"{base}#{id}")
                        #print("No href: "+str(link))



line_links_from_duri_passport = """
[GA4GH AAI OIDC Profile](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#terminology)
* <a name="term-passport"></a>**[Passport](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-passport)**
* <a name="term-passport-scoped-access-token"></a>**[Passport-Scoped Access Token](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-passport-scoped-access-token)**
* <a name="term-passport-clearinghouse"></a>**[Passport Clearinghouse](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-passport-clearinghouse)**
* <a name="term-visa-assertion"></a>**[Visa Assertion](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-visa-assertion)**
* <a name="term-visa-assertion-source"></a>**[Visa Assertion Source](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-visa-assertion-source)**
* <a name="term-visa-issuer"></a>**[Visa Issuer](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-visa-issuer)**
* <a name="term-visa"></a>**[Visa](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-visa)**
* <a name="term-jwt"></a>**[JWT](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-jwt)**
* <a name="term-ga4gh-claim"></a>**[GA4GH Claim](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-ga4gh-claim)**
* <a name="term-broker"></a>**[Broker](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-broker)**
Please see the [Flow of Assertions](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#flow-of-assertions)
    [GA4GH AAI Specification Visa formats](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#visa-issued-by-visa-issuer)
    [GA4GH AAI Specification](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md)
[Conformance for Visa Issuers](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#conformance-for-visa-issuers)
  for [Visa Document Token Format](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#visa-document-token-format)
- For [Visa Access Token Format](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#visa-access-token-format)
- REQUIRED.The section [Signing Algorithms](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#signing-algorithms)
if the Visa is encoded as a [Visa Access Token](https://github.com/ga4gh/data-security/blob/master/AAI/AAIConnectProfile.md#term-visa-access-token-format).
"""

print ("\n\nChecking anchors to which DURI passport links\n")
for line_from_duri in line_links_from_duri_passport.split('\n'):
    #print(line_from_duri)
    m = re.search(r'AAIConnectProfile.md#([^)]*)', line_from_duri)
    if m:
        target = f"aai-openid-connect-profile#{m.group(1)}"
        if target in anchors:
            print (f"valid {target}")
        else:
            print (f"INVALID ------ {target}")

#pprint(anchors)

print ("\n\nChecking links within AAI\n")
for local_href in local_hrefs:
    if local_href in anchors:
        print(f"valid {local_href}")
    else:
        print(f"INVALID ---- {local_href}")

print ("\n\nListing links from AAI to external hrefs\n")
pprint(external_hrefs)

