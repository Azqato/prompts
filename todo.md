analyze these resources and extract valuable information from thrm
as well as any reusable prompts that can be added to the main website in reference to these resources

https://x.com/twoclipping/status/2103835273813496100?s=46
https://x.com/shiri_shh/status/2103521939134550246?s=46
https://x.com/himanshubuildss/status/2103374896147378635?s=46



also do the following:
Update the documentation audit prompt so it permanently includes and maintains docs/PROMPTS.md.

Exact changes required:

1. Create the file docs/PROMPTS.md if it does not exist.  
   Populate it with a short header and an empty "Current Next Steps" section ready for bullets.

2. Edit the main documentation audit prompt (the long prompt that starts with "Perform a full documentation audit of the /docs folder") as follows:

- At the very beginning of the Steps section, insert a new mandatory Step 0:

  "0. Open and read docs/PROMPTS.md in full before any other action. Treat its contents as the current working todo list and instruction set for this session. If the file is missing, create it with a header and an empty Current Next Steps section."

- In the Standards section, add this rule:

  "docs/PROMPTS.md is an operational working file. Never merge its content into PRD.md, DESIGN.md, or PATCHNOTES.md. Keep it separate. Review it for accuracy against the latest conversation and code state. Update its bullet list when next steps change. After any major documentation or code change, append or revise the Current Next Steps section so it stays current."

- In the folder structure enforcement section, add docs/PROMPTS.md as a required file that lives inside /docs and must not be moved or deleted by the audit.

- In the final summary instructions, require the audit to report whether PROMPTS.md was reviewed and what (if anything) was updated in it.

3. Do not change any other part of the documentation audit prompt except the additions above.

4. After making the edits, confirm the new Step 0 is present, the non-merge rule is present, and docs/PROMPTS.md exists.
