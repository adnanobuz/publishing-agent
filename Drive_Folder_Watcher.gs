/**
 * Adnan Obuz Content Forge 2026 - Google Drive Folder Watcher & Auto-Publisher
 *
 * This Google Apps Script monitors your designated Google Drive staging folder
 * (e.g., 01_Active_Work/00_Raw_Inputs). When a new Google Doc is added or tagged,
 * it runs the compliance audit (identity isolation, banned lexicon, cadence normalization),
 * formats the SEO/Rank Math metadata, and creates a draft post on your WordPress site.
 */


// --- CONFIGURATION ---
const CONFIG = {
  // Replace with the ID of your Google Drive folder for raw inputs
  STAGING_FOLDER_ID: "PASTE_YOUR_RAW_INPUTS_FOLDER_ID_HERE",
  PROCESSED_FOLDER_ID: "PASTE_YOUR_PROCESSED_FOLDER_ID_HERE", // Optional: to move finished docs
  
  // WordPress Site Configuration
  WP_SITE_URL: "https://adnanobuz.com", // Or mrobuz.com
  WP_USERNAME: "PASTE_YOUR_WP_USERNAME_HERE",
  WP_APP_PASSWORD: "PASTE_YOUR_WP_APPLICATION_PASSWORD_HERE", // Generated from WP Users -> Application Passwords
  
  // Publishing Mode: "draft" (recommended for safe review) or "publish"
  POST_STATUS: "draft",
  
  // Primary Identities
  DEFAULT_IDENTITY: "Adnan Obuz",
  KNOWN_IDENTITIES: ["Adnan Obuz", "Edward Obuz", "Adnan Menderes Obuz"],
  BANNED_LEGACY_NAMES: ["Zane"],
  
  // AI Banned Lexicon
  BANNED_LEXICON: [
    "delve", "tapestry", "nuanced", "pivotal", "furthermore", "moreover",
    "landscape", "testament", "revolutionize", "game-changer", "unlock",
    "skyrocket", "hence", "in today's fast-paced world", "it's important to note",
    "let's explore", "at its core", "foster", "holistic", "beacon", "dive into"
  ]
};


/**
 * Main Trigger Function: Run on an hourly or daily time-driven trigger.
 */
function watchFolderAndProcessDrafts() {
  if (CONFIG.STAGING_FOLDER_ID === "PASTE_YOUR_RAW_INPUTS_FOLDER_ID_HERE") {
    Logger.log("Please configure STAGING_FOLDER_ID in script settings.");
    return;
  }


  const folder = DriveApp.getFolderById(CONFIG.STAGING_FOLDER_ID);
  const files = folder.getFilesByType(MimeType.GOOGLE_DOCS);
  
  while (files.hasNext()) {
    const file = files.next();
    const doc = DocumentApp.openById(file.getId());
    const docTitle = doc.getName();
    const bodyText = doc.getBody().getText();
    
    // Check if already processed
    if (docTitle.includes("[PROCESSED]") || docTitle.includes("[SUSPENDED]")) {
      continue;
    }
    
    Logger.log("Processing doc: " + docTitle);
    
    // Determine Target Identity from filename or default
    let targetIdentity = CONFIG.DEFAULT_IDENTITY;
    for (let id of CONFIG.KNOWN_IDENTITIES) {
      if (docTitle.toLowerCase().includes(id.toLowerCase())) {
        targetIdentity = id;
        break;
      }
    }
    
    // Run Audit & Normalization
    const auditResult = runAudit(docTitle, bodyText, targetIdentity);
    if (!auditResult.passed) {
      Logger.log("Audit failed for " + docTitle + ": " + JSON.stringify(auditResult.errors));
      doc.setName("[SUSPENDED] " + docTitle);
      doc.getBody().insertParagraph(0, "⚠️ FORGE AUDIT FAILED:\n" + auditResult.errors.join("\n") + "\n----------------------------------\n");
      continue;
    }
    
    // Normalize Punctuation
    const cleanContent = normalizePunctuation(bodyText);
    
    // Publish to WordPress
    const publishResult = publishToWordPress(docTitle.replace("[READY]", "").trim(), cleanContent, targetIdentity);
    
    if (publishResult.success) {
      Logger.log("Successfully created post. ID: " + publishResult.id + " Link: " + publishResult.link);
      doc.setName("[PROCESSED] " + docTitle);
      doc.getBody().insertParagraph(0, "✓ PUBLISHED TO WORDPRESS (" + CONFIG.POST_STATUS + "):\nURL: " + publishResult.link + "\n----------------------------------\n");
    } else {
      Logger.log("Publish failed: " + publishResult.error);
    }
  }
}


/**
 * Compliance Audit Engine
 */
function runAudit(title, text, targetIdentity) {
  const fullText = title + "\n" + text;
  const errors = [];
  
  // 1. Identity isolation
  for (let otherId of CONFIG.KNOWN_IDENTITIES) {
    if (otherId !== targetIdentity) {
      const regex = new RegExp(otherId, "gi");
      if (regex.test(fullText)) {
        errors.push("Forbidden cross-identity detected: " + otherId);
      }
    }
  }
  for (let banned of CONFIG.BANNED_LEGACY_NAMES) {
    const regex = new RegExp("\\b" + banned + "\\b", "gi");
    if (regex.test(fullText)) {
      errors.push("Banned legacy name detected: " + banned);
    }
  }
  
  // 2. Banned lexicon check
  for (let word of CONFIG.BANNED_LEXICON) {
    const regex = new RegExp("\\b" + word + "\\b", "gi");
    if (regex.test(fullText)) {
      errors.push("Banned AI-sounding phrase found: '" + word + "'");
    }
  }
  
  return {
    passed: errors.length === 0,
    errors: errors
  };
}


/**
 * Normalizes em-dashes and formal semicolons into ellipses.
 */
function normalizePunctuation(text) {
  let clean = text.replace(/\s*[—–]\s*|\s*--\s*/g, " ... ");
  clean = clean.replace(/;\s*/g, " ... ");
  return clean;
}


/**
 * WordPress REST API Publisher
 */
function publishToWordPress(title, content, targetIdentity) {
  const url = CONFIG.WP_SITE_URL.replace(/\/$/, "") + "/wp-json/wp/v2/posts";
  const authString = Utilities.base64Encode(CONFIG.WP_USERNAME + ":" + CONFIG.WP_APP_PASSWORD);
  
  const payload = {
    title: title,
    content: content,
    status: CONFIG.POST_STATUS,
    meta: {
      rank_math_title: title,
      rank_math_description: "Strategic analysis and executive commentary by " + targetIdentity + ".",
      rank_math_focus_keyword: targetIdentity
    }
  };
  
  const options = {
    method: "post",
    contentType: "application/json; charset=utf-8",
    headers: {
      "Authorization": "Basic " + authString
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };
  
  try {
    const response = UrlFetchApp.fetch(url, options);
    const code = response.getResponseCode();
    const data = JSON.parse(response.getContentText());
    
    if (code >= 200 && code < 300) {
      return { success: true, id: data.id, link: data.link };
    } else {
      return { success: false, error: "HTTP " + code + ": " + (data.message || response.getContentText()) };
    }
  } catch (e) {
    return { success: false, error: e.toString() };
  }
}