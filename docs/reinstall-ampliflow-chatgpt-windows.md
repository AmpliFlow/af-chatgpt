# Remove and reinstall AmpliFlow in ChatGPT Desktop for Windows

Open a new ChatGPT Desktop **Work** conversation and paste this whole document as your message. **Do not tag `@AmpliFlow`**. This checklist is for a workspace where the existing AmpliFlow plugins do not work.

## ChatGPT: start here

Guide the user through a full removal and reimport of the AmpliFlow marketplace, then reinstall and test the plugin. Reply in the user's language. Do not search for or call AmpliFlow during diagnosis. Skip any step the user has already confirmed. Give one short numbered list at a time, one action per line, then wait for the result. Ask for copied text **or** a cropped screenshot of the relevant screen. Tell the user to hide names, emails, customer data, and sign-in details before sharing. If a named button is missing, ask what they see.

**Start with Step 1.** If the user cannot open the Admin console, give them Steps 1–2 to forward to their workspace admin. Do not send them to plugin settings before the new marketplace is imported.

## 1. Delete the old marketplace (workspace admin)

**This removes every plugin imported from the AmpliFlow marketplace for the whole workspace.** Tell affected users before proceeding. A workspace admin must confirm and perform the deletion.

1. Open the ChatGPT **Admin console** and select the affected workspace.
2. Click **Plugins > Marketplaces**.
3. Open the marketplace with this GitHub source: `https://github.com/AmpliFlow/af-chatgpt`. Use the source to identify it even if the display name is old.
4. Note who has access and the installation policy for the imported AmpliFlow plugins so you can restore those settings after reimporting.
5. Delete that marketplace. Read the confirmation before proceeding. Leave unrelated marketplaces alone.
6. Check that the old marketplace and its imported plugins are gone. Paste what remains in the AmpliFlow listings, or paste a cropped screenshot. If an AmpliFlow entry remains, check its source: a separately uploaded plugin is not removed with the marketplace. Do not delete an entry whose source you have not confirmed.

## 2. Import the marketplace again (workspace admin)

1. In **Admin console > Plugins**, click **Add > Import marketplace**.
2. Paste `https://github.com/AmpliFlow/af-chatgpt` into **Source**.
3. Leave **Path** and **Branch, tag, or commit** empty. Select **Import marketplace** and authorize GitHub if prompted.
4. Check **Import results** for errors. The marketplace name is **AmpliFlow**. It contains **AmpliFlow** and **AmpliFlow (Beta Channel)**.
5. Restore the intended installation policy and role access. Make the production plugin available to the affected users. Enable Beta for users who are meant to use that channel.
6. Paste the import result or a cropped screenshot of it. If the import failed, stop here and capture the error rather than reinstalling an old entry.

[OpenAI's marketplace import and deletion guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github)

## 3. Reinstall and sign in (Windows user)

1. Save any unsaved work and reopen ChatGPT Desktop. Select the same work workspace. If you may lose this conversation, save a short note of the completed steps first.
2. Click **Plugins > Installed**. If an old AmpliFlow entry remains and you can identify it as the old copy, uninstall it if the option is available. If you cannot tell which copy it is or workspace policy prevents removal, show your admin what remains.
3. Open **Plugins > Your workspace**. Install the newly imported **AmpliFlow**. Choose **AmpliFlow (Beta Channel)** instead if your admin told you to use Beta. If the workspace installs it automatically, open the new entry under **Installed**.
4. Open the installed plugin. If there is a gear under **MCP servers**, open it and look under **From plugins**. If a URL is visible, check it against the table. If it differs, stop and paste just the host and path so the admin can check the source. If it is hidden, say **URL not shown**.
5. Sign in with the intended AmpliFlow account. Use **Authenticate** or **Reconnect** if shown. Beta requires a fresh sign-in. Tell ChatGPT whether sign-in succeeded. If it failed, paste the error text or a cropped screenshot of the error. Never share sign-in screens, full sign-in links, passwords, or codes.

| Plugin | Connection URL |
| --- | --- |
| AmpliFlow | `https://mcp.ampliflow.com/mcp` |
| AmpliFlow (Beta Channel) | `https://mcp.ampliflow.com/mcp-beta` |

## 4. Verify the connection (Windows user)

1. Open a new **Work** conversation in the same workspace.
2. Select the reinstalled AmpliFlow plugin.
3. Send **"What projects do I have? Do not change anything."**
4. Come back to this conversation and say whether an AmpliFlow tool call completed. If it failed, paste the error text or a cropped screenshot with project names and records hidden.

A completed tool call can return zero projects. A plugin mention or an answer without a tool result is unverified.

## If the new plugin still fails

Compare with another eligible user or PC in the same workspace, if available. If several users are affected, stop and produce the support log; repeating the marketplace deletion or resetting PCs will not help diagnose the shared failure. If the problem is isolated to one PC, try a full app restart. Do not scan or delete AppData folders or open cache contents. If needed, follow [OpenAI's Windows reset instructions](https://help.openai.com/en/articles/9982051-using-the-chatgpt-windows-app). Save a troubleshooting note outside the app first. **Reset deletes local app data** and can remove preferences and sign-in details. The user performs the reset, signs in again, and repeats Step 4.

## ChatGPT: finish with two outputs

1. **Repair steps:** Give a numbered list of what worked or what to do next. Mark each step **User** or **Workspace admin**. If blocked, name the exact person or role that needs to act.
2. **`ampliflow-chatgpt-support-log.md`:** Create the file or give one copyable Markdown block. Record the channel, Windows/Desktop/plugin versions if known, what was removed, the import result, connection host/path, sign-in result, short sanitized errors, and the Work-mode test result. Mark what you observed versus what the user reported or did not check. Omit raw transcripts, screenshots, personal details, customer records, credentials, and URL query strings. Ask the user to review the log and email it to **patrik@ampliflow.com**. Do not send it yourself.

Give both outputs when the read works, when the user asks to stop, or when the next step requires someone they cannot reach.
