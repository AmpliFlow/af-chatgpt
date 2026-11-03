# Proposed license and policy text

Prepared 2026-11-02. These are drafts for owner decision, not legal advice, approval, or an effective grant of rights. Nothing here changes LICENSE, the website, customer permissions, or publication status.

## Sources checked

- [Repository LICENSE](../LICENSE): binary-only internal-use grant; copying, distribution, modification, and sublicensing restricted.
- [Live Terms of Service](https://www.ampliflow.com/terms/): fetched with curl on 2026-11-02; published 2026-07-03, effective 2026-08-02. Both automation prohibitions below remain present. Also checked Intellectual Property Rights, AI and Machine Learning Use of Data, Use of AI Providers, and the policy-change provisions.
- [Live SaaS privacy policy](https://www.ampliflow.com/privacy-policy/): fetched with curl on 2026-11-02; published 2026-07-03, effective 2026-08-02. Optional AI disclosures describe tenant-admin-enabled providers, not clearly external ChatGPT/MCP use.
- [Plugin manifest](../plugins/ampliflow/plugin.json) and [MCP configuration](../plugins/ampliflow/mcp.json): package describes account authentication, permission-limited reads, user-confirmed changes, and the hosted MCP endpoint. These describe intended integration behavior, not authenticated runtime proof. No server source was researched.

## 1. Proposed LICENSE addendum

Append only if adopted by Cognit Consulting AB. This text does not relicense the AmpliFlow server or customer records.

### AmpliFlow ChatGPT package exception

For this exception, "Package" means the AmpliFlow ChatGPT plugin submitted by Cognit Consulting AB, including its plugin and MCP manifests, skills, supporting references, and bundled assets, in source form and any packaged form. It excludes the AmpliFlow service implementation, credentials, and customer data.

Notwithstanding the binary-form limitation in section 1 and the restrictions in section 2(a)-(c), Cognit Consulting AB grants OpenAI a non-exclusive, royalty-free, worldwide license to receive, copy, host, inspect, scan, test, and review the Package for ChatGPT submission, security, compatibility, and operation, and to distribute the Package through ChatGPT's plugin installation and update mechanisms. OpenAI may use service providers acting on its behalf solely for these purposes and may authorize end users to receive and use the Package on the terms below. Technical repackaging necessary for these purposes is permitted; substantive modification and unrelated redistribution are not.

Customers and their authorized users may download, copy as necessary to install, install, and use the unmodified Package in source or packaged form with ChatGPT solely for their internal business use of AmpliFlow. Every service request remains subject to authentication, the connected account's permissions, applicable tenant restrictions, and the AmpliFlow service terms. This exception grants no service access or permission to act for another account.

Bundled AmpliFlow names and logos may be displayed only as supplied to identify this Package in its listing, installation, and use. Ownership of all marks remains unchanged; no other trademark use, endorsement claim, or removal or alteration of proprietary notices is permitted.

This exception permits no sale of the Package, competing product, unrelated derivative work, or model training. It grants no rights in customer data or third-party materials beyond rights Cognit Consulting AB is entitled to grant. All other license provisions, including termination, warranty disclaimer, limitation of liability, and governing law, remain unchanged. This exception controls only the express conflicts identified above and the limited display of bundled marks described here.

## 2. Proposed replacements for exactly two terms clauses

Replace only the two quoted sentences below. Leave the other prohibited activities intact. The proposed wording expressly approves this integration, rather than relying on an undefined exception for bots.

### User Representations

Current:

> You will not access the Service through automated or non-human means, whether through a bot, script, or otherwise.

Replacement:

> You will access the Service through automated or non-human means only through integrations expressly approved by us and within their documented scope. Our AmpliFlow ChatGPT integration using our designated MCP endpoint is an approved integration for authenticated, account-authorized requests. Such use remains subject to your account permissions, applicable tenant restrictions, documented limits, and any required user confirmation. This permission does not authorize scraping, crawling, bulk extraction outside the integration's documented scope, or bypassing authentication, access controls, or rate limits.

### Prohibited Activities

Current, under "As a user of the Service, you agree not to":

> Use any automated system, such as scripts or bots, to access the Service.

Replacement, retaining that introductory wording:

> Use automated systems, including scripts, bots, scrapers, or crawlers, to access the Service except through integrations expressly approved by us, within their documented scope and your account permissions, and subject to applicable tenant restrictions, documented limits, and any required user confirmation. Our AmpliFlow ChatGPT integration using our designated MCP endpoint is approved on that basis. This exception does not permit bypassing authentication, access controls, or rate limits, or bulk extraction outside the integration's documented scope.

### AI and Machine Learning Use of Data: proposed clarification

Insert after the existing sentence requiring prior written consent for training, development, or similar applications:

> For clarity, authenticated use of our approved AmpliFlow ChatGPT integration to retrieve, summarize, analyze, or make explicitly confirmed changes to account-authorized records is permitted within the integration's documented scope. This permission concerns inference for the requested task; it does not authorize using service data to train or develop models, opting that data into model training, or bypassing your organization's data-handling rules. The terms and data controls of the external ChatGPT account or workspace also apply.

## 3. Proposed SaaS privacy subsection

Insert as a separate subsection beside "Optional AI providers", not as another provider example in that embedded-AI section. The text below states the known functional flow; unresolved operational details are listed separately, not invented.

### External ChatGPT access through MCP

The AmpliFlow ChatGPT integration connects an external ChatGPT session to AmpliFlow through our Model Context Protocol (MCP) endpoint. When you connect your AmpliFlow account, ChatGPT can send tool requests to that endpoint on your behalf. Requests can include search criteria, record references, and content for a requested change. AmpliFlow processes requests within the connected account's permissions and returns tool results to ChatGPT. Depending on the request, results can include business record content, personal information contained in those records, and operation results or errors. Authorized change requests can update AmpliFlow records.

Information returned to ChatGPT leaves the AmpliFlow service and becomes available to ChatGPT for the conversation. Consider which records and personal information your request will expose before using the integration, and use it only for information and actions your organization authorizes.

This is distinct from AI features embedded in AmpliFlow, where a tenant administrator enables an AI capability and selects a provider. The embedded-AI opt-in and API-provider descriptions do not establish the settings or processing terms for your external ChatGPT account. Review the privacy terms and data controls applicable to the ChatGPT account or workspace you use; do not assume that statements about OpenAI API processing describe ChatGPT processing.

## 4. Owner-only decisions and factual confirmations

No committee, new legal sign-off workflow, or extra approval layer is proposed. [MCP-EVIDENCE.md](MCP-EVIDENCE.md) records the source-supported technical facts and their deployment limits so you do not need to research the code. The authorized owner must decide the rights and policy wording and confirm the remaining operational facts:

- **Rights:** Confirm Cognit Consulting AB may grant the proposed rights for all bundled source, skills, references, and assets, including the limited logo display, and adopt or revise section 1. Confirm whether OpenAI's actual submission agreement requires any additional rights; this draft is not a representation that its terms have been accepted.
- **Integration approval:** Decide whether to expressly approve the ChatGPT/MCP integration under section 2. Confirm the approved endpoint and documented operation limits against the separate technical review. An authenticated account is not evidence of organizational approval.
- **Existing AI restriction:** The terms separately prohibit using service data for AI training or development "or for any similar applications" without prior written consent. Approve or revise the proposed inference clarification above before publication; the two automation replacements alone do not settle that ambiguity.
- **External-data facts:** Confirm the deployed request/result flow and actual data categories, any tenant enablement or approval requirement for external MCP, the contractual entities and their roles, hosting locations and transfers, recipients, logging, retention/deletion, and training controls for this external path. Use deployment evidence and the applicable ChatGPT agreement, not embedded-AI API defaults. Supply any missing disclosures and reconcile the existing EU-storage and sharing statements before publishing; this subsection alone does not establish a complete privacy notice.
- **Adoption and publication:** Choose final wording and publication/effective dates, then authorize the license and website changes. The current terms and privacy policy state that revisions take effect at least 30 days after publication. No date, publication, consent, or rights approval is supplied by this preparation.
