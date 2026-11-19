# AmpliFlow for ChatGPT

Use AmpliFlow in ChatGPT Desktop **Work** mode to review project tasks, portfolios, goals, risks and controls, improvements, and checklists. The general AmpliFlow skill can also answer other questions about your records and make changes you explicitly confirm.

This GitHub marketplace does not make AmpliFlow tools available in Desktop **Chat** mode, on the web, or on mobile.

## Import the marketplace

A ChatGPT workspace admin can add AmpliFlow:

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Enter `https://github.com/AmpliFlow/af-chatgpt` as the source and leave **Path** empty.
3. Import the marketplace and make **AmpliFlow** available to users. Enable **AmpliFlow (Beta Channel)** only for users who want beta.

To update an existing marketplace, select **Sync now** on its GitHub source. See OpenAI's [marketplace import guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).

## Connect and try it

1. Install **AmpliFlow** from the Plugins Directory and sign in to your AmpliFlow account when prompted.
2. Start a new ChatGPT Desktop conversation in **Work** mode.
3. Add `@AmpliFlow` and ask: "What projects do I have?"

For a focused review, try: "Show incomplete tasks in [project name], including assignees and due dates. Do not change anything."

AmpliFlow uses the permissions of your connected account. The six focused reviews are read-only. For a change, review the exact record and proposed values before confirming. ChatGPT receives the AmpliFlow data needed to answer your request, so use the integration only with records your organization allows you to share with ChatGPT.

## Troubleshooting

- **AmpliFlow is visible but its tools are unavailable.** Start a new Desktop **Work** conversation. The mention can appear in **Chat** even though the tools aren't available there.
- **Sign-in fails or an older installation connects to the wrong channel.** Check the installed connection against the table below. If the URL is wrong, ask your workspace admin to sync the marketplace and reinstall the affected entry if needed. Sign in again when changing channels; authorization is specific to the connection URL.
- **A change could not be verified.** Check the record in AmpliFlow before asking ChatGPT to make the change again.

| Plugin | Connection URL |
| --- | --- |
| AmpliFlow | `https://mcp.ampliflow.com/mcp` |
| AmpliFlow (Beta Channel) | `https://mcp.ampliflow.cc/mcp-beta` |

For help with your AmpliFlow account or connection, contact [AmpliFlow support](https://www.ampliflow.com/support/).

## License

Copyright (c) 2026 Cognit Consulting AB, trading as AmpliFlow. All rights reserved. See [LICENSE](LICENSE).
