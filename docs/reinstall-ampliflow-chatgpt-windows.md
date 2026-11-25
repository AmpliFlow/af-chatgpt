# Remove and reinstall AmpliFlow in ChatGPT Desktop for Windows

Open a new ChatGPT Desktop **Work** conversation and paste this whole document as your message. **Do not tag `@AmpliFlow`**. This checklist is for a workspace where the existing AmpliFlow plugins do not work.

## ChatGPT: start here

Guide the user through a full removal and reimport of the AmpliFlow marketplace, then reinstall and test the plugin. Reply in the user's language. Do not search for or call AmpliFlow during diagnosis. Skip any step the user has already confirmed. Give one short numbered list at a time, one action per line, then wait for the result. Ask for copied text **or** a cropped screenshot of the relevant screen. Tell the user to hide names, emails, customer data, and sign-in details before sharing. If a named button is missing, ask what they see.

**Start with the account menu.** Give the user these steps and wait for the result:

1. In ChatGPT Desktop, click your profile or workspace icon at the bottom left of the sidebar. Use the account menu, not the ChatGPT/Codex switcher.
2. If the menu shows a workspace name, check that it is the one where you use AmpliFlow. Select the correct workspace first if you need to switch.
3. Click **Workspace Settings** if shown. It opens the workspace admin site at `admin.openai.com` in your browser. It may open on **Members**; that is expected.
4. In the browser sidebar, look under the **Plugins** heading for **Marketplaces**. If it is not visible, click **Plugins**, open the catalog named after your workspace, and open an AmpliFlow entry. Then check the sidebar again. If you still cannot open **Marketplaces**, paste the menu labels or a cropped screenshot. Do not paste the browser URL; it can contain your email and workspace ID.

Seeing **Plus**, **ChatGPT**, or **Codex** does not establish how the plugin was installed. If you cannot access workspace settings, ask how AmpliFlow was installed before choosing the next path.

- **Workspace import:** Start with Step 1. If the user is not an admin, give them Steps 1–2 to forward to their workspace admin.
- **Personal install or source unknown:** Start with **Personal marketplace** below. If the user was expecting a managed workspace but cannot find it, ask its admin to confirm the user has access before changing anything.

### Personal marketplace: remove and add the source again

Use this path for a user-installed GitHub marketplace. It does not require a ChatGPT workspace admin. OpenAI documents the following marketplace commands for **Codex CLI**, and documents that configured marketplaces appear in the Desktop **Work** or **Codex** Plugins Directory. This path requires an existing Codex CLI on the same Windows PC; the commands are documented, but this recovery path has not been tested on Windows Desktop.

1. Open **PowerShell** on the Windows PC that runs ChatGPT Desktop.
2. Run `codex plugin marketplace list`. Paste back only the AmpliFlow marketplace name you see, without local paths. If `codex` is not recognized, stop and report that the CLI is missing. Do not install software or delete Windows app data to resolve that error.
3. If the list contains `ampliflow-pilot`, run `codex plugin marketplace remove ampliflow-pilot`. If it contains `ampliflow`, run `codex plugin marketplace remove ampliflow`. Remove only those AmpliFlow entries that are listed. If neither is listed, skip removal.
4. Run `codex plugin marketplace add https://github.com/AmpliFlow/af-chatgpt`. Paste whether it succeeded or the error, without credentials or local paths.
5. Reopen ChatGPT Desktop in **Work**. Open **Plugins** and select **AmpliFlow** as the marketplace source. Continue at Step 3, using that source instead of **Your workspace**. If the source is missing, stop and capture the Plugins Directory listing. A successful CLI add alone does not verify Desktop can see it.

[OpenAI's marketplace commands](https://learn.chatgpt.com/docs/developer-commands) and [where marketplaces appear in Desktop](https://learn.chatgpt.com/plugins/build/plugins)

## 1. Delete the old marketplace (workspace admin)

**This removes every plugin imported from the AmpliFlow marketplace for the whole workspace.** Tell affected users before proceeding. A workspace admin must confirm and perform the deletion.

1. In the browser opened by **Workspace Settings**, verify that you are in the affected workspace. If you landed on **Members**, stay in that workspace.
2. Under **Plugins** in the sidebar, click **Marketplaces**. If access is denied, ask a workspace admin to take over.
3. Click **Add**. Wait for **Checking GitHub plugin availability...** to finish. If **Import marketplace** is selectable, close the menu and continue. If it is disabled, follow **Enable GitHub before deleting** below. Do not delete the marketplace until you can reimport it.
4. Find the row for `ampliflow/af-chatgpt`. Note who has access and the installation policies for its plugins so you can restore them after reimporting.
5. In that row, click **Settings for ampliflow/af-chatgpt**. In **Marketplace settings**, select **Delete marketplace** and review the confirmation. Leave unrelated marketplaces alone.
6. Check that the old marketplace and its imported plugins are gone. Paste what remains in the AmpliFlow listings, or paste a cropped screenshot. If an AmpliFlow entry remains, check its source: a separately uploaded plugin is not removed with the marketplace. Do not delete an entry whose source you have not confirmed.

### Enable GitHub before deleting (workspace admin)

Use these steps if **Import marketplace** says **Enable the GitHub plugin to import a marketplace.**

1. In the admin sidebar, click **Plugins**.
2. Select the **Public** catalog.
3. Search for **GitHub** and open the GitHub plugin published by OpenAI.
4. Check the button at the top of the GitHub detail page. If it says **Enable**, ask the workspace admin to enable it there if policy allows. If it already says **Enabled**, leave it enabled and continue. Check the detail page even if the catalog row looked enabled. **Configure GitHub Enterprise** is for a different setup.
5. If ChatGPT asks you to connect GitHub, use the importing admin's account with read access to `AmpliFlow/af-chatgpt`. Do not paste the authorization screen or link into the chat.
6. Go back to **Marketplaces > Add** and wait for the check to finish. When **Import marketplace** says **Keep plugins updated from GitHub**, open it and confirm the **Import marketplace from GitHub** form appears. Click **Cancel** without submitting. Tell ChatGPT whether the form opened or paste the final disabled message. If you cannot open the form, keep the old marketplace in place and produce the support log.

## 2. Import the marketplace again (workspace admin)

1. On the **Marketplaces** page, click **Add > Import marketplace**.
2. Paste `https://github.com/AmpliFlow/af-chatgpt` into **Source**.
3. Leave **Path** and **Branch, tag, or commit** empty. Select **Import marketplace** and authorize GitHub if prompted.
4. Check **Import results** for errors. The marketplace name is **AmpliFlow**. It contains **AmpliFlow** and **AmpliFlow (Beta Channel)**.
5. Restore the intended installation policy and role access. Make the production plugin available to the affected users. Enable Beta for users who are meant to use that channel.
6. Paste the import result or a cropped screenshot of it. If the import failed, stop here and capture the error rather than reinstalling an old entry.

[OpenAI's marketplace import and deletion guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github)

## 3. Reinstall and sign in (Windows user)

1. Save any unsaved work and reopen ChatGPT Desktop. For a managed import, select the same work workspace. If you may lose this conversation, save a short note of the completed steps first.
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
