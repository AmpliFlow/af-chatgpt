# Diagnose and reinstall AmpliFlow in ChatGPT Desktop for Windows

**For the Windows user:** Open a new **Work** conversation in ChatGPT Desktop in the workspace where you use AmpliFlow. Paste this document in full and send it as your message. Stay in the conversation so you can check settings and report what you see. The checklist works without a working AmpliFlow connection.

## Instructions for ChatGPT

Run this as an interactive support session. The goal is to restore the user's AmpliFlow project read in ChatGPT Desktop **Work** on Windows and document what happened. The checklist does not depend on the AmpliFlow plugin, browser access, local tools, an admin account, or any earlier conversation.

**Start now:** Ask which AmpliFlow channel they intended to use, what they see or what error they get, and whether they are in a new **Work** conversation in the intended workspace. Then ask for the one screen or result that will determine the next step. Wait for their reply instead of listing every possible reset. A user can say `finish` at any time; give the two outputs below with any gaps marked.

Label each result **Observed** (you saw the screen or tool output yourself; say where), **User-reported** (the user or admin told you), **Not checked** (the check was skipped or not yet done), or **Unavailable** (the relevant control or access was missing). Keep the observation separate from what it suggests. A successful public probe, a folder timestamp, and a successful AmpliFlow tool call are different kinds of evidence.

Before asking the user to close or reset ChatGPT, give them a short, redacted checkpoint to save outside the app: what they saw, what they already tried, and the next check. If they cannot return to this conversation, tell them to paste this document and that checkpoint into a new **Work** conversation. Resume from the checkpoint; do not repeat a removal or reset just because the conversation is new.

### Task 1: Record the starting state

- [ ] Ask for the channel they intended to use, the exact symptom or error, and when it occurred, including time zone. Record the Windows version and ChatGPT Desktop and plugin versions if visible. Confirm they selected the intended workspace and are in **Work**, not **Chat**. Use a label such as `work workspace` instead of its real name in the support log.
- [ ] Ask the user to open **Plugins > Installed**. Note whether **AmpliFlow**, **AmpliFlow (Beta Channel)**, duplicate entries, or entries marked **No longer in source** appear. In the affected plugin, check the gear next to its server under **MCP servers** and the connection under **From plugins**, if shown. Record the connection host and path without query parameters, and whether the UI offers **Authenticate**, **Reconnect**, or **Disconnect**. Do not ask the user to open or copy tokens, cookies, or OAuth callback URLs.
- [ ] Compare the connection with the expected values below. [Version 0.10.2](https://github.com/AmpliFlow/af-chatgpt/releases/tag/v0.10.2) renamed the GitHub marketplace to **AmpliFlow** (`ampliflow`) and moved Beta from the retired `.cc` host to `.com`. The Beta sign-in issuer also changed, so old Beta authorization cannot be reused. The production resource URL stayed the same in this release. Both plugins keep their existing plugin identities. Check the URL and source even if the name looks right. A stale URL does not tell you where the old value is stored.

  | Plugin | Connection URL | Expected OAuth issuer |
  | --- | --- | --- |
  | AmpliFlow | `https://mcp.ampliflow.com/mcp` | `https://mcp.ampliflow.com` |
  | AmpliFlow (Beta Channel) | `https://mcp.ampliflow.com/mcp-beta` | `https://mcp.ampliflow.com/oauth/beta` |

- [ ] If you have web or network access, optionally check the public [production discovery document](https://mcp.ampliflow.com/.well-known/oauth-protected-resource/mcp) or [Beta discovery document](https://mcp.ampliflow.com/.well-known/oauth-protected-resource/mcp-beta). Record the returned resource and authorization server. Label where you checked from if known: a public check from ChatGPT's tools does not prove the Windows PC can connect or that the installed plugin uses that URL. Do not send credentials to perform this check.

### Task 2: Check the workspace import and narrow the problem

- [ ] If the plugin is missing, duplicated, or shows an old URL, ask a workspace admin to check **Admin console > Plugins > Marketplaces** in the affected workspace. Verify the source is `https://github.com/AmpliFlow/af-chatgpt` and check **Path** and **Branch, tag, or commit**. A source pinned to an old revision won't pick up the migration. For the standard setup, leave both fields empty to use the repository root and default branch. Ask the admin to select **Sync now** and review the result and any errors. **Refresh plugin list** only reloads the list.
- [ ] If the workspace entry is current, check whether the symptom also occurs for another eligible user or on another supported desktop, if one is available. Record whether the comparison used the same workspace, channel, and account or a different account. A problem on just one PC makes local state worth checking; it does not prove a cache problem. If multiple users see the same old entry, check the marketplace source, policy, and duplicate manual uploads before proposing a Windows reset.

### Task 3: Investigate possible local state without changing it

- [ ] If the issue appears local, ask the user to fully close and reopen ChatGPT. Compare the plugin name, version, connection URL, and error before and after. If the browser opens the wrong account during sign-in, ask the user to select the intended account themselves. Record whether this changed the outcome.
- [ ] If you have a tool running on the user's Windows PC, first ask permission for a **read-only metadata check**. You may check the installed ChatGPT package version, whether Windows offers **Repair** or **Reset**, and whether a ChatGPT-specific cache location documented for that installed build exists and when it was last modified. Use only the documented location; if none is available, record **Not checked: no documented cache location for this build**. A folder's existence or timestamps do not show that it holds the old plugin URL. If you cannot inspect the PC, use the information the user can see in Windows Settings and label it **User-reported**.

Do not search the user's profile or recursively scan AppData. Do not open or copy cache contents, account databases, browser profiles, credential stores, environment variables, or raw diagnostic archives. Do not delete files or Windows credentials, run reset commands, uninstall a plugin, change workspace settings, or send email on the user's behalf. The user or admin makes those changes after reviewing the consequences.

### Task 4: Guide the user through the appropriate repair

Choose the next action from the evidence:

| What you found | What to do next |
| --- | --- |
| The workspace import is missing, pinned to an old revision, or shows a sync error. | Ask the admin to fix the import and read back the result. Reinstalling on Windows will not fix a stale workspace import. |
| The workspace import is current, but the installed entry points to the retired host or the wrong channel. | Reinstall only the affected plugin from **Your workspace**. Check the source of any duplicate before removing it. |
| The URL matches, but the user sees a sign-in prompt, the wrong account, or an authorization error. | Reconnect the intended account. If the fresh sign-in fails, record the sanitized error and where it appeared. Do not assume the failure is a cache problem. |
| The current entry and fresh sign-in work on another comparable desktop, but this PC still fails. | Compare before and after closing and reopening the app. Consider **Repair** or **Reset** only if the problem persists. |
| A current import and fresh sign-in fail on multiple desktops, or you cannot verify the workspace import. | Escalate with the log. Do not delete the marketplace or reset multiple PCs as a test. |

After each repair the user actually performs, run Task 5. If it fails, use the new observation to choose the next step. Do not run every repair in sequence.

**Reconnect or reinstall just the affected plugin.** After the admin verifies the workspace import, go to **Settings > Plugins** and review the affected AmpliFlow connection. If **Disconnect** is available for the old connection, review the warning and disconnect only the affected account. In **Plugins > Installed**, uninstall the affected plugin if the action is offered, then reinstall the current entry from **Your workspace**. If workspace policy installs it automatically, ask the admin about any stale entry you cannot remove. Open the correct connection and select **Authenticate** or **Reconnect** as offered. Beta users need fresh authorization. Leave unrelated plugins and accounts alone. See [OpenAI's account connection guide](https://help.openai.com/en/articles/20001494-connecting-and-managing-app-accounts-in-chatgpt).

**Remove and reimport the marketplace when a workspace-wide reset is needed.** A workspace admin should schedule this with affected users. Deleting the marketplace removes **every plugin imported from it for the whole workspace**. Users should disconnect and uninstall their existing AmpliFlow plugins where the UI allows, then close the desktop app. In **Admin console > Plugins > Marketplaces**, the admin identifies the exact AmpliFlow GitHub source, records the imported entries and their access policies, deletes only that marketplace, and verifies that the old entries are gone. Separately uploaded plugins are not removed by this action. In **Plugins > Add > Import marketplace**, the admin enters `https://github.com/AmpliFlow/af-chatgpt`, leaves **Path** and **Branch, tag, or commit** empty for the standard setup, and reviews the import report. Restore intended role access and installation policies, then ask users to reopen Desktop, reinstall the intended plugin, and sign in. See [OpenAI's marketplace guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).

**Reset the Windows app when the current import and fresh sign-in still fail on one PC.** Save unsaved work outside ChatGPT and make sure the user can sign in again. In Windows **Settings > Apps > Installed apps**, open the menu next to **ChatGPT** and choose **Advanced options**. If offered, **Repair** is a less disruptive option, but it preserves app data. **Reset** deletes local app data, which can include preferences and sign-in details. The user should read the Windows warning before confirming, then reopen ChatGPT, sign in to the same workspace, and reconnect the plugin. If **Reset** is unavailable, refer the user to IT or OpenAI Support. A Windows reset does not reimport a workspace marketplace, and OpenAI does not document it as a complete purge of plugin or OAuth records. See [OpenAI's Windows reset instructions](https://help.openai.com/en/articles/9982051-using-the-chatgpt-windows-app) and [Microsoft's Repair and Reset documentation](https://learn.microsoft.com/en-us/windows/msix/desktop/managing-your-msix-reset-and-repair).

### Task 5: Verify the result

- [ ] In a **new Work conversation** in ChatGPT Desktop, select the intended plugin and ask: **"What projects do I have? Do not change anything."** Look for an actual AmpliFlow tool call and result. If the test is in another conversation, ask the user whether they saw the call succeed or an error; you cannot see the other conversation just because it is on the same PC. A successful read can return an empty list. A plugin mention or an answer without a visible tool result is unverified. Record `Succeeded`, `Failed`, `Unverified`, or `Not run` without copying project names or records into the log.

## Output 1: Step-by-step instructions for this user

Explain what you observed, what it suggests, and what is still unknown. Give a numbered list tailored to the user's situation, with the exact next clicks where verified. Label each step **User** or **Workspace admin**. Put the impact and who must confirm it before any workspace deletion or Windows reset. End with the read-only check and what counts as success. If no tool access was available, give manual instructions and say which observations the user still needs to collect.

## Output 2: `ampliflow-chatgpt-support-log.md`

Create a Markdown file if you can; otherwise output the Markdown in a single copyable code block. Summarize relevant session output and debugging observations. Include sanitized error text and the result of each step, not the full transcript, raw command output, screenshots, or system dumps. Redact names, workspace and tenant identifiers, email addresses, local usernames and paths, customer records, passwords, codes, cookies, tokens, and URL query strings or fragments. Record `Not checked` where evidence is missing. Ask the user to review the log and, if they choose, email it to **patrik@ampliflow.com**. Do not send it automatically.

```markdown
# AmpliFlow ChatGPT Desktop support log

- Incident time and time zone:
- Windows version / ChatGPT Desktop version / AmpliFlow plugin version:
- Intended channel and selected mode (Work or Chat):
- Marketplace source, revision, and last sync/import result, if known:
- Installed entries and any duplicates:
- Before: connection host/path and visible sign-in controls:
- After: connection host/path and visible sign-in controls:
- Public discovery check: resource, issuer, where checked, or not checked:
- Comparison on another desktop/account and what was held constant:
- Local checks: restart result, Windows app metadata, Repair/Reset availability:
- Repair actions taken and by whom (include whether Reset was used):
- Sanitized error message or relevant session result:
- Final Work-mode project read: Succeeded / Failed / Unverified / Not run:
- Suspected cause, supporting evidence, and remaining unknowns:
- Next action, who can take it, and whether an admin is needed:

| Step | Evidence status | Observation or result |
| --- | --- | --- |
| | Observed / User-reported / Not checked / Unavailable | |
```
