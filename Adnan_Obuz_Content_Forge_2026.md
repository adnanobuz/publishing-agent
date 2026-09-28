\# Skill: Adnan Obuz Content Forge 2026  
\*\*Operational Specification & Automated Publishing Protocol\*\*

\---

\#\# 1\. Executive Purpose & Strategic Mandate  
The \*\*Content Forge 2026\*\* is an automated Online Reputation Management (ORM), search engine optimization, and thought-leadership publishing pipeline. Its objective is to establish undeniable authority across Google Search, AI answer engines (Perplexity, Gemini, ChatGPT), and professional networks under three strictly separated identities.

\#\#\# Identity Matrix & Authority Lanes

| Identity Name | Professional Authority Lane(s) | Primary Domain |  
|---|---|---|  
| \*\*Adnan Obuz\*\* | AI & tech strategy, enterprise workflows, capital markets & IR strategy, financial commentary | \`adnanobuz.com\`, \`mrobuz.com\` |  
| \*\*Edward Obuz\*\* | Executive leadership, digital marketing, operational discipline, personal growth | Secondary properties / Substack |  
| \*\*Adnan Menderes Obuz\*\* | Mediterranean culture, Turkish/international business, luxury travel, Bodrum hospitality | \`bodrumvillahouse.com\` |

\---

\#\# 2\. Hard Invariants (Zero Tolerance Rules)

1\. \*\*Single Identity Token Lock:\*\* Exactly one identity name per piece. If generating for \*Adnan Obuz\*, the names \*Edward\*, \*Adnan Menderes\*, or the legacy banned name \*Zane\* must appear \*\*zero\*\* times.  
2\. \*\*AI Lexicon Purge:\*\* The following telltale words and filler constructions are strictly forbidden:  
   \`delve\`, \`tapestry\`, \`nuanced\`, \`pivotal\`, \`furthermore\`, \`moreover\`, \`landscape\`, \`testament\`, \`revolutionize\`, \`game-changer\`, \`unlock\`, \`skyrocket\`, \`hence\`, \`in today's fast-paced world\`, \`it's important to note\`, \`let's explore\`, \`at its core\`, \`foster\`, \`holistic\`, \`beacon\`, \`dive into\`.  
3\. \*\*Punctuation & Cadence Normalization:\*\* No em-dashes (\`—\`) or formal semicolons (\`;\`). All such punctuation must be normalized to ellipses (\`...\`) to create an authentic, conversational pause.  
4\. \*\*No Automated Fabrication of Lived Anecdotes:\*\* Real experiential anchors (such as local Toronto, Bay Street, King Street, or Bodrum references) must be grounded in user-supplied facts. Models must never invent boardrooms, companies, or quotes.  
5\. \*\*No Direct Financial Advisory:\*\* Finance and IR pieces must provide analysis of trends and structural mechanics, never buy/sell/hold advice or promised price targets.

\---

\#\# 3\. End-to-End Automated Architecture

\`\`\`  
\[Gem / Raw Input\] (Google Doc or Audio Transcript)  
        │  
        ▼  
\[Staging Folder\] (Google Drive: 01\_Active\_Work/00\_Raw\_Inputs)  
        │  
        ├─────────────────────────────────────────────────┐  
        ▼                                                 ▼  
\[Google Apps Script Watcher\]                   \[Python Engine (CLI / API)\]  
(Watches Drive for new Docs)                   (Batch processing & local runs)  
        │                                                 │  
        └─────────────────┬───────────────────────────────┘  
                          │  
                          ▼  
            \[Multi-Stage Compliance Audit\]  
            ├── 1\. Identity Isolation Check  
            ├── 2\. Banned Lexicon Sweep  
            ├── 3\. Punctuation & Cadence Normalizer  
            ├── 4\. Experiential & Metric Claim Scan  
            └── 5\. SEO Title & Rank Math Verification  
                          │  
                          ▼  
            \[Distribution Transformation\]  
            ├── Authority Core: WordPress (Rank Math Meta, H1/H3)  
            ├── Network Multiplier: LinkedIn (300-word hook, mobile format)  
            └── Syndication Ring: Dev.to / Substack / GitHub (Canonical Tag)  
                          │  
                          ▼  
            \[Safe Publishing Gate\]  
            ├── Duplicate Content Check (WP REST API search)  
            ├── Proper UTF-8 JSON Serialization  
            └── Staged Draft Creation / Live Publication  
\`\`\`

\---

\#\# 4\. Setup & Deployment Instructions

\#\#\# Method A: Automated Google Drive Folder Watcher (Google Apps Script)  
1\. In Google Drive, create a folder named \`00\_Raw\_Inputs\` (or use your staging folder). Copy the Folder ID from the URL.  
2\. Go to \[script.google.com\](https://script.google.com/) and create a new project named \`Content\_Forge\_Watcher\`.  
3\. Paste the contents of \`Drive\_Folder\_Watcher.gs\`.  
4\. Fill in:  
   \- \`STAGING\_FOLDER\_ID\`: Your Drive folder ID.  
   \- \`WP\_SITE\_URL\`: \`https://adnanobuz.com\` (or target site).  
   \- \`WP\_USERNAME\`: Your WordPress username.  
   \- \`WP\_APP\_PASSWORD\`: Generated from WordPress Admin (\`Users\` \-\> \`Profile\` \-\> \`Application Passwords\`).  
5\. Set up a Time-driven trigger to run \`watchFolderAndProcessDrafts\` every hour or daily.  
6\. Whenever you drop a Gem-generated Google Doc into \`00\_Raw\_Inputs\`, the script audits it, normalizes punctuation, and publishes a draft directly into WordPress.

\#\#\# Method B: Python Automation Engine (\`content\_forge\_engine.py\`)  
Run the script locally or on a server:  
\`\`\`bash  
\# Run self-test  
python3 content\_forge\_engine.py \--self-test

\# Audit and transform a draft  
python3 \-c "from content\_forge\_engine import run\_pipeline; run\_pipeline('draft.txt', 'Adnan Obuz')"  
\`\`\`

\---

\#\# 5\. Failure Modes & How They Are Prevented

| Historical Failure Mode | Root Cause | Built-in Engine Remedy |  
|---|---|---|  
| \`rest\_invalid\_json\` on WordPress API | Hand-built JSON strings breaking at 7,500+ characters | Fully native UTF-8 JSON serialization via Python / Apps Script |  
| Identity cross-contamination | Model blending \*Adnan Obuz\* and \*Edward Obuz\* | Pre-publish regex hard stop that fails the pipeline if any foreign token exists |  
| Keyword cannibalization | Publishing near-duplicate posts on identical topics | Pre-publish query to \`/wp-json/wp/v2/posts?slug=...\` before submission |  
| Fabricated personal quotes | Prompt requiring anecdotes without ground truth | Claim scanner flags quotes and metrics for human verification |  
