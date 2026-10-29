# Hebrew translation (Track F3)

Catalog: `packages/lib/translations/he/web.po` (lingui, PO format, `Plural-Forms: nplurals=2; plural=(n != 1);`).

## Coverage (v2.21.1-vs1)

| Scope | Translated | Total | % |
|---|---|---|---|
| Client-facing (signing pages, emails, certificate/audit PDF, shared components on those pages) | 836 | 836 | 100 % |
| Whole catalog (incl. admin/authenticated UI) | 3411 | 3411 | 100 % |

Validator: `python3 vs/tools/check_po.py packages/lib/translations/he/web.po --scope` → 0 errors
(same placeholders, JSX tags, ICU plural/select heads and `#` as the msgid; balanced braces; no vendor name).

"Client-facing" is defined by source path in `vs/tools/scope.py` (`_recipient+`, `_share+`, `document-signing/`,
`envelope-signing/`, `direct-template/`, `pdf-viewer/`, `sign-field-*` dialogs, non-authoring `embed/`,
`[__htmltopdf]` certificate/audit routes, the signature disclosure, `packages/email`, email job handlers,
`server-only/pdf`, audit-log formatting, recipient roles, signature pad, field rendering, dialog/sheet primitives,
the source-code footer).

## How the catalog is built and how fallback works

- The Docker build (`apps/remix/.bin/build.sh`) runs `npm run translate` = `lingui extract --clean` + `lingui compile`.
  Extract re-syncs every catalog with the source; msgids we translated are kept, new msgids arrive with an empty msgstr.
- `lingui.config.ts` has `sourceLocale: 'en'` and no `fallbackLocales`. In `@lingui/cli` 5.x
  (`getTranslationsForCatalog`) an empty msgstr falls back to the **source-locale (en) translation**, then the source
  message, and only as a last resort to the id. So untranslated strings render in English, never empty and never as a hash.
- Upgrades: rebase, then regenerate `he/web.po` from `en/web.po` (msgids only), translate the delta, run the validator.

## Translation conventions

- Formal, polite Israeli business Hebrew; the user is addressed in the plural ("לחצו", "הוזמנתם") or impersonally
  ("יש ל…", "נא ל…"). Third-person actors are rendered in the passive ("המסמך נחתם על ידי {user}") to stay gender-neutral.
- Recipient-role **action verbs** (`msgctxt "Recipient role action verb"`) are only interpolated into sentences
  ("has invited you to {action} the document …", "Please {action} your document"). They are therefore translated as
  full infinitive phrases that already contain the object: Sign → "לחתום על המסמך", Approve → "לאשר את המסמך",
  View → "לצפות במסמך", CC → "לקבל עותק של המסמך", Assist → "לסייע במילוי המסמך"; the host sentences drop
  "the document". Same for `Recipient role actioned` (used only in the direct-template email).
- "Documenso" never appears in Hebrew; it is replaced by "VoIPe" or by neutral wording.
- Email is written דוא״ל (gershayim U+05F4).
- The English fallback catalog (`en/web.po`) carries neutral msgstr overrides for 23 client-facing msgids that named the
  vendor (see `BRANDING.md`); msgids are unchanged, so `lingui extract` keeps the overrides.
- The admin/authenticated UI (2575 strings) was drafted in four parallel batches with the same glossary and validated
  with the same script; it has had less review than the client-facing scope.

## Items for Nir's review (legal / wording decisions)

- The signature disclosure page (`/articles/signature-disclosure`) is a faithful translation of the upstream US text,
  including the reference to the US E-Sign Act (row "When you use our platform…"). VoIPe may want an Israeli
  wording (חוק חתימה אלקטרונית, התשס״א-2001) — that is a legal decision, not a translation one.
- The consent text under the signature ("By proceeding with your electronic signature…") — legal wording.
- Typed delete confirmations in the admin UI ask for the Hebrew phrase (e.g. "מחיקת {0}"), because the check
  compares against the same translated string.

## Which language a signer sees (upstream behaviour, not changed)

- **Signing pages:** the UI locale comes from the `lang` cookie, else the browser's `Accept-Language` (first entry,
  e.g. `he-IL` → `he`). It does **not** follow the document's `meta.language`. A client whose phone/browser is set to
  English sees the English signing UI (with RTL off). Making the signing page follow the document language would be a
  functional change (DB lookup in the root loader); left as a decision for VoIPe.
- **Emails, certificate and audit log:** rendered in the document's `meta.language` (`he` → Hebrew, RTL).

## What must be verified visually (cannot be run on the build host)

- **QA-21 (RTL, iOS Safari + Android Chrome):** `<html dir="rtl" lang="he">` on `/sign/<token>`; signer header,
  sidebar/widget, dialogs (signature pad, text/number/email/name dialogs, reject dialog, complete dialog) laid out
  right-to-left; back/next arrows mirrored; email inputs and the 2FA/PIN code input stay LTR; the PDF pages and the field
  overlays are not mirrored and fields sit exactly on their boxes (`dir="ltr"` on `[data-pdf-content]` and on the field
  portal); progress bar fills from the right; "קוד מקור" footer visible and links to the repo; no horizontal scroll.
- **QA-07/25 (emails, Gmail + Outlook):** with `meta.language = "he"` the invite/reminder/completed/rejected emails are
  Hebrew and right-aligned (`dir="rtl"` on `<html>`, `<body>` and the body table cell); check Outlook desktop (Word
  engine) alignment; buttons centred; no vendor name (with the `BRANDING.md` §1 configuration). Check the subject
  line wording, e.g. "הוזמנתם על ידי VoIPe לחתום על המסמך".
- **QA-09/11 (sealed PDF):**
  1. Certificate and audit-log pages are in Hebrew and contain no tofu boxes (Noto Sans Hebrew registered from
     `public/fonts/noto-sans-hebrew.ttf`; Konva font list `Inter, "Noto Sans Hebrew"`; skia-canvas falls back per glyph).
  2. Hebrew labels read correctly right-to-left, including mixed strings ("כתובת IP", "קוד 2FA", "מזהה מעטפה: <id>"):
     labels/titles/event descriptions are drawn with an RTL base direction (`Konva.Text direction: 'rtl'`).
  3. On the certificate, each "label: value" pair is mirrored (label at the right edge, value right-aligned to its left).
     The **table column order is not mirrored** (Signer events | Signature | Details stay left-to-right); accept or
     raise as follow-up.
  4. Hebrew signer names (column 1, audit log) and a typed Hebrew signature render in the right order (the signature
     font chain now includes "Noto Sans Hebrew"; inserted NAME/TEXT fields use the same chain).
  5. `pdftotext -layout` shows Hebrew in logical order (QA-09 text check). If it shows reversed words, the PDF text is
     still correct visually; record the pdftotext result and the visual check separately.
  6. Dates stay `yyyy-MM-dd hh:mm:ss a (ZZZZ)` (upstream fixed format), IPs/emails/ids LTR.

## Client-facing strings for review

| # | msgid | Hebrew | context |
|---|---|---|---|
| 1 | "{0}" will appear on the document as it has a timezone of "{1}". | "{0}" יופיע במסמך, משום שאזור הזמן שלו הוא "{1}". | apps/remix/app/components/general/document-signing/document-signing-date-field.tsx |
| 2 | "{documentName}" has been deleted by an admin. | המסמך "{documentName}" נמחק על ידי מנהל מערכת. | packages/email/template-components/template-document-super-delete.tsx |
| 3 | “{documentName}” has been signed | המסמך „{documentName}” נחתם | packages/email/template-components/template-document-pending.tsx |
| 4 | “{documentName}” was signed by all signers | המסמך „{documentName}” נחתם על ידי כל החותמים | packages/email/template-components/template-document-completed.tsx |
| 5 | (You) | (אני) | apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/general/document-signing/document-signing-form.tsx, apps/remix/app/components/general/envelope-signing/envelope-signer-form.tsx |
| 6 | {0, plural, one {(1 character over)} other {(# characters over)}} | {0, plural, one {(חריגה של תו אחד)} other {(חריגה של # תווים)}} | apps/remix/app/components/general/document-signing/document-signing-text-field.tsx |
| 7 | {0, plural, one {# character remaining} other {# characters remaining}} | {0, plural, one {נותר תו אחד} other {נותרו # תווים}} | apps/remix/app/components/dialogs/sign-field-text-dialog.tsx |
| 8 | {0, plural, one {# field} other {# fields}} | {0, plural, one {שדה אחד} other {# שדות}} | apps/remix/app/components/general/envelope-signing/envelope-signer-form.tsx |
| 9 | {0, plural, one {# recipient} other {# recipients}} | {0, plural, one {נמען אחד} other {# נמענים}} | apps/remix/app/routes/_recipient+/d.$token+/_index.tsx |
| 10 | {0, plural, one {1 Field Remaining} other {# Fields Remaining}} | {0, plural, one {נותר שדה אחד} other {נותרו # שדות}} | apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx, apps/remix/app/components/general/envelope-signing/envelope-signer-header.tsx |
| 11 | {0, plural, one {1 Field} other {# Fields}} | {0, plural, one {שדה אחד} other {# שדות}} | apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx |
| 12 | {0, plural, one {1 matching field} other {# matching fields}} | {0, plural, one {שדה תואם אחד} other {# שדות תואמים}} | apps/remix/app/components/general/document-signing/document-signing-auto-sign.tsx |
| 13 | {0} | {0} | apps/remix/app/components/general/document-signing/document-signing-auto-sign.tsx |
| 14 | {0} has invited you to {recipientActionVerb} the document "{1}". | הוזמנתם על ידי {0} {recipientActionVerb} "{1}". | packages/lib/jobs/definitions/emails/send-signing-email.handler.ts, packages/lib/server-only/document/resend-document.ts |
| 15 | {0} invited you to {recipientActionVerb} a document | הוזמנתם על ידי {0} {recipientActionVerb} | packages/lib/jobs/definitions/emails/send-signing-email.handler.ts |
| 16 | {browserInfo} on {os} | {browserInfo} ב-{os} | packages/lib/server-only/pdf/render-audit-logs.ts |
| 17 | {charactersRemaining, plural, one {1 character remaining} other {{charactersRemaining} characters remaining}} | {charactersRemaining, plural, one {נותר תו אחד} other {נותרו {charactersRemaining} תווים}} | apps/remix/app/components/general/document-signing/document-signing-text-field.tsx |
| 18 | {expiresInMinutes, plural, one {This code will expire in # minute.} other {This code will expire in # minutes.}} | {expiresInMinutes, plural, one {תוקף הקוד יפוג בעוד דקה אחת.} other {תוקף הקוד יפוג בעוד # דקות.}} | packages/email/template-components/template-access-auth-2fa.tsx |
| 19 | {inviterName} &lt;0&gt;({inviterEmail})&lt;/0&gt; | {inviterName} &lt;0&gt;({inviterEmail})&lt;/0&gt; | packages/email/templates/document-invite.tsx |
| 20 | {inviterName} has cancelled the document {documentName}, you don't need to sign it anymore. | המסמך {documentName} בוטל על ידי {inviterName}, ואין עוד צורך לחתום עליו. | packages/email/templates/document-cancel.tsx |
| 21 | {inviterName} has cancelled the document&lt;0/&gt;"{documentName}" | המסמך בוטל על ידי {inviterName}&lt;0/&gt;"{documentName}" | packages/email/template-components/template-document-cancel.tsx |
| 22 | {inviterName} has invited you to {0}&lt;0/&gt;"{documentName}" | הוזמנתם על ידי {inviterName} {0}&lt;0/&gt;"{documentName}" | packages/email/template-components/template-document-invite.tsx |
| 23 | {inviterName} has invited you to {action} {documentName} | הוזמנתם על ידי {inviterName} {action} {documentName} | packages/email/templates/document-invite.tsx |
| 24 | {inviterName} has invited you to {action} the document "{documentName}". | הוזמנתם על ידי {inviterName} {action} "{documentName}". | packages/email/templates/document-invite.tsx |
| 25 | {inviterName} has removed you from the document {documentName}. | הוסרתם מהמסמך {documentName} על ידי {inviterName}. | packages/email/templates/recipient-removed-from-document.tsx |
| 26 | {inviterName} has removed you from the document&lt;0/&gt;"{documentName}" | הוסרתם על ידי {inviterName} מהמסמך&lt;0/&gt;"{documentName}" | packages/email/templates/recipient-removed-from-document.tsx |
| 27 | {inviterName} on behalf of "{0}" has invited you to {recipientActionVerb} the document "{1}". | הוזמנתם על ידי {inviterName} בשם "{0}" {recipientActionVerb} "{1}". | packages/lib/jobs/definitions/emails/send-signing-email.handler.ts, packages/lib/server-only/document/resend-document.ts |
| 28 | {inviterName} on behalf of "{teamName}" has invited you to {0}&lt;0/&gt;"{documentName}" | הוזמנתם על ידי {inviterName} בשם "{teamName}" {0}&lt;0/&gt;"{documentName}" | packages/email/template-components/template-document-invite.tsx |
| 29 | {inviterName} on behalf of "{teamName}" has invited you to {action} {documentName} | הוזמנתם על ידי {inviterName} בשם "{teamName}" {action} {documentName} | packages/email/templates/document-invite.tsx |
| 30 | {recipientActionVerb} document | {recipientActionVerb} | apps/remix/app/components/general/direct-template/direct-template-page.tsx |
| 31 | {recipientActionVerb} the document to complete the process. | יש {recipientActionVerb} כדי להשלים את התהליך. | apps/remix/app/components/general/direct-template/direct-template-page.tsx |
| 32 | {recipientCount} recipients | {recipientCount} נמענים | apps/remix/app/components/general/document/document-certificate-qr-view.tsx, apps/remix/app/components/general/document/document-certificate-qr-view.tsx |
| 33 | {recipientLabel} has been removed from the document "{documentName}" by an administrator, typically at the request of the document sender. | הנמען {recipientLabel} הוסר מהמסמך "{documentName}" על ידי מנהל מערכת, בדרך כלל לבקשת שולח המסמך. | packages/email/template-components/template-recipient-removed-by-admin.tsx |
| 34 | {recipientName} {action} a document by using one of your direct links | {recipientName} {action} באמצעות אחד הקישורים הישירים שלכם | packages/email/templates/document-created-from-direct-template.tsx |
| 35 | {recipientName} has been removed from the document "{documentName}" by an administrator. | הנמען {recipientName} הוסר מהמסמך "{documentName}" על ידי מנהל מערכת. | packages/email/templates/recipient-removed-by-admin.tsx |
| 36 | {recipientName} has rejected the document '{documentName}' | המסמך '{documentName}' נדחה על ידי {recipientName} | packages/email/templates/document-rejected.tsx |
| 37 | {recipientReference} has completed signing the document. | החתימה של {recipientReference} על המסמך הושלמה. | packages/email/template-components/template-document-recipient-signed.tsx |
| 38 | {recipientReference} has signed "{0}" | "{0}" נחתם על ידי {recipientReference} | packages/lib/jobs/definitions/emails/send-recipient-signed-email.handler.ts |
| 39 | {recipientReference} has signed "{documentName}" | "{documentName}" נחתם על ידי {recipientReference} | packages/email/template-components/template-document-recipient-signed.tsx |
| 40 | {recipientReference} has signed {documentName} | {documentName} נחתם על ידי {recipientReference} | packages/email/templates/document-recipient-signed.tsx |
| 41 | {signerName} has rejected the document "{documentName}". | המסמך "{documentName}" נדחה על ידי {signerName}. | packages/email/template-components/template-document-rejected.tsx |
| 42 | {teamName} has invited you to {0}&lt;0/&gt;"{documentName}" | הוזמנתם על ידי {teamName} {0}&lt;0/&gt;"{documentName}" | packages/email/template-components/template-document-invite.tsx |
| 43 | {teamName} has invited you to {action} {documentName} | הוזמנתם על ידי {teamName} {action} {documentName} | packages/email/templates/document-invite.tsx |
| 44 | {user} added a field | שדה נוסף על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 45 | {user} added a recipient | נמען נוסף על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 46 | {user} approved the document | המסמך אושר על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 47 | {user} authenticated with the signing provider | בוצע אימות מול ספק החתימה על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 48 | {user} authorised the remote signature | החתימה המרוחקת אושרה על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 49 | {user} cancelled the document | המסמך בוטל על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 50 | {user} CC'd the document | עותק של המסמך נמסר אל {user} | packages/lib/utils/document-audit-logs.ts |
| 51 | {user} completed their task | המשימה הושלמה על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 52 | {user} created an envelope item with title {0} | פריט מעטפה בשם {0} נוצר על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 53 | {user} created the document | המסמך נוצר על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 54 | {user} deleted an envelope item with title {0} | פריט מעטפה בשם {0} נמחק על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 55 | {user} deleted the document | המסמך נמחק על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 56 | {user} failed to validate a 2FA token for the document | אימות קוד 2FA למסמך נכשל עבור {user} | packages/lib/utils/document-audit-logs.ts |
| 57 | {user} moved the document to team | המסמך הועבר לצוות על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 58 | {user} opened the document | המסמך נפתח על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 59 | {user} prefilled a field | שדה מולא מראש על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 60 | {user} rejected the document | המסמך נדחה על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 61 | {user} removed a field | שדה הוסר על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 62 | {user} removed a recipient | נמען הוסר על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 63 | {user} removed a recipient as an administrator | נמען הוסר על ידי {user} בהרשאת מנהל מערכת | packages/lib/utils/document-audit-logs.ts |
| 64 | {user} replaced the PDF for envelope item {0} | קובץ ה-PDF של פריט המעטפה {0} הוחלף על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 65 | {user} requested a 2FA token for the document | קוד 2FA למסמך התבקש על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 66 | {user} requested a remote signature | חתימה מרוחקת התבקשה על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 67 | {user} resent an email to {0} | דוא״ל נשלח שוב אל {0} על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 68 | {user} sent an email to {0} | דוא״ל נשלח אל {0} על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 69 | {user} sent the document | המסמך נשלח על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 70 | {user} signed a field | שדה נחתם על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 71 | {user} signed the document | המסמך נחתם על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 72 | {user} unsigned a field | חתימת שדה בוטלה על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 73 | {user} updated a field | שדה עודכן על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 74 | {user} updated a recipient | נמען עודכן על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 75 | {user} updated an envelope item | פריט מעטפה עודכן על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 76 | {user} updated the document | המסמך עודכן על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 77 | {user} updated the document access auth requirements | דרישות האימות לגישה למסמך עודכנו על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 78 | {user} updated the document external ID | המזהה החיצוני של המסמך עודכן על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 79 | {user} updated the document signing auth requirements | דרישות האימות לחתימה על המסמך עודכנו על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 80 | {user} updated the document title | כותרת המסמך עודכנה על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 81 | {user} updated the document visibility | נראות המסמך עודכנה על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 82 | {user} validated a 2FA token for the document | קוד 2FA למסמך אומת על ידי {user} | packages/lib/utils/document-audit-logs.ts |
| 83 | {user} viewed the document | המסמך נצפה על ידי {user} | packages/lib/utils/document-audit-logs.ts, packages/lib/utils/document-audit-logs.ts |
| 84 | {user}'s remote signature was applied | החתימה המרוחקת של {user} הוחלה | packages/lib/utils/document-audit-logs.ts |
| 85 | {user}'s signing provider authentication failed | האימות של {user} מול ספק החתימה נכשל | packages/lib/utils/document-audit-logs.ts |
| 86 | {userAgent} | {userAgent} | packages/lib/server-only/pdf/render-audit-logs.ts |
| 87 | {validationLength, plural, one {Select at least # option} other {Select at least # options}} | {validationLength, plural, one {יש לבחור לפחות אפשרות אחת} other {יש לבחור לפחות # אפשרויות}} | apps/remix/app/components/dialogs/sign-field-checkbox-dialog.tsx |
| 88 | {validationLength, plural, one {Select at most # option} other {Select at most # options}} | {validationLength, plural, one {יש לבחור לכל היותר אפשרות אחת} other {יש לבחור לכל היותר # אפשרויות}} | apps/remix/app/components/dialogs/sign-field-checkbox-dialog.tsx |
| 89 | {validationLength, plural, one {Select exactly # option} other {Select exactly # options}} | {validationLength, plural, one {יש לבחור בדיוק אפשרות אחת} other {יש לבחור בדיוק # אפשרויות}} | apps/remix/app/components/dialogs/sign-field-checkbox-dialog.tsx |
| 90 | &lt;0&gt;"{0}"&lt;/0&gt; is no longer available to sign | &lt;0&gt;"{0}"&lt;/0&gt; אינו זמין עוד לחתימה | apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx, apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx |
| 91 | &lt;0&gt;{organisationName}&lt;/0&gt; has requested to create an account on your behalf. | &lt;0&gt;{organisationName}&lt;/0&gt; ביקש ליצור עבורכם חשבון. | packages/email/templates/organisation-account-link-confirmation.tsx |
| 92 | &lt;0&gt;{organisationName}&lt;/0&gt; has requested to link your current Documenso account to their organisation. | &lt;0&gt;{organisationName}&lt;/0&gt; ביקש לקשר את החשבון הנוכחי שלכם לארגון. | packages/email/templates/organisation-account-link-confirmation.tsx |
| 93 | &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; has invited you to approve this document | הוזמנתם על ידי &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; לאשר מסמך זה | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 94 | &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; has invited you to assist this document | הוזמנתם על ידי &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; לסייע במסמך זה | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 95 | &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; has invited you to sign this document | הוזמנתם על ידי &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; לחתום על מסמך זה | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 96 | &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; has invited you to view this document | הוזמנתם על ידי &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; לצפות במסמך זה | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 97 | &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; on behalf of "{0}" has invited you to approve this document | הוזמנתם על ידי &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; בשם "{0}" לאשר מסמך זה | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 98 | &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; on behalf of "{0}" has invited you to assist this document | הוזמנתם על ידי &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; בשם "{0}" לסייע במסמך זה | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 99 | &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; on behalf of "{0}" has invited you to sign this document | הוזמנתם על ידי &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; בשם "{0}" לחתום על מסמך זה | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 100 | &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; on behalf of "{0}" has invited you to view this document | הוזמנתם על ידי &lt;0&gt;{senderName} {senderEmail}&lt;/0&gt; בשם "{0}" לצפות במסמך זה | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 101 | &lt;0&gt;{teamName}&lt;/0&gt; has requested to use your email address for their team on Documenso. | &lt;0&gt;{teamName}&lt;/0&gt; ביקש להשתמש בכתובת הדוא״ל שלכם עבור הצוות שלו. | packages/email/templates/confirm-team-email.tsx |
| 102 | 2FA | 2FA | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx |
| 103 | 2FA token | קוד 2FA | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 104 | 404 not found | 404 – הדף לא נמצא | apps/remix/app/components/general/generic-error-layout.tsx |
| 105 | 500 Internal Server Error | 500 – שגיאת שרת פנימית | apps/remix/app/components/general/generic-error-layout.tsx |
| 106 | A device capable of accessing, opening, and reading documents | מכשיר המאפשר גישה למסמכים, פתיחתם וקריאתם | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 107 | A document was created by your direct template that requires you to {recipientActionVerb} it. | נוצר מסמך באמצעות התבנית הישירה שלכם, ויש {recipientActionVerb}. | packages/lib/jobs/definitions/emails/send-signing-email.handler.ts |
| 108 | A field was added | נוסף שדה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 109 | A field was removed | הוסר שדה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 110 | A field was updated | עודכן שדה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 111 | A means to print or download documents for your records | אמצעי להדפסה או להורדה של מסמכים לשמירה | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 112 | A member has joined your organisation on Documenso | חבר חדש הצטרף לארגון שלכם | packages/email/templates/organisation-join.tsx |
| 113 | A member has left your organisation | חבר עזב את הארגון שלכם | packages/lib/jobs/definitions/emails/send-organisation-member-left-email.handler.ts |
| 114 | A member has left your organisation {organisationName} | חבר עזב את הארגון שלכם {organisationName} | packages/email/templates/organisation-leave.tsx |
| 115 | A member has left your organisation on Documenso | חבר עזב את הארגון שלכם | packages/email/templates/organisation-leave.tsx |
| 116 | A new member has joined your organisation | חבר חדש הצטרף לארגון שלכם | packages/lib/jobs/definitions/emails/send-organisation-member-joined-email.handler.ts |
| 117 | A new member has joined your organisation {organisationName} | חבר חדש הצטרף לארגון שלכם {organisationName} | packages/email/templates/organisation-join.tsx |
| 118 | A recipient has been removed from your document | נמען הוסר מהמסמך שלכם | packages/email/template-components/template-recipient-removed-by-admin.tsx, packages/lib/jobs/definitions/emails/send-admin-recipient-removed-emails.handler.ts |
| 119 | A recipient was added | נוסף נמען | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 120 | A recipient was removed | הוסר נמען | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 121 | A recipient was removed by an administrator | נמען הוסר על ידי מנהל מערכת | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 122 | A recipient was updated | עודכן נמען | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 123 | A request has been made to create an account for you | התקבלה בקשה ליצור עבורכם חשבון | packages/email/templates/organisation-account-link-confirmation.tsx |
| 124 | A request has been made to link your Documenso account | התקבלה בקשה לקשר את החשבון שלכם | packages/email/templates/organisation-account-link-confirmation.tsx |
| 125 | A stable internet connection | חיבור יציב לאינטרנט | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 126 | A team you were a part of has been deleted | צוות שהייתם חברים בו נמחק | packages/email/templates/team-delete.tsx, packages/email/templates/team-delete.tsx |
| 127 | A valid email is required | נדרשת כתובת דוא״ל תקינה | apps/remix/app/components/embed/embed-direct-template-client-page.tsx |
| 128 | Accept | אישור | packages/email/templates/confirm-team-email.tsx, packages/email/templates/organisation-invite.tsx |
| 129 | Accept invitation to join an organisation on Documenso | הזמנה להצטרף לארגון | packages/email/templates/organisation-invite.tsx |
| 130 | Accept team email request for {teamName} on Documenso | אישור בקשה לשימוש בכתובת דוא״ל עבור הצוות {teamName} | packages/email/templates/confirm-team-email.tsx |
| 131 | Acceptance and Consent | הסכמה ואישור | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 132 | Account | חשבון | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx |
| 133 | Account Authentication | אימות חשבון | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/generate-certificate-pdf.ts |
| 134 | Account creation request | בקשה ליצירת חשבון | packages/email/templates/organisation-account-link-confirmation.tsx |
| 135 | Account Re-Authentication | אימות חוזר של החשבון | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/generate-certificate-pdf.ts |
| 136 | Acknowledgment | אישור קריאה | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 137 | Actions | פעולות | apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx, apps/remix/app/components/general/envelope-signing/envelope-signer-header.tsx |
| 138 | After signing a document electronically, you will be provided the opportunity to view, download, and print the document for your records. It is highly recommended that you retain a copy of all electronically signed documents for your personal records. We will also retain a copy of the signed document for our records however we may not be able to provide you with a copy of the signed document after a certain period of time. | לאחר החתימה האלקטרונית על מסמך, תינתן לכם האפשרות לצפות במסמך, להוריד אותו ולהדפיס אותו לשמירה. מומלץ מאוד לשמור עותק של כל המסמכים החתומים אלקטרונית לתיעוד האישי שלכם. גם אנו נשמור עותק של המסמך החתום לתיעוד שלנו, אולם ייתכן שלא נוכל לספק לכם עותק של המסמך החתום לאחר פרק זמן מסוים. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 139 | All documents have been completed! | כל המסמכים הושלמו! | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 140 | All documents related to the electronic signing process will be provided to you electronically through our platform or via email. It is your responsibility to ensure that your email address is current and that you can receive and open our emails. | כל המסמכים הנוגעים לתהליך החתימה האלקטרונית יסופקו לכם באופן אלקטרוני באמצעות הפלטפורמה שלנו או בדוא״ל. באחריותכם לוודא שכתובת הדוא״ל שלכם מעודכנת ושבאפשרותכם לקבל ולפתוח את הודעות הדוא״ל שלנו. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 141 | All recipients have signed. The document is being processed and you will receive an email copy shortly. | כל הנמענים חתמו. המסמך נמצא בעיבוד, ועותק שלו יישלח אליכם בדוא״ל בקרוב. | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 142 | All signatures have been voided. | כל החתימות בוטלו. | packages/email/template-components/template-document-cancel.tsx |
| 143 | Allow document recipients to reply directly to this email address | אפשרו לנמעני המסמכים להשיב ישירות לכתובת דוא״ל זו | packages/email/templates/confirm-team-email.tsx |
| 144 | Almost there | כמעט סיימנו | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 145 | An account was automatically disabled | חשבון הושבת באופן אוטומטי | packages/lib/jobs/definitions/emails/send-account-disabled-email.handler.ts |
| 146 | An admin has deleted your document "{documentName}". | המסמך שלכם "{documentName}" נמחק על ידי מנהל מערכת. | packages/email/templates/document-super-delete.tsx |
| 147 | An administrator has created a Documenso account for you. | מנהל מערכת יצר עבורכם חשבון. | packages/email/template-components/template-admin-user-created.tsx |
| 148 | An electronic signature provided by you on our platform, achieved through clicking through to a document and entering your name, or any other electronic signing method we provide, is legally binding. It carries the same weight and enforceability as a manual signature written with ink on paper. | חתימה אלקטרונית שלכם בפלטפורמה שלנו, שבוצעה באמצעות מעבר למסמך והזנת שמכם או בכל אמצעי חתימה אלקטרוני אחר שאנו מספקים, מחייבת משפטית. יש לה תוקף ואכיפוּת זהים לאלה של חתימה ידנית בדיו על גבי נייר. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 149 | An email account | חשבון דוא״ל | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 150 | An error occurred | אירעה שגיאה | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx, apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 151 | An error occurred while auto-signing the document, some fields may not be signed. Please review and manually sign any remaining fields. | אירעה שגיאה בחתימה האוטומטית על המסמך, וייתכן שחלק מהשדות לא נחתמו. נא לבדוק ולחתום ידנית על השדות שנותרו. | apps/remix/app/components/general/document-signing/document-signing-auto-sign.tsx |
| 152 | An error occurred while loading the document. | אירעה שגיאה בטעינת המסמך. | apps/remix/app/components/general/pdf-viewer/pdf-viewer.tsx |
| 153 | An error occurred while rejecting the document. Please try again. | אירעה שגיאה בדחיית המסמך. נא לנסות שוב. | apps/remix/app/components/general/document-signing/document-signing-reject-dialog.tsx |
| 154 | An error occurred while removing the field. | אירעה שגיאה בהסרת השדה. | apps/remix/app/components/general/document-signing/document-signing-checkbox-field.tsx, apps/remix/app/components/general/document-signing/document-signing-date-field.tsx, apps/remix/app/components/general/document-signing/document-signing-dropdown-field.tsx (+5) |
| 155 | An error occurred while removing the selection. | אירעה שגיאה בהסרת הבחירה. | apps/remix/app/components/general/document-signing/document-signing-radio-field.tsx |
| 156 | An error occurred while removing the signature. | אירעה שגיאה בהסרת החתימה. | apps/remix/app/components/general/document-signing/document-signing-signature-field.tsx |
| 157 | An error occurred while signing as assistant. | אירעה שגיאה בחתימה כעוזר. | apps/remix/app/components/general/document-signing/document-signing-checkbox-field.tsx, apps/remix/app/components/general/document-signing/document-signing-date-field.tsx, apps/remix/app/components/general/document-signing/document-signing-dropdown-field.tsx (+6) |
| 158 | An error occurred while signing the document. | אירעה שגיאה בחתימה על המסמך. | apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx, apps/remix/app/components/general/document-signing/document-signing-checkbox-field.tsx, apps/remix/app/components/general/document-signing/document-signing-date-field.tsx (+8) |
| 159 | An error occurred while signing the field. | אירעה שגיאה בחתימה על השדה. | apps/remix/app/components/general/envelope-signing/envelope-signer-page-renderer.tsx |
| 160 | An error occurred while updating the signature. | אירעה שגיאה בעדכון החתימה. | apps/remix/app/components/general/document-signing/document-signing-checkbox-field.tsx |
| 161 | An organisation has exceeded their fair use limits | ארגון חרג ממגבלות השימוש ההוגן | packages/lib/jobs/definitions/emails/send-organisation-limit-alert-email.handler.ts |
| 162 | An organisation is nearing their fair use limits | ארגון מתקרב למגבלות השימוש ההוגן | packages/lib/jobs/definitions/emails/send-organisation-limit-alert-email.handler.ts |
| 163 | An unexpected error occurred. | אירעה שגיאה בלתי צפויה. | apps/remix/app/components/general/generic-error-layout.tsx |
| 164 | Applying your signature | החתימה שלכם מוחלת | apps/remix/app/components/general/document-signing/csc-recipient-signing-in-progress-page.tsx |
| 165 | Applying your signature... | החתימה שלכם מוחלת... | apps/remix/app/components/general/envelope-signing/envelope-signing-csc-status.tsx |
| 166 | Approaching Your Plan Limits | מתקרבים למגבלות התוכנית | packages/email/templates/organisation-limit-alert.tsx, packages/email/templates/organisation-limit-alert.tsx, packages/lib/jobs/definitions/emails/send-organisation-limit-alert-email.handler.ts |
| 167 | Approve | אישור | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 168 | Approve | לאשר את המסמך | [Recipient role action verb] packages/lib/constants/recipient-roles.ts |
| 169 | Approve Document | אישור המסמך | apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx (+1) |
| 170 | Approved | אישר/ה את המסמך | [Recipient role actioned] packages/lib/constants/recipient-roles.ts |
| 171 | Approver | מאשר | apps/remix/app/components/general/envelope-signing/envelope-signer-header.tsx |
| 172 | Approver | מאשר | [Recipient role name] packages/lib/constants/recipient-roles.ts |
| 173 | Approvers | מאשרים | [Recipient role plural name] packages/lib/constants/recipient-roles.ts |
| 174 | Approving | מאשר | [Recipient role progressive verb] packages/lib/constants/recipient-roles.ts |
| 175 | Are you sure you want to reject this document? This action cannot be undone. | האם לדחות את המסמך? לא ניתן לבטל פעולה זו. | apps/remix/app/components/general/document-signing/document-signing-reject-dialog.tsx |
| 176 | Are you sure? | האם להמשיך? | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 177 | Assist | לסייע במילוי המסמך | [Recipient role action verb] packages/lib/constants/recipient-roles.ts |
| 178 | Assist Document | סיוע במסמך | apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx (+1) |
| 179 | Assist with signing | סיוע בחתימה | apps/remix/app/components/embed/embed-document-signing-page-v1.tsx |
| 180 | Assistant | עוזר | apps/remix/app/components/general/envelope-signing/envelope-signer-header.tsx |
| 181 | Assistant | עוזר | [Recipient role name] packages/lib/constants/recipient-roles.ts |
| 182 | Assistants | עוזרים | [Recipient role plural name] packages/lib/constants/recipient-roles.ts |
| 183 | Assistants and Copy roles are currently not compatible with the multi-sign experience. | תפקידי עוזר ומקבל עותק אינם נתמכים כרגע בחתימה על מספר מסמכים. | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 184 | Assisted | סייע/ה במסמך | [Recipient role actioned] packages/lib/constants/recipient-roles.ts |
| 185 | Assisting | מסייע | [Recipient role progressive verb] packages/lib/constants/recipient-roles.ts |
| 186 | Attachments | קבצים מצורפים | apps/remix/app/components/general/document-signing/document-signing-attachments-popover.tsx, apps/remix/app/components/general/document-signing/document-signing-attachments-popover.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx |
| 187 | Audit Log | יומן ביקורת | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 188 | Authentication Level | רמת אימות | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 189 | Authentication required | נדרש אימות | apps/remix/app/components/general/direct-template/direct-template-signing-auth-page.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-page.tsx |
| 190 | Authenticator app | אפליקציית אימות | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 191 | Authorise your signature with your signing provider in the popup window | יש לאשר את החתימה מול ספק החתימה בחלון הקופץ | apps/remix/app/components/general/envelope-signing/envelope-signing-csc-status.tsx |
| 192 | Automatically sign fields | חתימה אוטומטית על שדות | apps/remix/app/components/general/document-signing/document-signing-auto-sign.tsx |
| 193 | Back | חזרה | apps/remix/app/components/general/direct-template/direct-template-signing-form.tsx |
| 194 | Back home | חזרה לדף הבית | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 195 | Before you get started, please confirm your email address by clicking the button below: | לפני שמתחילים, נא לאשר את כתובת הדוא״ל שלכם בלחיצה על הכפתור שלמטה: | packages/email/template-components/template-confirmation-email.tsx |
| 196 | Black | שחור | packages/ui/primitives/signature-pad/signature-pad-color-picker.tsx |
| 197 | Blue | כחול | packages/ui/primitives/signature-pad/signature-pad-color-picker.tsx |
| 198 | Bulk send operation complete for template "{templateName}" | השליחה המרובה עבור התבנית "{templateName}" הושלמה | packages/email/templates/bulk-send-complete.tsx |
| 199 | by &lt;0&gt;{senderName}&lt;/0&gt; | מאת &lt;0&gt;{senderName}&lt;/0&gt; | packages/email/templates/organisation-invite.tsx |
| 200 | By accepting this request, you will be granting &lt;0&gt;{teamName}&lt;/0&gt; access to: | אישור הבקשה יעניק ל-&lt;0&gt;{teamName}&lt;/0&gt; גישה אל: | packages/email/templates/confirm-team-email.tsx |
| 201 | By enabling 2FA, you will be required to enter a code from your authenticator app every time you sign in using email password. | לאחר הפעלת 2FA, תידרשו להזין קוד מאפליקציית האימות בכל התחברות באמצעות דוא״ל וסיסמה. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 202 | By proceeding to use the electronic signature service provided by Documenso, you affirm that you have read and understood this disclosure. You agree to all terms and conditions related to the use of electronic signatures and electronic transactions as outlined herein. | בהמשך השימוש בשירות החתימה האלקטרונית, הנכם מאשרים שקראתם והבנתם הודעה זו, ומסכימים לכל התנאים הנוגעים לשימוש בחתימות אלקטרוניות ובעסקאות אלקטרוניות כמפורט בה. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 203 | By proceeding with your electronic signature, you acknowledge and consent that it will be used to sign the given document and holds the same legal validity as a handwritten signature. By completing the electronic signing process, you affirm your understanding and acceptance of these conditions. | בהמשך החתימה האלקטרונית, הנכם מאשרים ומסכימים שהיא תשמש לחתימה על המסמך הנוכחי ושיש לה תוקף משפטי זהה לזה של חתימה בכתב יד. בהשלמת תהליך החתימה האלקטרונית, הנכם מאשרים שהבנתם תנאים אלה ומקבלים אותם. | apps/remix/app/components/general/document-signing/document-signing-disclosure.tsx |
| 204 | By using the electronic signature feature, you are consenting to conduct transactions and receive disclosures electronically. You acknowledge that your electronic signature on documents is binding and that you accept the terms outlined in the documents you are signing. | בשימוש באפשרות החתימה האלקטרונית, הנכם מסכימים לבצע עסקאות ולקבל הודעות באופן אלקטרוני. הנכם מאשרים שהחתימה האלקטרונית שלכם על מסמכים מחייבת, ושהנכם מקבלים את התנאים המפורטים במסמכים שעליהם אתם חותמים. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 205 | Cancel | ביטול | apps/remix/app/components/dialogs/sign-field-checkbox-dialog.tsx, apps/remix/app/components/dialogs/sign-field-email-dialog.tsx, apps/remix/app/components/dialogs/sign-field-initials-dialog.tsx (+22) |
| 206 | Cc | מקבל עותק | [Recipient role name] packages/lib/constants/recipient-roles.ts |
| 207 | CC | לקבל עותק של המסמך | [Recipient role action verb] packages/lib/constants/recipient-roles.ts |
| 208 | CC | מקבל עותק | [Recipient role progressive verb] packages/lib/constants/recipient-roles.ts |
| 209 | CC'd | קיבל/ה עותק של המסמך | [Recipient role actioned] packages/lib/constants/recipient-roles.ts |
| 210 | Ccers | מקבלי עותק | [Recipient role plural name] packages/lib/constants/recipient-roles.ts |
| 211 | Checkbox | תיבת סימון | packages/lib/utils/fields.ts |
| 212 | Checkbox option | אפשרות בתיבת סימון | packages/ui/primitives/document-flow/field-content.tsx |
| 213 | Choose verification method | בחירת שיטת אימות | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 214 | Choose your preferred authentication method: | נא לבחור את שיטת האימות המועדפת: | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx |
| 215 | Clear Signature | ניקוי החתימה | packages/ui/primitives/signature-pad/signature-pad-draw.tsx |
| 216 | Click to insert field | לחצו להוספת השדה | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx (+3) |
| 217 | Close | סגירה | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-set-password.tsx (+2) |
| 218 | Collapse sidebar | כיווץ סרגל הצד | apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx |
| 219 | Complete | השלמה | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx (+4) |
| 220 | Complete sign in in the popup window | יש להשלים את ההתחברות בחלון הקופץ | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 221 | Complete sign in with your signing provider in the popup window | יש להשלים את ההתחברות מול ספק החתימה בחלון הקופץ | apps/remix/app/components/embed/embed-csc-authentication-required.tsx |
| 222 | Complete the fields for the following signers. | נא למלא את השדות עבור החותמים הבאים. | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 223 | Completed | הושלם | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx, packages/email/template-components/template-document-completed.tsx, packages/email/template-components/template-document-recipient-signed.tsx (+1) |
| 224 | Completed Document | מסמך שהושלם | packages/email/templates/document-completed.tsx, packages/email/templates/document-self-signed.tsx |
| 225 | Completed on {formattedDate} | הושלם בתאריך {formattedDate} | apps/remix/app/components/general/document/document-certificate-qr-view.tsx, apps/remix/app/components/general/document/document-certificate-qr-view.tsx |
| 226 | Configuration Error | שגיאת תצורה | packages/lib/constants/pdf-viewer-i18n.ts, packages/lib/constants/pdf-viewer-i18n.ts, packages/lib/constants/pdf-viewer-i18n.ts (+1) |
| 227 | Confirm | אישור | apps/remix/app/components/dialogs/sign-field-checkbox-dialog.tsx |
| 228 | Confirm email | אישור כתובת הדוא״ל | packages/email/template-components/template-confirmation-email.tsx |
| 229 | Connecting to the embed... | מתחבר להטמעה... | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 230 | Consent to Electronic Transactions | הסכמה לעסקאות אלקטרוניות | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 231 | Contact Information | פרטי התקשרות | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 232 | Continue | המשך | apps/remix/app/components/embed/embed-popup-auth.tsx, apps/remix/app/components/general/document-signing/document-signing-form.tsx, apps/remix/app/routes/embed+/auth+/popup.tsx |
| 233 | Continue by approving the document. | להמשך, יש לאשר את המסמך. | packages/email/template-components/template-document-invite.tsx, packages/email/template-components/template-document-reminder.tsx |
| 234 | Continue by assisting with the document. | להמשך, יש לסייע במילוי המסמך. | packages/email/template-components/template-document-invite.tsx, packages/email/template-components/template-document-reminder.tsx |
| 235 | Continue by downloading the document. | להמשך, יש להוריד את המסמך. | packages/email/template-components/template-document-completed.tsx |
| 236 | Continue by signing the document. | להמשך, יש לחתום על המסמך. | packages/email/template-components/template-document-invite.tsx, packages/email/template-components/template-document-reminder.tsx |
| 237 | Continue by viewing the document. | להמשך, יש לצפות במסמך. | packages/email/template-components/template-document-invite.tsx, packages/email/template-components/template-document-reminder.tsx |
| 238 | Continue to your signing provider | המשך אל ספק החתימה | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 239 | Continue with {0} | המשך עם {0} | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 240 | Continue with Google | המשך עם Google | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 241 | Continue with Microsoft | המשך עם Microsoft | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 242 | Could not connect to the Documenso embed. Close this window and try again. | לא ניתן היה להתחבר להטמעה. נא לסגור חלון זה ולנסות שוב. | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 243 | Create a &lt;0&gt;free account&lt;/0&gt; to access your signed documents at any time. | באפשרותכם ליצור &lt;0&gt;חשבון חינמי&lt;/0&gt; כדי לגשת למסמכים החתומים שלכם בכל עת. | packages/email/template-components/template-document-self-signed.tsx |
| 244 | Create account | יצירת חשבון | packages/email/template-components/template-document-self-signed.tsx |
| 245 | Create your account and start using state-of-the-art document signing. | צרו חשבון והתחילו לחתום על מסמכים בטכנולוגיה מתקדמת. | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 246 | Created At | נוצר בתאריך | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 247 | Date | תאריך | apps/remix/app/components/general/document-signing/document-signing-date-field.tsx, packages/lib/utils/fields.ts |
| 248 | Decline | דחייה | packages/email/templates/organisation-invite.tsx |
| 249 | Deleted | נמחק | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 250 | Details | פרטים | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 251 | Device | מכשיר | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 252 | Did not expect this email? &lt;0&gt;Click here to report the sender&lt;/0&gt;. Never sign a document you don't recognize or weren't expecting. | לא ציפיתם להודעה זו? &lt;0&gt;לחצו כאן כדי לדווח על השולח&lt;/0&gt;. אין לחתום על מסמך שאינכם מזהים או שלא ציפיתם לו. | packages/email/template-components/template-footer.tsx |
| 253 | Didn't request a password change? We are here to help you secure your account, just &lt;0&gt;contact us&lt;/0&gt;. | לא ביקשתם לשנות את הסיסמה? נשמח לעזור לכם לאבטח את החשבון – פשוט &lt;0&gt;צרו איתנו קשר&lt;/0&gt;. | packages/email/templates/reset-password.tsx |
| 254 | Document "{0}" - Rejected by {1} | המסמך "{0}" – נדחה על ידי {1} | packages/lib/jobs/definitions/emails/send-rejection-emails.handler.ts |
| 255 | Document "{0}" - Rejection Confirmed | המסמך "{0}" – הדחייה אושרה | packages/lib/jobs/definitions/emails/send-rejection-emails.handler.ts |
| 256 | Document "{0}" Cancelled | המסמך "{0}" בוטל | packages/lib/jobs/definitions/emails/send-document-cancelled-emails.handler.ts |
| 257 | Document access auth updated | אימות הגישה למסמך עודכן | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 258 | Document already signed | המסמך כבר נחתם | apps/remix/app/components/general/envelope-signing/envelope-signing-complete-dialog.tsx |
| 259 | Document Approved | המסמך אושר | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 260 | Document cancelled | המסמך בוטל | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 261 | Document Cancelled | המסמך בוטל | apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx, apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx, packages/lib/jobs/definitions/emails/send-document-deleted-emails.handler.ts |
| 262 | Document completed | המסמך הושלם | [Audit log format] packages/lib/utils/document-audit-logs.ts, packages/lib/utils/document-audit-logs.ts, packages/lib/utils/document-audit-logs.ts |
| 263 | Document Completed | המסמך הושלם | apps/remix/app/components/embed/embed-document-completed.tsx |
| 264 | Document created | המסמך נוצר | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 265 | Document created from direct template | נוצר מסמך מתבנית ישירה | packages/email/templates/document-created-from-direct-template.tsx, packages/lib/jobs/definitions/emails/send-document-created-from-direct-template-email.handler.ts |
| 266 | Document deleted | המסמך נמחק | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 267 | Document external ID updated | המזהה החיצוני של המסמך עודכן | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 268 | Document found in your account | המסמך נמצא בחשבון שלכם | apps/remix/app/components/general/document/document-certificate-qr-view.tsx |
| 269 | Document moved to team | המסמך הועבר לצוות | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 270 | Document no longer available to sign | המסמך אינו זמין עוד לחתימה | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 271 | Document opened | המסמך נפתח | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 272 | Document rejected | המסמך נדחה | apps/remix/app/components/general/document-signing/document-signing-reject-dialog.tsx |
| 273 | Document Rejected | המסמך נדחה | apps/remix/app/components/embed/embed-document-rejected.tsx, apps/remix/app/routes/_recipient+/sign.$token+/rejected.tsx, packages/email/template-components/template-document-rejected.tsx |
| 274 | Document sent | המסמך נשלח | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 275 | Document Signed | המסמך נחתם | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 276 | Document signing auth updated | אימות החתימה על המסמך עודכן | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 277 | Document title updated | כותרת המסמך עודכנה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 278 | Document updated | המסמך עודכן | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 279 | Document viewed | המסמך נצפה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 280 | Document Viewed | המסמך נצפה | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 281 | Document visibility updated | נראות המסמך עודכנה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 282 | Documents and resources related to this envelope. | מסמכים ומשאבים הקשורים למעטפה זו. | apps/remix/app/components/general/document-signing/document-signing-attachments-popover.tsx |
| 283 | Download | הורדה | apps/remix/app/components/general/document/document-certificate-qr-view.tsx, apps/remix/app/components/general/document/document-certificate-qr-view.tsx, apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx (+1) |
| 284 | Download PDF | הורדת PDF | apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx, apps/remix/app/components/general/envelope-signing/envelope-signer-header.tsx |
| 285 | Draw | ציור | [Draw signature] packages/ui/primitives/signature-pad/signature-pad.tsx |
| 286 | Electronic Delivery of Documents | מסירה אלקטרונית של מסמכים | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 287 | Electronic Signature Disclosure | גילוי נאות בנושא חתימה אלקטרונית | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 288 | Email | דוא״ל | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx (+7) |
| 289 | Email is required | יש להזין כתובת דוא״ל | apps/remix/app/components/dialogs/sign-field-email-dialog.tsx |
| 290 | Email resent | הדוא״ל נשלח שוב | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 291 | Email sent | הדוא״ל נשלח | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 292 | Email verification | אימות בדוא״ל | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 293 | Enclosed Document | המסמך המצורף | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx |
| 294 | Enclosed Documents | המסמכים המצורפים | packages/lib/server-only/pdf/render-audit-logs.ts |
| 295 | Enter | הזנה | apps/remix/app/components/dialogs/sign-field-email-dialog.tsx, apps/remix/app/components/dialogs/sign-field-initials-dialog.tsx, apps/remix/app/components/dialogs/sign-field-name-dialog.tsx (+2) |
| 296 | Enter Email | הזנת כתובת דוא״ל | apps/remix/app/components/dialogs/sign-field-email-dialog.tsx |
| 297 | Enter Initials | הזנת ראשי תיבות | apps/remix/app/components/dialogs/sign-field-initials-dialog.tsx |
| 298 | Enter Name | הזנת שם | apps/remix/app/components/dialogs/sign-field-name-dialog.tsx |
| 299 | Enter Number | הזנת מספר | apps/remix/app/components/dialogs/sign-field-number-dialog.tsx |
| 300 | Enter Text | הזנת טקסט | apps/remix/app/components/dialogs/sign-field-text-dialog.tsx |
| 301 | Enter the next signer's email | נא להזין את כתובת הדוא״ל של החותם הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 302 | Enter the next signer's name | נא להזין את שם החותם הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 303 | Enter verification code | הזנת קוד אימות | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 304 | Enter your 2FA code | נא להזין את קוד ה-2FA | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx |
| 305 | Enter your email | נא להזין כתובת דוא״ל | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 306 | Enter your email address to receive the completed document. | נא להזין את כתובת הדוא״ל שלכם כדי לקבל את המסמך החתום. | apps/remix/app/components/general/direct-template/direct-template-configure-form.tsx |
| 307 | Enter your name | נא להזין את שמכם | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 308 | Enter your number here | נא להזין מספר כאן | apps/remix/app/components/dialogs/sign-field-number-dialog.tsx |
| 309 | Enter your password | נא להזין סיסמה | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-password.tsx |
| 310 | Enter your text here | נא להזין טקסט כאן | apps/remix/app/components/dialogs/sign-field-text-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-text-field.tsx |
| 311 | Envelope ID | מזהה מעטפה | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts, packages/lib/server-only/pdf/render-audit-logs.ts (+3) |
| 312 | Envelope item created | נוצר פריט מעטפה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 313 | Envelope item deleted | נמחק פריט מעטפה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 314 | Envelope item PDF replaced | קובץ ה-PDF של פריט מעטפה הוחלף | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 315 | Envelope item updated | פריט מעטפה עודכן | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 316 | Error | שגיאה | apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx, apps/remix/app/components/general/document-signing/document-signing-auto-sign.tsx, apps/remix/app/components/general/document-signing/document-signing-checkbox-field.tsx (+24) |
| 317 | Error loading page | שגיאה בטעינת העמוד | apps/remix/app/components/general/pdf-viewer/pdf-viewer-page-image.tsx |
| 318 | Everyone has signed | כל הנמענים חתמו | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 319 | Everyone has signed! You will receive an email copy of the signed document. | כל הנמענים חתמו! עותק של המסמך החתום יישלח אליכם בדוא״ל. | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 320 | Expand sidebar | הרחבת סרגל הצד | apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx |
| 321 | Expires in {0} | יפוג בעוד {0} | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 322 | Failed to load document | טעינת המסמך נכשלה | apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx |
| 323 | Failed: {failedCount} | נכשלו: {failedCount} | packages/email/templates/bulk-send-complete.tsx |
| 324 | Field prefilled by assistant | שדה מולא מראש על ידי עוזר | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 325 | Field signed | שדה נחתם | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 326 | Field unsigned | חתימת שדה בוטלה | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 327 | For any questions regarding this disclosure, electronic signatures, or any related process, please contact us at: &lt;0&gt;{SUPPORT_EMAIL}&lt;/0&gt; | לכל שאלה בנוגע להודעה זו, לחתימות אלקטרוניות או לכל תהליך קשור, ניתן לפנות אלינו בכתובת: &lt;0&gt;{SUPPORT_EMAIL}&lt;/0&gt; | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 328 | Forgot your password? | שכחתם את הסיסמה? | packages/email/template-components/template-forgot-password.tsx |
| 329 | Free Signature | חתימה חופשית | packages/lib/utils/fields.ts |
| 330 | Full Name | שם מלא | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx (+4) |
| 331 | General | כללי | apps/remix/app/components/general/direct-template/direct-template-page.tsx |
| 332 | Go Back | חזרה | apps/remix/app/components/general/generic-error-layout.tsx, apps/remix/app/routes/_recipient+/_layout.tsx |
| 333 | Go Back Home | חזרה לדף הבית | apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx, apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx, apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 334 | Go to document | מעבר למסמך | apps/remix/app/components/general/document/document-certificate-qr-view.tsx |
| 335 | Green | ירוק | packages/ui/primitives/signature-pad/signature-pad-color-picker.tsx |
| 336 | Help complete the document for other signers. | סיוע בהשלמת המסמך עבור חותמים אחרים. | apps/remix/app/components/embed/embed-document-signing-page-v1.tsx |
| 337 | Hi {recipientName}, | שלום {recipientName}, | packages/email/template-components/template-document-reminder.tsx |
| 338 | Hi {userName}, | שלום {userName}, | packages/email/templates/bulk-send-complete.tsx |
| 339 | Hi {userName}, you need to enter a verification code to complete the document "{documentTitle}". | שלום {userName}, יש להזין קוד אימות כדי להשלים את המסמך "{documentTitle}". | packages/email/template-components/template-access-auth-2fa.tsx |
| 340 | Hi, {userName} &lt;0&gt;({userEmail})&lt;/0&gt; | שלום {userName} &lt;0&gt;({userEmail})&lt;/0&gt; | packages/email/templates/reset-password.tsx |
| 341 | Home | בית | apps/remix/app/components/general/generic-error-layout.tsx |
| 342 | I am a signer of this document | אני חותם/ת על מסמך זה | packages/lib/constants/recipient-roles.ts |
| 343 | I am a viewer of this document | אני צופה במסמך זה | packages/lib/constants/recipient-roles.ts |
| 344 | I am an approver of this document | אני מאשר/ת מסמך זה | packages/lib/constants/recipient-roles.ts |
| 345 | I am an assistant of this document | אני עוזר/ת במסמך זה | packages/lib/constants/recipient-roles.ts |
| 346 | I am required to receive a copy of this document | אני נדרש/ת לקבל עותק של מסמך זה | packages/lib/constants/recipient-roles.ts |
| 347 | I am the owner of this document | אני הבעלים של מסמך זה | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 348 | If this was you, no action is needed. If it wasn't, reset your password immediately and &lt;0&gt;contact us&lt;/0&gt;. | אם הפעולה בוצעה על ידכם, אין צורך לעשות דבר. אם לא, יש לאפס את הסיסמה מיד ו&lt;0&gt;ליצור איתנו קשר&lt;/0&gt;. | packages/email/templates/reset-password.tsx |
| 349 | If you believe this is a mistake, please contact the sender directly. | אם לדעתכם מדובר בטעות, נא לפנות ישירות לשולח. | apps/remix/app/components/general/document-signing/document-signing-sender-disabled-page.tsx |
| 350 | If you believe this was a mistake, contact us at &lt;0&gt;{supportEmail}&lt;/0&gt;. | אם לדעתכם מדובר בטעות, ניתן לפנות אלינו בכתובת &lt;0&gt;{supportEmail}&lt;/0&gt;. | packages/email/template-components/template-account-disabled.tsx |
| 351 | If you did not expect this email or believe it is spam, you can report the sender to our team for review. | אם לא ציפיתם להודעת דוא״ל זו או שלדעתכם מדובר בדואר זבל, באפשרותכם לדווח על השולח לצוות שלנו לבדיקה. | apps/remix/app/routes/_recipient+/report.$token.tsx |
| 352 | If you didn't expect this account or have any questions, please &lt;0&gt;contact support&lt;/0&gt;. | אם לא ציפיתם לחשבון זה או שיש לכם שאלות, נא &lt;0&gt;לפנות לתמיכה&lt;/0&gt;. | packages/email/template-components/template-admin-user-created.tsx |
| 353 | If you didn't request this verification code, you can safely ignore this email. | אם לא ביקשתם קוד אימות זה, ניתן להתעלם מהודעה זו. | packages/email/template-components/template-access-auth-2fa.tsx |
| 354 | If you expect to need higher limits, please contact support at {SUPPORT_EMAIL} and we will review your account. | אם צפוי שתזדקקו למגבלות גבוהות יותר, נא לפנות לתמיכה בכתובת {SUPPORT_EMAIL} ואנו נבחן את החשבון שלכם. | packages/email/templates/organisation-limit-alert.tsx |
| 355 | If you have any questions, please contact support at {SUPPORT_EMAIL}. | לכל שאלה, ניתן לפנות לתמיכה בכתובת {SUPPORT_EMAIL}. | packages/email/templates/organisation-limits-updated.tsx |
| 356 | If you recently received an email regarding your usage limits, this change was made in response to that. | אם קיבלתם לאחרונה הודעת דוא״ל בנוגע למגבלות השימוש שלכם, שינוי זה בוצע בעקבותיה. | packages/email/templates/organisation-limits-updated.tsx |
| 357 | Initials | ראשי תיבות | apps/remix/app/components/dialogs/sign-field-initials-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-initials-field.tsx, packages/lib/utils/fields.ts |
| 358 | Initials are required | יש להזין ראשי תיבות | apps/remix/app/components/dialogs/sign-field-initials-dialog.tsx |
| 359 | Invalid direct link template | תבנית קישור ישיר לא תקינה | apps/remix/app/components/general/direct-template/direct-template-invalid-page.tsx |
| 360 | IP Address | כתובת IP | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-audit-logs.ts, packages/lib/server-only/pdf/render-certificate.ts |
| 361 | It is crucial to keep your contact information, especially your email address, up to date with us. Please notify us immediately of any changes to ensure that you continue to receive all necessary communications. | חשוב מאוד לעדכן אותנו בפרטי ההתקשרות שלכם, ובמיוחד בכתובת הדוא״ל. נא להודיע לנו מיד על כל שינוי, כדי להבטיח שתמשיכו לקבל את כל ההודעות הנדרשות. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 362 | It looks like we ran into an issue! | נראה שנתקלנו בבעיה! | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 363 | It's currently not your turn to sign. Please check back soon as this document should be available for you to sign shortly. | זה עדיין לא תורכם לחתום. נא לבדוק שוב בקרוב – המסמך אמור להיות זמין לחתימתכם בקרוב. | apps/remix/app/components/embed/embed-document-waiting-for-turn.tsx |
| 364 | It's currently not your turn to sign. You will receive an email with instructions once it's your turn to sign the document. | זה עדיין לא תורכם לחתום. כשיגיע תורכם לחתום על המסמך, תישלח אליכם הודעת דוא״ל עם הנחיות. | apps/remix/app/routes/_recipient+/sign.$token+/waiting.tsx |
| 365 | Join {organisationName} on Documenso | הצטרפות לארגון {organisationName} | packages/email/templates/organisation-invite.tsx |
| 366 | Last Updated | עדכון אחרון | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 367 | Legality of Electronic Signatures | תוקפן המשפטי של חתימות אלקטרוניות | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 368 | Link expires in 1 hour. | תוקף הקישור יפוג בעוד שעה. | packages/email/templates/confirm-team-email.tsx |
| 369 | Link expires in 30 minutes. | תוקף הקישור יפוג בעוד 30 דקות. | packages/email/templates/organisation-account-link-confirmation.tsx |
| 370 | Link your Documenso account | קישור החשבון שלכם | packages/email/templates/organisation-account-link-confirmation.tsx |
| 371 | Loading document... | המסמך נטען... | apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx |
| 372 | Loading... | טוען... | apps/remix/app/components/embed/embed-client-loading.tsx |
| 373 | Login | התחברות | apps/remix/app/components/general/direct-template/direct-template-signing-auth-page.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-page.tsx |
| 374 | Mark as viewed | סימון כנצפה | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 375 | Mark as Viewed | סימון כנצפה | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 376 | N/A | לא רלוונטי | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 377 | Name | שם | apps/remix/app/components/general/document-signing/document-signing-name-field.tsx, packages/lib/utils/fields.ts |
| 378 | Name is required | יש להזין שם | apps/remix/app/components/dialogs/sign-field-name-dialog.tsx |
| 379 | Need to sign documents? | צריכים לחתום על מסמכים? | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 380 | Next | הבא | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx (+1) |
| 381 | Next Field | השדה הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 382 | Next Recipient Email | כתובת הדוא״ל של הנמען הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 383 | Next Recipient Name | שם הנמען הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 384 | No document found | לא נמצא מסמך | apps/remix/app/components/general/pdf-viewer/envelope-pdf-viewer.tsx, apps/remix/app/components/general/pdf-viewer/pdf-viewer.tsx |
| 385 | No document selected | לא נבחר מסמך | apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx |
| 386 | No further action is required | אין צורך בפעולה נוספת | apps/remix/app/components/embed/embed-document-completed.tsx |
| 387 | No further action is required from you at this time. | אין צורך בפעולה נוספת מצדכם בשלב זה. | apps/remix/app/components/embed/embed-document-rejected.tsx, apps/remix/app/routes/_recipient+/sign.$token+/rejected.tsx |
| 388 | No password set | לא הוגדרה סיסמה | apps/remix/app/components/general/document-signing/document-signing-auth-set-password.tsx |
| 389 | No signing credentials available | אין אמצעי חתימה זמינים | apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx |
| 390 | Not Found | לא נמצא | apps/remix/app/routes/embed+/_v0+/_layout.tsx |
| 391 | Number | מספר | apps/remix/app/components/general/document-signing/document-signing-number-field.tsx, packages/lib/utils/fields.ts |
| 392 | Number needs to be formatted as {numberFormat} | יש להזין את המספר בתבנית {numberFormat} | apps/remix/app/components/dialogs/sign-field-number-dialog.tsx |
| 393 | One of the documents in the current bundle has a signing role that is not compatible with the current signing experience. | לאחד המסמכים בחבילה הנוכחית יש תפקיד חתימה שאינו תואם לחוויית החתימה הנוכחית. | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 394 | One of your signing requests has been reported. As part of keeping signers safe, we've disabled your account for now. | אחת מבקשות החתימה שלכם דווחה. כחלק מהשמירה על בטיחות החותמים, החשבון שלכם הושבת בשלב זה. | packages/email/template-components/template-account-disabled.tsx |
| 395 | Only sign if you know and were expecting this sender. | יש לחתום רק אם אתם מכירים את השולח וציפיתם למסמך ממנו. | packages/email/template-components/template-new-account-warning.tsx |
| 396 | Only sign if you know and were expecting this sender. &lt;0&gt;Report sender&lt;/0&gt; | יש לחתום רק אם אתם מכירים את השולח וציפיתם למסמך ממנו. &lt;0&gt;דיווח על השולח&lt;/0&gt; | packages/email/template-components/template-new-account-warning.tsx |
| 397 | Oops! Something went wrong. | אופס! משהו השתבש. | apps/remix/app/components/general/generic-error-layout.tsx, apps/remix/app/components/general/generic-error-layout.tsx |
| 398 | Options | אפשרויות | apps/remix/app/components/dialogs/sign-field-dropdown-dialog.tsx |
| 399 | Organisation Review Required | נדרשת בדיקת ארגון | packages/email/templates/organisation-limit-alert.tsx, packages/email/templates/organisation-limit-alert.tsx, packages/lib/jobs/definitions/emails/send-organisation-limit-alert-email.handler.ts |
| 400 | Owner | בעלים | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 401 | Page {pageNumber} of {numPages} | עמוד {pageNumber} מתוך {numPages} | apps/remix/app/components/general/pdf-viewer/pdf-viewer.tsx |
| 402 | Passkey | מפתח גישה | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 403 | Passkey Re-Authentication | אימות חוזר באמצעות מפתח גישה | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/generate-certificate-pdf.ts |
| 404 | Passkeys could not be used here. If this document is embedded in another site, that site needs to allow passkeys for the embed. | לא ניתן להשתמש כאן במפתחות גישה. אם מסמך זה מוטמע באתר אחר, על האתר לאפשר שימוש במפתחות גישה בהטמעה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 405 | Password | סיסמה | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-password.tsx |
| 406 | Password authentication unavailable | אימות באמצעות סיסמה אינו זמין | apps/remix/app/components/general/document-signing/document-signing-auth-set-password.tsx |
| 407 | Password Re-Authentication | אימות חוזר באמצעות סיסמה | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/generate-certificate-pdf.ts |
| 408 | Password Reset Requested | התקבלה בקשה לאיפוס סיסמה | packages/email/templates/forgot-password.tsx |
| 409 | Password Reset Successful | הסיסמה אופסה בהצלחה | packages/email/templates/reset-password.tsx |
| 410 | Password updated! | הסיסמה עודכנה! | packages/email/template-components/template-reset-password.tsx |
| 411 | Pending | ממתין | packages/ui/components/document/document-read-only-fields.tsx |
| 412 | Pending Document | מסמך ממתין | packages/email/templates/document-pending.tsx |
| 413 | Please {0} your document&lt;0/&gt;"{documentName}" | נא {0}&lt;0/&gt;"{documentName}" | packages/email/template-components/template-document-invite.tsx |
| 414 | Please {action} your document {documentName} | נא {action} {documentName} | packages/email/templates/document-invite.tsx |
| 415 | Please {recipientActionVerb} this document | נא {recipientActionVerb} | packages/lib/jobs/definitions/emails/send-signing-email.handler.ts |
| 416 | Please {recipientActionVerb} this document created by your direct template | נא {recipientActionVerb} שנוצר באמצעות התבנית הישירה שלכם | packages/lib/jobs/definitions/emails/send-signing-email.handler.ts |
| 417 | Please {recipientActionVerb} your document | נא {recipientActionVerb} | packages/lib/jobs/definitions/emails/send-signing-email.handler.ts |
| 418 | Please check with the parent application for more information. | למידע נוסף, נא לפנות לאפליקציה המארחת. | apps/remix/app/components/embed/embed-document-waiting-for-turn.tsx, apps/remix/app/components/embed/embed-recipient-expired.tsx, apps/remix/app/components/embed/embed-sender-disabled.tsx |
| 419 | Please check your email for updates. | עדכונים יישלחו אליכם בדוא״ל. | apps/remix/app/routes/_recipient+/sign.$token+/waiting.tsx |
| 420 | Please complete the document once reviewed | נא להשלים את המסמך לאחר העיון בו | apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx, apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx, apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx |
| 421 | Please confirm your email address | נא לאשר את כתובת הדוא״ל שלכם | packages/email/templates/confirm-email.tsx |
| 422 | Please contact &lt;0&gt;support&lt;/0&gt; if you have any questions. | לכל שאלה, ניתן לפנות &lt;0&gt;לתמיכה&lt;/0&gt;. | apps/remix/app/components/embed/embed-paywall.tsx |
| 423 | Please contact support at {SUPPORT_EMAIL} and we will review your account. | נא לפנות לתמיכה בכתובת {SUPPORT_EMAIL} ואנו נבחן את החשבון שלכם. | packages/email/templates/organisation-limit-alert.tsx |
| 424 | Please contact the site owner for further assistance. | לסיוע נוסף, נא לפנות לבעלי האתר. | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 425 | Please don't close this tab. The signing provider is finalising your signature. | נא לא לסגור את הלשונית. ספק החתימה משלים את החתימה שלכם. | apps/remix/app/components/general/document-signing/csc-recipient-signing-in-progress-page.tsx |
| 426 | Please enter a number | נא להזין מספר | apps/remix/app/components/dialogs/sign-field-number-dialog.tsx |
| 427 | Please enter a valid number | נא להזין מספר תקין | apps/remix/app/components/dialogs/sign-field-number-dialog.tsx |
| 428 | Please enter a value | נא להזין ערך | apps/remix/app/components/dialogs/sign-field-text-dialog.tsx |
| 429 | Please enter your email address | נא להזין את כתובת הדוא״ל שלכם | apps/remix/app/components/dialogs/sign-field-email-dialog.tsx |
| 430 | Please enter your full name | נא להזין את שמכם המלא | apps/remix/app/components/dialogs/sign-field-name-dialog.tsx |
| 431 | Please enter your initials | נא להזין את ראשי התיבות שלכם | apps/remix/app/components/dialogs/sign-field-initials-dialog.tsx |
| 432 | Please follow any instructions provided within the parent application. | נא לפעול לפי ההנחיות שמופיעות באפליקציה המארחת. | apps/remix/app/components/embed/embed-document-completed.tsx |
| 433 | Please mark as viewed to complete | להשלמה, יש לסמן כנצפה | apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx |
| 434 | Please mark as viewed to complete. | להשלמה, יש לסמן כנצפה. | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 435 | Please open your authenticator app and enter the 6-digit code for this document. | נא לפתוח את אפליקציית האימות ולהזין את הקוד בן 6 הספרות עבור מסמך זה. | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 436 | Please provide a reason for rejecting this document | נא לציין את הסיבה לדחיית המסמך | apps/remix/app/components/general/document-signing/document-signing-reject-dialog.tsx |
| 437 | Please review the document before approving. | נא לעיין במסמך לפני האישור. | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 438 | Please review the document before signing. | נא לעיין במסמך לפני החתימה. | apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx |
| 439 | Please select how you'd like to receive your verification code. | נא לבחור כיצד לקבל את קוד האימות. | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 440 | Please try again or contact our support. | נא לנסות שוב או לפנות לתמיכה. | apps/remix/app/components/general/pdf-viewer/pdf-viewer-states.tsx |
| 441 | Please upload a valid image file. | נא להעלות קובץ תמונה תקין. | packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 442 | Powered by | מופעל על ידי | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx (+3) |
| 443 | Preview and configure template. | תצוגה מקדימה והגדרת התבנית. | apps/remix/app/components/general/direct-template/direct-template-page.tsx |
| 444 | Processing document | המסמך בעיבוד | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 445 | Progress | התקדמות | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 446 | Qualified electronic signatures are not supported in this embed. | חתימות אלקטרוניות מאושרות אינן נתמכות בהטמעה זו. | apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx, apps/remix/app/routes/embed+/v1+/multisign+/_index.tsx |
| 447 | Radio | בחירה יחידה | packages/lib/utils/fields.ts |
| 448 | Read the full &lt;0&gt;signature disclosure&lt;/0&gt;. | לקריאת &lt;0&gt;הגילוי הנאות בנושא חתימה אלקטרונית&lt;/0&gt; המלא. | apps/remix/app/components/general/document-signing/document-signing-disclosure.tsx |
| 449 | Reason | סיבה | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 450 | Reason for cancellation: {cancellationReason} | סיבת הביטול: {cancellationReason} | packages/email/template-components/template-document-cancel.tsx |
| 451 | Reason for rejection: {rejectionReason} | סיבת הדחייה: {rejectionReason} | packages/email/template-components/template-document-rejected.tsx |
| 452 | Reason must be less than 500 characters | הסיבה חייבת להכיל פחות מ-500 תווים | apps/remix/app/components/general/document-signing/document-signing-reject-dialog.tsx |
| 453 | Reauthentication is required to sign this field | נדרש אימות חוזר כדי לחתום על שדה זה | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx |
| 454 | Reauthorise and retry | אישור מחדש וניסיון חוזר | apps/remix/app/components/general/document-signing/csc-recipient-signing-in-progress-page.tsx, apps/remix/app/components/general/envelope-signing/envelope-signing-csc-status.tsx |
| 455 | Recipient approved the document | המסמך אושר על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 456 | Recipient authenticated with the signing provider | הנמען ביצע אימות מול ספק החתימה | packages/lib/utils/document-audit-logs.ts |
| 457 | Recipient authorised the remote signature | החתימה המרוחקת אושרה על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 458 | Recipient CC'd the document | עותק של המסמך נמסר לנמען | packages/lib/utils/document-audit-logs.ts |
| 459 | Recipient completed their task | המשימה הושלמה על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 460 | Recipient failed to validate a 2FA token for the document | אימות קוד 2FA למסמך נכשל עבור הנמען | packages/lib/utils/document-audit-logs.ts |
| 461 | Recipient rejected the document | המסמך נדחה על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 462 | Recipient rejected the document externally | המסמך נדחה על ידי הנמען באופן חיצוני | packages/lib/utils/document-audit-logs.ts |
| 463 | Recipient requested a 2FA token for the document | קוד 2FA למסמך התבקש על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 464 | Recipient requested a remote signature | חתימה מרוחקת התבקשה על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 465 | Recipient signed the document | המסמך נחתם על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 466 | Recipient signing window expired | חלון הזמן לחתימת הנמען פג | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 467 | Recipient validated a 2FA token for the document | קוד 2FA למסמך אומת על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 468 | Recipient viewed the document | המסמך נצפה על ידי הנמען | packages/lib/utils/document-audit-logs.ts |
| 469 | Recipient's remote signature was applied | החתימה המרוחקת של הנמען הוחלה | packages/lib/utils/document-audit-logs.ts |
| 470 | Recipient's signing provider authentication failed | האימות של הנמען מול ספק החתימה נכשל | packages/lib/utils/document-audit-logs.ts |
| 471 | Recipients | נמענים | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 472 | Red | אדום | packages/ui/primitives/signature-pad/signature-pad-color-picker.tsx |
| 473 | Redirecting to your sign in provider... | מעבר לספק ההתחברות... | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 474 | Reject | דחייה | apps/remix/app/components/general/envelope-signing/envelope-signer-header.tsx |
| 475 | Reject Document | דחיית המסמך | apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx, apps/remix/app/components/general/document-signing/document-signing-reject-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-reject-dialog.tsx (+1) |
| 476 | Rejected | נדחה | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx, apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 477 | Rejection Confirmed | הדחייה אושרה | packages/email/template-components/template-document-rejection-confirmed.tsx |
| 478 | Rejection reason: {reason} | סיבת הדחייה: {reason} | packages/email/template-components/template-document-rejection-confirmed.tsx |
| 479 | Reminder to {action} {documentName} | תזכורת {action} {documentName} | packages/email/templates/document-reminder.tsx |
| 480 | Reminder: {0} | תזכורת: {0} | packages/lib/jobs/definitions/internal/process-signing-reminder.handler.ts, packages/lib/server-only/document/resend-document.ts |
| 481 | Reminder: {0} invited you to {recipientActionVerb} a document | תזכורת: הוזמנתם על ידי {0} {recipientActionVerb} | packages/lib/jobs/definitions/internal/process-signing-reminder.handler.ts, packages/lib/server-only/document/resend-document.ts |
| 482 | Reminder: Please {0} your document&lt;0/&gt;"{documentName}" | תזכורת: נא {0}&lt;0/&gt;"{documentName}" | packages/email/template-components/template-document-reminder.tsx |
| 483 | Reminder: Please {recipientActionVerb} the document "{0}" | תזכורת: נא {recipientActionVerb} "{0}" | packages/lib/jobs/definitions/internal/process-signing-reminder.handler.ts |
| 484 | Reminder: Please {recipientActionVerb} this document | תזכורת: נא {recipientActionVerb} | packages/lib/server-only/document/resend-document.ts |
| 485 | Reminder: Please {recipientActionVerb} your document | תזכורת: נא {recipientActionVerb} | packages/lib/server-only/document/resend-document.ts |
| 486 | Remove | הסרה | apps/remix/app/components/general/document-signing/document-signing-field-container.tsx |
| 487 | Report sender | דיווח על השולח | apps/remix/app/routes/_recipient+/report.$token.tsx |
| 488 | Report this sender? | לדווח על שולח זה? | apps/remix/app/routes/_recipient+/report.$token.tsx |
| 489 | Resend code | שליחת קוד חדש | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 490 | Reset Password | איפוס סיסמה | packages/email/template-components/template-forgot-password.tsx |
| 491 | Retention of Documents | שמירת מסמכים | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 492 | Retry | ניסיון חוזר | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 493 | Return | חזרה | apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx |
| 494 | Return Home | חזרה לדף הבית | apps/remix/app/components/general/document-signing/document-signing-sender-disabled-page.tsx, apps/remix/app/routes/_recipient+/sign.$token+/expired.tsx, apps/remix/app/routes/_recipient+/sign.$token+/rejected.tsx (+1) |
| 495 | Review request | עיון בבקשה | packages/email/templates/organisation-account-link-confirmation.tsx |
| 496 | Save | שמירה | apps/remix/app/components/general/document-signing/document-signing-number-field.tsx, apps/remix/app/components/general/document-signing/document-signing-text-field.tsx |
| 497 | Select | בחירה | apps/remix/app/components/general/document-signing/document-signing-dropdown-field.tsx, packages/ui/primitives/document-flow/field-content.tsx |
| 498 | Select an option | נא לבחור אפשרות | apps/remix/app/components/dialogs/sign-field-dropdown-dialog.tsx |
| 499 | Select Option | בחירת אפשרות | packages/lib/utils/fields.ts |
| 500 | Select Options | בחירת אפשרויות | apps/remix/app/components/dialogs/sign-field-checkbox-dialog.tsx |
| 501 | Select passkey | בחירת מפתח גישה | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 502 | Send documents on behalf of the team using the email address | שליחת מסמכים בשם הצוות באמצעות כתובת הדוא״ל | packages/email/templates/confirm-team-email.tsx |
| 503 | Sender Account Disabled | חשבון השולח הושבת | apps/remix/app/components/embed/embed-sender-disabled.tsx, apps/remix/app/components/general/document-signing/document-signing-sender-disabled-page.tsx |
| 504 | Sender reported | דווח על השולח | apps/remix/app/routes/_recipient+/report.$token.tsx |
| 505 | Sent | נשלח | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 506 | Set Password | הגדרת סיסמה | packages/email/template-components/template-admin-user-created.tsx |
| 507 | Set your password for Documenso | הגדרת סיסמה לחשבון שלכם | packages/email/templates/admin-user-created.tsx |
| 508 | Setup | הגדרה | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 509 | Sign | חתימה | apps/remix/app/components/dialogs/sign-field-signature-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx (+5) |
| 510 | Sign | לחתום על המסמך | [Recipient role action verb] packages/lib/constants/recipient-roles.ts |
| 511 | Sign as {0} &lt;0&gt;({1})&lt;/0&gt; | חתימה בשם {0} &lt;0&gt;({1})&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-signature-field.tsx |
| 512 | Sign as&lt;0&gt;{0} &lt;1&gt;({1})&lt;/1&gt;&lt;/0&gt; | חתימה בשם&lt;0&gt;{0} &lt;1&gt;({1})&lt;/1&gt;&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-name-field.tsx |
| 513 | Sign document | חתימה על המסמך | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx |
| 514 | Sign Document | חתימה על המסמך | apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx (+1) |
| 515 | Sign Document - Documenso | חתימה על מסמך | apps/remix/app/routes/_recipient+/_layout.tsx |
| 516 | Sign Documents | חתימה על מסמכים | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 517 | Sign field | חתימה על שדה | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx |
| 518 | Sign In | התחברות | packages/email/template-components/template-reset-password.tsx |
| 519 | Sign in did not complete. Close this window and try again. | ההתחברות לא הושלמה. נא לסגור חלון זה ולנסות שוב. | apps/remix/app/routes/embed+/auth+/complete.tsx |
| 520 | Sign in did not complete. Please try again. | ההתחברות לא הושלמה. נא לנסות שוב. | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 521 | Sign in timed out. Please try again. | זמן ההתחברות פג. נא לנסות שוב. | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 522 | Sign in to Documenso to continue | יש להתחבר כדי להמשיך | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 523 | Sign in to your account | התחברות לחשבון | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx |
| 524 | Sign in with email or passkey | התחברות באמצעות דוא״ל או מפתח גישה | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 525 | Sign in with passkey | התחברות באמצעות מפתח גישה | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 526 | Sign in with your signing provider | התחברות באמצעות ספק החתימה | apps/remix/app/components/embed/embed-csc-authentication-required.tsx |
| 527 | Sign in with your signing provider to continue | יש להתחבר באמצעות ספק החתימה כדי להמשיך | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 528 | Sign Signature Field | חתימה בשדה החתימה | apps/remix/app/components/dialogs/sign-field-signature-dialog.tsx |
| 529 | Sign the document to complete the process. | יש לחתום על המסמך כדי להשלים את התהליך. | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx |
| 530 | Sign up | הרשמה | apps/remix/app/components/general/document-signing/document-signing-auth-page.tsx |
| 531 | Signature | חתימה | apps/remix/app/components/embed/embed-direct-template-client-page.tsx, apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx (+7) |
| 532 | Signature ID | מזהה חתימה | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 533 | Signature is too small | החתימה קטנה מדי | packages/ui/primitives/signature-pad/signature-pad-draw.tsx, packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 534 | Signed | נחתם | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts, packages/ui/components/document/document-read-only-fields.tsx |
| 535 | Signed | חתם/ה על המסמך | [Recipient role actioned] packages/lib/constants/recipient-roles.ts |
| 536 | Signer | חותם | apps/remix/app/components/general/envelope-signing/envelope-signer-header.tsx |
| 537 | Signer | חותם | [Recipient role name] packages/lib/constants/recipient-roles.ts |
| 538 | Signer Events | אירועי חותם | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 539 | Signers | חותמים | [Recipient role plural name] packages/lib/constants/recipient-roles.ts |
| 540 | Signing | חותם | [Recipient role progressive verb] packages/lib/constants/recipient-roles.ts |
| 541 | Signing algorithm is not supported | אלגוריתם החתימה אינו נתמך | apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx |
| 542 | Signing Certificate | תעודת חתימה | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 543 | Signing certificate is invalid | תעודת החתימה אינה תקינה | apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx |
| 544 | Signing certificate provided by | תעודת החתימה סופקה על ידי | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 545 | Signing Complete! | החתימה הושלמה! | packages/lib/jobs/definitions/emails/send-document-completed-emails.handler.ts, packages/lib/jobs/definitions/emails/send-document-completed-emails.handler.ts |
| 546 | Signing Deadline Expired | המועד האחרון לחתימה חלף | apps/remix/app/routes/_recipient+/sign.$token+/expired.tsx |
| 547 | Signing failed | החתימה נכשלה | apps/remix/app/components/general/document-signing/csc-recipient-signing-in-progress-page.tsx |
| 548 | Signing for | חתימה עבור | apps/remix/app/components/embed/embed-document-signing-page-v1.tsx |
| 549 | Signing this field requires a password, but your account does not have one. We can email you a link to set one. Once done, sign in again and return to this document to continue. | החתימה על שדה זה מחייבת סיסמה, אך לחשבון שלכם לא הוגדרה סיסמה. נוכל לשלוח אליכם בדוא״ל קישור להגדרתה. לאחר מכן יש להתחבר שוב ולחזור למסמך זה כדי להמשיך. | apps/remix/app/components/general/document-signing/document-signing-auth-set-password.tsx |
| 550 | Signing Window Expired | חלון הזמן לחתימה פג | apps/remix/app/components/embed/embed-recipient-expired.tsx |
| 551 | Signing window expired for "{0}" on "{1}" | חלון הזמן לחתימה של "{0}" על "{1}" פג | packages/lib/jobs/definitions/emails/send-owner-recipient-expired-email.handler.ts |
| 552 | Signing window expired for "{displayName}" on "{documentName}" | חלון הזמן לחתימה של "{displayName}" על "{documentName}" פג | packages/email/template-components/template-recipient-expired.tsx |
| 553 | Signing window expired for {0} | חלון הזמן לחתימה של {0} פג | packages/lib/utils/document-audit-logs.ts, packages/lib/utils/document-audit-logs.ts |
| 554 | Signing you in... | מתבצעת התחברות... | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 555 | Something went wrong | משהו השתבש | apps/remix/app/components/general/direct-template/direct-template-signing-auth-page.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-page.tsx (+1) |
| 556 | Something went wrong while applying your signature. Please retry. | משהו השתבש בהחלת החתימה שלכם. נא לנסות שוב. | apps/remix/app/components/general/document-signing/csc-recipient-signing-in-progress-page.tsx, apps/remix/app/components/general/envelope-signing/envelope-signing-csc-status.tsx |
| 557 | Something went wrong while loading the document. | משהו השתבש בטעינת המסמך. | apps/remix/app/components/general/pdf-viewer/pdf-viewer-states.tsx |
| 558 | Something went wrong while loading your passkeys. | משהו השתבש בטעינת מפתחות הגישה שלכם. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 559 | Something went wrong while preparing the remote signature. Please try again. | משהו השתבש בהכנת החתימה המרוחקת. נא לנסות שוב. | apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx |
| 560 | Something went wrong while rendering the document, please try again or contact our support. | משהו השתבש בהצגת המסמך. נא לנסות שוב או לפנות לתמיכה. | packages/lib/constants/pdf-viewer-i18n.ts |
| 561 | Something went wrong while rendering the document, some fields may be missing or corrupted. | משהו השתבש בהצגת המסמך, וייתכן שחלק מהשדות חסרים או פגומים. | packages/lib/constants/pdf-viewer-i18n.ts, packages/lib/constants/pdf-viewer-i18n.ts |
| 562 | Something went wrong while signing you in. Please try again. | משהו השתבש בהתחברות. נא לנסות שוב. | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 563 | Something went wrong. Close this window and try again. | משהו השתבש. נא לסגור חלון זה ולנסות שוב. | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 564 | Source code | קוד מקור | apps/remix/app/components/general/source-code-footer.tsx |
| 565 | Starting sign in... | ההתחברות מתחילה... | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 566 | Status | סטטוס | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 567 | Storage access was denied, so we cannot keep you signed in inside this embed. Please try again. | הגישה לאחסון נחסמה, ולכן לא ניתן לשמור על החיבור שלכם בתוך ההטמעה. נא לנסות שוב. | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 568 | Successfully created: {successCount} | נוצרו בהצלחה: {successCount} | packages/email/templates/bulk-send-complete.tsx |
| 569 | Summary: | סיכום: | packages/email/templates/bulk-send-complete.tsx |
| 570 | System auto inserted fields | שדות שהוזנו אוטומטית על ידי המערכת | [Audit log format] packages/lib/utils/document-audit-logs.ts, packages/lib/utils/document-audit-logs.ts, packages/lib/utils/document-audit-logs.ts |
| 571 | System Requirements | דרישות מערכת | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 572 | Team email removed | כתובת הדוא״ל של הצוות הוסרה | packages/email/templates/team-email-removed.tsx |
| 573 | Team email removed for {teamName} on Documenso | כתובת הדוא״ל של הצוות {teamName} הוסרה | packages/email/templates/team-email-removed.tsx |
| 574 | Text | טקסט | apps/remix/app/components/general/document-signing/document-signing-text-field.tsx, apps/remix/app/components/general/document-signing/document-signing-text-field.tsx, packages/lib/utils/fields.ts |
| 575 | Text is required | יש להזין טקסט | apps/remix/app/components/dialogs/sign-field-text-dialog.tsx |
| 576 | Thank you for completing the signing process. | תודה שהשלמתם את תהליך החתימה. | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 577 | Thank you for letting us know, we have flagged this sender for review. If you have any concerns please feel free to reach out to our &lt;0&gt;support team&lt;/0&gt;. | תודה על הדיווח. סימנו את השולח לבדיקה. בכל שאלה או חשש ניתן לפנות אל &lt;0&gt;צוות התמיכה&lt;/0&gt; שלנו. | apps/remix/app/routes/_recipient+/report.$token.tsx |
| 578 | Thank you for using Documenso to perform your electronic document signing. The purpose of this disclosure is to inform you about the process, legality, and your rights regarding the use of electronic signatures on our platform. By opting to use an electronic signature, you are agreeing to the terms and conditions outlined below. | תודה שבחרתם בשירות החתימה האלקטרונית שלנו. מטרת הודעה זו היא ליידע אתכם על התהליך, על תוקפו המשפטי ועל זכויותיכם בנוגע לשימוש בחתימות אלקטרוניות בפלטפורמה שלנו. בבחירה בחתימה אלקטרונית, הנכם מסכימים לתנאים המפורטים להלן. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 579 | That's okay, it happens! Click the button below to reset your password. | זה בסדר, זה קורה! לחצו על הכפתור שלמטה כדי לאפס את הסיסמה. | packages/email/template-components/template-forgot-password.tsx |
| 580 | The document has been successfully rejected. | המסמך נדחה בהצלחה. | apps/remix/app/components/general/document-signing/document-signing-reject-dialog.tsx |
| 581 | The document owner has been notified of this rejection. No further action is required from you at this time. The document owner may contact you with any questions regarding this rejection. | בעלי המסמך קיבלו הודעה על הדחייה. אין צורך בפעולה נוספת מצדכם בשלב זה. ייתכן שבעלי המסמך ייצרו איתכם קשר בשאלות בנוגע לדחייה. | packages/email/template-components/template-document-rejection-confirmed.tsx |
| 582 | The document owner has been notified of your decision. They may contact you with further instructions if necessary. | בעלי המסמך קיבלו הודעה על החלטתכם, וייתכן שייצרו איתכם קשר עם הנחיות נוספות במידת הצורך. | apps/remix/app/components/embed/embed-document-rejected.tsx, apps/remix/app/routes/_recipient+/sign.$token+/rejected.tsx |
| 583 | The document ownership was delegated to {0} on behalf of {1} | הבעלות על המסמך הועברה אל {0} בשם {1} | [Audit log format] packages/lib/utils/document-audit-logs.ts |
| 584 | The document was rejected externally by {onBehalfOf} on behalf of {user} | המסמך נדחה באופן חיצוני על ידי {onBehalfOf} בשם {user} | packages/lib/utils/document-audit-logs.ts |
| 585 | The document was rejected externally by {onBehalfOf} on behalf of the recipient | המסמך נדחה באופן חיצוני על ידי {onBehalfOf} בשם הנמען | packages/lib/utils/document-audit-logs.ts, packages/lib/utils/document-audit-logs.ts |
| 586 | The document was rejected externally on behalf of {user} | המסמך נדחה באופן חיצוני בשם {user} | packages/lib/utils/document-audit-logs.ts |
| 587 | The document was rejected externally on behalf of the recipient | המסמך נדחה באופן חיצוני בשם הנמען | packages/lib/utils/document-audit-logs.ts |
| 588 | The following errors occurred: | אירעו השגיאות הבאות: | packages/email/templates/bulk-send-complete.tsx |
| 589 | The following organisation has been deleted by an administrator. You and your members will no longer be able to access this organisation, its teams, or its associated data. | הארגון הבא נמחק על ידי מנהל מערכת. לכם ולחברי הארגון לא תהיה עוד גישה לארגון זה, לצוותים שלו או לנתונים הקשורים אליו. | packages/email/templates/organisation-delete.tsx |
| 590 | The following organisation has been deleted. You and your members will no longer be able to access this organisation, its teams, or its associated data. | הארגון הבא נמחק. לכם ולחברי הארגון לא תהיה עוד גישה לארגון זה, לצוותים שלו או לנתונים הקשורים אליו. | packages/email/templates/organisation-delete.tsx |
| 591 | The following team has been deleted. You will no longer be able to access this team and its documents | הצוות הבא נמחק. לא תהיה לכם עוד גישה לצוות זה ולמסמכים שלו | packages/email/templates/team-delete.tsx |
| 592 | The image could not be loaded. Please try again. | לא ניתן היה לטעון את התמונה. נא לנסות שוב. | packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 593 | The image must be smaller than 5MB. | גודל התמונה חייב להיות קטן מ-5MB. | packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 594 | The page you are looking for was moved, removed, renamed or might never have existed. | הדף שחיפשתם הועבר, הוסר, שונה שמו או שמעולם לא היה קיים. | apps/remix/app/components/general/generic-error-layout.tsx |
| 595 | The reason provided for deletion is the following: | סיבת המחיקה שצוינה היא: | packages/email/template-components/template-document-super-delete.tsx |
| 596 | The signing deadline for this document has passed. Please contact the document owner if you need a new copy to sign. | המועד האחרון לחתימה על מסמך זה חלף. אם נדרש עותק חדש לחתימה, נא לפנות לבעלי המסמך. | apps/remix/app/routes/_recipient+/sign.$token+/expired.tsx |
| 597 | The signing provider did not respond in time. Please retry. | ספק החתימה לא הגיב בזמן. נא לנסות שוב. | apps/remix/app/components/general/document-signing/csc-recipient-signing-in-progress-page.tsx, apps/remix/app/components/general/envelope-signing/envelope-signing-csc-status.tsx |
| 598 | The signing window for "{recipientName}" on document "{documentName}" has expired. | חלון הזמן לחתימה של "{recipientName}" על המסמך "{documentName}" פג. | packages/email/templates/recipient-expired.tsx |
| 599 | The signing window for {displayName} on document "{documentName}" has expired. You can resend the document to extend their deadline or cancel the document. | חלון הזמן לחתימה של {displayName} על המסמך "{documentName}" פג. באפשרותכם לשלוח את המסמך מחדש כדי להאריך את המועד, או לבטל את המסמך. | packages/email/template-components/template-recipient-expired.tsx |
| 600 | The team email &lt;0&gt;{teamEmail}&lt;/0&gt; has been removed from the following team | כתובת הדוא״ל של הצוות &lt;0&gt;{teamEmail}&lt;/0&gt; הוסרה מהצוות הבא | packages/email/templates/team-email-removed.tsx |
| 601 | There is no action required on your side. If you believe this was a mistake, please contact the document sender. | אין צורך בפעולה מצדכם. אם לדעתכם מדובר בטעות, נא לפנות לשולח המסמך. | packages/email/template-components/template-recipient-removed-by-admin.tsx |
| 602 | There is no action required on your side. If you believe this was a mistake, please contact your administrator. | אין צורך בפעולה מצדכם. אם לדעתכם מדובר בטעות, נא לפנות למנהל המערכת. | packages/email/template-components/template-recipient-removed-by-admin.tsx |
| 603 | There was an issue rendering some fields, please review the fields and try again. | אירעה בעיה בהצגת חלק מהשדות. נא לבדוק את השדות ולנסות שוב. | packages/lib/constants/pdf-viewer-i18n.ts |
| 604 | This direct link template cannot be used because one or more signers do not have a signature field assigned. Please contact the sender to update the template. | לא ניתן להשתמש בתבנית קישור ישיר זו, משום שלאחד החותמים או יותר לא הוקצה שדה חתימה. נא לפנות לשולח לעדכון התבנית. | apps/remix/app/components/general/direct-template/direct-template-invalid-page.tsx |
| 605 | This document can not be recovered, if you would like to dispute the reason for future documents please contact support. | לא ניתן לשחזר מסמך זה. אם ברצונכם לערער על הסיבה לגבי מסמכים עתידיים, נא לפנות לתמיכה. | packages/email/template-components/template-document-super-delete.tsx |
| 606 | This document has been cancelled by the owner and is no longer available for others to sign. | מסמך זה בוטל על ידי הבעלים ואינו זמין עוד לחתימה. | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 607 | This document has been cancelled by the owner. | מסמך זה בוטל על ידי הבעלים. | apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx, apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx |
| 608 | This document is available in your Documenso account. You can view more details, recipients, and audit logs there. | מסמך זה זמין בחשבון שלכם. שם ניתן לצפות בפרטים נוספים, בנמענים וביומני הביקורת. | apps/remix/app/components/general/document/document-certificate-qr-view.tsx |
| 609 | This document is no longer available to sign because the account that sent it has been disabled, likely due to spam or abuse. | מסמך זה אינו זמין עוד לחתימה, משום שהחשבון ששלח אותו הושבת, ככל הנראה בשל דואר זבל או שימוש לרעה. | apps/remix/app/components/embed/embed-sender-disabled.tsx, apps/remix/app/components/general/document-signing/document-signing-sender-disabled-page.tsx |
| 610 | This document requires a qualified electronic signature. Sign in with your signing provider to continue. | מסמך זה מחייב חתימה אלקטרונית מאושרת. יש להתחבר באמצעות ספק החתימה כדי להמשיך. | apps/remix/app/components/embed/embed-csc-authentication-required.tsx |
| 611 | This document was already signed and no further action was taken. | מסמך זה כבר נחתם, ולא בוצעה פעולה נוספת. | apps/remix/app/components/general/envelope-signing/envelope-signing-complete-dialog.tsx |
| 612 | This document was sent using &lt;0&gt;Documenso&lt;/0&gt;. | מסמך זה נשלח באמצעות &lt;0&gt;מערכת חתימה בקוד פתוח&lt;/0&gt;. | packages/email/template-components/template-footer.tsx |
| 613 | This email confirms that you have rejected the document &lt;0&gt;"{documentName}"&lt;/0&gt; sent by {documentOwnerName}. | הודעה זו מאשרת שדחיתם את המסמך &lt;0&gt;"{documentName}"&lt;/0&gt; שנשלח על ידי {documentOwnerName}. | packages/email/template-components/template-document-rejection-confirmed.tsx |
| 614 | This feature is not available on your current plan | אפשרות זו אינה זמינה בתוכנית הנוכחית שלכם | apps/remix/app/components/embed/embed-paywall.tsx |
| 615 | This image is invalid, please upload a valid image file. | התמונה אינה תקינה. נא להעלות קובץ תמונה תקין. | packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 616 | This signing request is missing its details. Close this window and try again. | חסרים פרטים בבקשת החתימה. נא לסגור חלון זה ולנסות שוב. | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 617 | This window must be opened from a Documenso embed. | יש לפתוח חלון זה מתוך הטמעה של המערכת. | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 618 | Time Zone | אזור זמן | apps/remix/app/routes/_internal+/[__htmltopdf]+/audit-log.tsx, packages/lib/server-only/pdf/render-audit-logs.ts |
| 619 | To approve this document, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לאשר מסמך זה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 620 | To approve this document, you need to be logged in. | כדי לאשר מסמך זה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 621 | To approve this field, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לאשר שדה זה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 622 | To approve this field, you need to be logged in. | כדי לאשר שדה זה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 623 | To assist with this document, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לסייע במסמך זה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 624 | To assist with this document, you need to be logged in. | כדי לסייע במסמך זה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 625 | To assist with this field, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לסייע בשדה זה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 626 | To assist with this field, you need to be logged in. | כדי לסייע בשדה זה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 627 | To get started, please set your password by clicking the button below: | כדי להתחיל, נא להגדיר סיסמה בלחיצה על הכפתור שלמטה: | packages/email/template-components/template-admin-user-created.tsx |
| 628 | To mark this document as viewed, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לסמן מסמך זה כנצפה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 629 | To mark this document as viewed, you need to be logged in. | כדי לסמן מסמך זה כנצפה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 630 | To sign this document, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לחתום על מסמך זה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 631 | To sign this document, you need to be logged in. | כדי לחתום על מסמך זה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 632 | To sign this field, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לחתום על שדה זה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 633 | To sign this field, you need to be logged in. | כדי לחתום על שדה זה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 634 | To use our electronic signature service, you must have access to: | כדי להשתמש בשירות החתימה האלקטרונית שלנו, נדרשת לכם גישה אל: | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 635 | To view this document you need to be signed into your account, please sign in to continue. | כדי לצפות במסמך זה יש להתחבר לחשבון. נא להתחבר כדי להמשיך. | apps/remix/app/components/embed/embed-authentication-required.tsx |
| 636 | To view this document, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לצפות במסמך זה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 637 | To view this document, you need to be logged in. | כדי לצפות במסמך זה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 638 | To view this field, you need to be logged in as &lt;0&gt;{0}&lt;/0&gt; | כדי לצפות בשדה זה, יש להתחבר בתור &lt;0&gt;{0}&lt;/0&gt; | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 639 | To view this field, you need to be logged in. | כדי לצפות בשדה זה, יש להתחבר. | apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx |
| 640 | Total rows processed: {totalProcessed} | סה״כ שורות שעובדו: {totalProcessed} | packages/email/templates/bulk-send-complete.tsx |
| 641 | Try again | ניסיון חוזר | apps/remix/app/components/embed/embed-csc-authentication-required.tsx, apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx, apps/remix/app/components/general/envelope-signing/envelope-signing-csc-status.tsx |
| 642 | Two-Factor Authentication | אימות דו-שלבי | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/generate-certificate-pdf.ts |
| 643 | Two-Factor Re-Authentication | אימות דו-שלבי חוזר | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/generate-certificate-pdf.ts |
| 644 | Type | הקלדה | [Type signature] packages/ui/primitives/signature-pad/signature-pad.tsx |
| 645 | Type your signature | הקלידו את חתימתכם | packages/ui/primitives/signature-pad/signature-pad-type.tsx |
| 646 | Typed signatures are not allowed. Please draw your signature. | חתימה מוקלדת אינה מותרת. נא לצייר את החתימה. | apps/remix/app/components/general/document-signing/document-signing-signature-field.tsx |
| 647 | Unable to sign document | לא ניתן לחתום על המסמך | apps/remix/app/components/embed/embed-document-signing-page-v1.tsx, apps/remix/app/components/embed/multisign/multi-sign-document-signing-view.tsx |
| 648 | Unable to start the signing flow | לא ניתן להתחיל את תהליך החתימה | apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx |
| 649 | Unable to upload image | לא ניתן להעלות את התמונה | packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 650 | Unauthorized | אין הרשאה | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-password.tsx |
| 651 | Undo | ביטול פעולה | packages/ui/primitives/signature-pad/signature-pad-draw.tsx, packages/ui/primitives/signature-pad/signature-pad-draw.tsx |
| 652 | Unknown | לא ידוע | apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx (+6) |
| 653 | Unknown sign in provider. | ספק התחברות לא מוכר. | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 654 | Updating Your Information | עדכון הפרטים שלכם | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 655 | Upload | העלאה | [Upload signature] packages/ui/primitives/signature-pad/signature-pad.tsx |
| 656 | Upload New Image | העלאת תמונה חדשה | packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 657 | Upload Signature | העלאת חתימה | packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 658 | Use your authenticator app to generate a code | יש להשתמש באפליקציית האימות כדי להפיק קוד | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 659 | Use your passkey for authentication | אימות באמצעות מפתח הגישה שלכם | apps/remix/app/components/general/document-signing/document-signing-auth-dialog.tsx |
| 660 | User | משתמש | packages/lib/server-only/pdf/render-audit-logs.ts |
| 661 | User Agent | סוכן משתמש (User Agent) | packages/lib/server-only/pdf/render-audit-logs.ts |
| 662 | Validation failed | האימות נכשל | apps/remix/app/components/dialogs/sign-field-checkbox-dialog.tsx |
| 663 | Verification Code Required | נדרש קוד אימות | packages/email/template-components/template-access-auth-2fa.tsx |
| 664 | Verify & Complete | אימות והשלמה | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 665 | Verify your email, then close this window and try again. | יש לאמת את כתובת הדוא״ל, ואז לסגור חלון זה ולנסות שוב. | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 666 | Verify your team email address | אימות כתובת הדוא״ל של הצוות | packages/email/templates/confirm-team-email.tsx |
| 667 | View | צפייה | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 668 | View | לצפות במסמך | [Recipient role action verb] packages/lib/constants/recipient-roles.ts |
| 669 | View all documents sent to and from this email address | צפייה בכל המסמכים שנשלחו אל כתובת דוא״ל זו וממנה | packages/email/templates/confirm-team-email.tsx |
| 670 | View document | צפייה במסמך | packages/email/templates/document-created-from-direct-template.tsx |
| 671 | View Document | צפייה במסמך | apps/remix/app/components/general/document-signing/document-signing-mobile-widget.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v1.tsx, apps/remix/app/components/general/document-signing/document-signing-page-view-v2.tsx (+4) |
| 672 | View Document to approve | צפייה במסמך לאישור | packages/email/template-components/template-document-invite.tsx |
| 673 | View Document to assist | צפייה במסמך לסיוע | packages/email/template-components/template-document-invite.tsx |
| 674 | View Document to sign | צפייה במסמך לחתימה | packages/email/template-components/template-document-invite.tsx |
| 675 | View next document | צפייה במסמך הבא | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 676 | View plans | צפייה בתוכניות | packages/email/template-components/template-document-self-signed.tsx |
| 677 | Viewed | נצפה | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx, apps/remix/app/routes/_internal+/[__htmltopdf]+/certificate.tsx, packages/lib/server-only/pdf/render-certificate.ts |
| 678 | Viewed | צפה/תה במסמך | [Recipient role actioned] packages/lib/constants/recipient-roles.ts |
| 679 | Viewer | צופה | apps/remix/app/components/general/envelope-signing/envelope-signer-header.tsx |
| 680 | Viewer | צופה | [Recipient role name] packages/lib/constants/recipient-roles.ts |
| 681 | Viewers | צופים | [Recipient role plural name] packages/lib/constants/recipient-roles.ts |
| 682 | Viewing | צופה | [Recipient role progressive verb] packages/lib/constants/recipient-roles.ts |
| 683 | Waiting for others | ממתינים לאחרים | packages/email/template-components/template-document-pending.tsx |
| 684 | Waiting for others to complete signing | ממתינים להשלמת החתימה על ידי האחרים | packages/lib/jobs/definitions/emails/send-document-pending-email.handler.ts |
| 685 | Waiting for others to sign | ממתינים לחתימת האחרים | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 686 | Waiting for Your Turn | ממתינים לתורכם | apps/remix/app/components/embed/embed-document-waiting-for-turn.tsx, apps/remix/app/routes/_recipient+/sign.$token+/waiting.tsx |
| 687 | Want to send slick signing links like this one? &lt;0&gt;Check out Documenso&lt;/0&gt;. | רוצים לשלוח קישורי חתימה כמו זה? &lt;0&gt;למידע נוסף&lt;/0&gt;. | apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx, apps/remix/app/routes/_recipient+/sign.$token+/_index.tsx |
| 688 | Warning: This was sent from a new account ({senderEmail}) | אזהרה: הודעה זו נשלחה מחשבון חדש ({senderEmail}) | packages/email/template-components/template-new-account-warning.tsx |
| 689 | We encountered an unknown error while attempting to request the two-factor authentication code. Please try again later. | אירעה שגיאה לא ידועה בבקשת קוד האימות הדו-שלבי. נא לנסות שוב מאוחר יותר. | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx, apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 690 | We were unable to log you out at this time. | לא ניתן היה לנתק אתכם כעת. | apps/remix/app/components/general/direct-template/direct-template-signing-auth-page.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-account.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-page.tsx |
| 691 | We were unable to report this sender at this time. Please try again later. | לא ניתן היה לדווח על שולח זה כעת. נא לנסות שוב מאוחר יותר. | apps/remix/app/routes/_recipient+/report.$token.tsx |
| 692 | We were unable to start the sign in flow. Close this window and try again. | לא ניתן היה להתחיל את תהליך ההתחברות. נא לסגור חלון זה ולנסות שוב. | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 693 | We were unable to verify your details. Please try again or contact support | לא ניתן היה לאמת את הפרטים שלכם. נא לנסות שוב או לפנות לתמיכה | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-password.tsx |
| 694 | We'll send a 6-digit code to your email | קוד בן 6 ספרות יישלח לכתובת הדוא״ל שלכם | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 695 | We're still waiting for other signers to sign this document.&lt;0/&gt;We'll notify you as soon as it's ready. | אנו עדיין ממתינים לחתימת שאר החותמים על מסמך זה.&lt;0/&gt;נעדכן אתכם ברגע שהמסמך יהיה מוכן. | packages/email/template-components/template-document-pending.tsx |
| 696 | We've changed your password as you asked. You can now sign in with your new password. | שינינו את הסיסמה כפי שביקשתם. כעת ניתן להתחבר עם הסיסמה החדשה. | packages/email/templates/reset-password.tsx |
| 697 | We've noticed API activity on your account that exceeds the fair use limits of your current plan. As a precaution, new API activity has been temporarily paused pending review. | זיהינו בחשבון שלכם פעילות API החורגת ממגבלות השימוש ההוגן של התוכנית הנוכחית. כאמצעי זהירות, פעילות API חדשה הושהתה זמנית עד לבדיקה. | packages/email/templates/organisation-limit-alert.tsx |
| 698 | We've noticed document activity on your account that exceeds the fair use limits of your current plan. As a precaution, new document activity has been temporarily paused pending review. | זיהינו בחשבון שלכם פעילות מסמכים החורגת ממגבלות השימוש ההוגן של התוכנית הנוכחית. כאמצעי זהירות, פעילות מסמכים חדשה הושהתה זמנית עד לבדיקה. | packages/email/templates/organisation-limit-alert.tsx |
| 699 | We've noticed email sending activity on your account that exceeds the fair use limits of your current plan. As a precaution, new email activity has been temporarily paused pending review. | זיהינו בחשבון שלכם פעילות שליחת דוא״ל החורגת ממגבלות השימוש ההוגן של התוכנית הנוכחית. כאמצעי זהירות, שליחת דוא״ל חדשה הושהתה זמנית עד לבדיקה. | packages/email/templates/organisation-limit-alert.tsx |
| 700 | We've sent a 6-digit verification code to your email. Please enter it below to complete the document. | שלחנו קוד אימות בן 6 ספרות לכתובת הדוא״ל שלכם. נא להזין אותו למטה כדי להשלים את המסמך. | apps/remix/app/components/general/document-signing/access-auth-2fa-form.tsx |
| 701 | We've updated the usage limits for your organisation. | עדכנו את מגבלות השימוש של הארגון שלכם. | packages/email/templates/organisation-limits-updated.tsx |
| 702 | Welcome | ברוכים הבאים | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 703 | Welcome to Documenso | ברוכים הבאים | packages/lib/jobs/definitions/emails/send-admin-user-created-email.handler.ts |
| 704 | Welcome to Documenso! | ברוכים הבאים! | packages/email/template-components/template-admin-user-created.tsx, packages/email/template-components/template-confirmation-email.tsx |
| 705 | Were you trying to edit this document instead? | האם התכוונתם לערוך את המסמך? | apps/remix/app/routes/_recipient+/sign.$token+/waiting.tsx |
| 706 | When you sign a document, we can automatically fill in and sign the following fields using information that has already been provided. You can also manually sign or remove any automatically signed fields afterwards if you desire. | בעת החתימה על מסמך, נוכל למלא ולחתום באופן אוטומטי על השדות הבאים באמצעות מידע שכבר נמסר. לאחר מכן תוכלו, אם תרצו, לחתום ידנית על שדות שנחתמו אוטומטית או להסיר אותם. | apps/remix/app/components/general/document-signing/document-signing-auto-sign.tsx |
| 707 | When you use our platform to affix your electronic signature to documents, you are consenting to do so under the Electronic Signatures in Global and National Commerce Act (E-Sign Act) and other applicable laws. This action indicates your agreement to use electronic means to sign documents and receive notifications. | בשימוש בפלטפורמה שלנו להוספת החתימה האלקטרונית שלכם למסמכים, הנכם מסכימים לעשות זאת בהתאם לחוק החתימות האלקטרוניות בסחר העולמי והלאומי (E-Sign Act) ולדינים החלים האחרים. פעולה זו מעידה על הסכמתכם להשתמש באמצעים אלקטרוניים לחתימה על מסמכים ולקבלת הודעות. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 708 | Withdrawing Consent | ביטול ההסכמה | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 709 | You | אתם | packages/lib/utils/document-audit-logs.ts |
| 710 | You added a field | הוספתם שדה | packages/lib/utils/document-audit-logs.ts |
| 711 | You added a recipient | הוספתם נמען | packages/lib/utils/document-audit-logs.ts |
| 712 | You approved the document | אישרתם את המסמך | packages/lib/utils/document-audit-logs.ts |
| 713 | You are about to complete approving the following document | אתם עומדים להשלים את אישור המסמך הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 714 | You are about to complete assisting the following document | אתם עומדים להשלים את הסיוע במסמך הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 715 | You are about to complete signing the following document | אתם עומדים להשלים את החתימה על המסמך הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 716 | You are about to complete viewing the following document | אתם עומדים להשלים את הצפייה במסמך הבא | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 717 | You are currently signed in as &lt;0&gt;{signedInAs}&lt;/0&gt;. Signing in below will switch accounts. | אתם מחוברים כעת בתור &lt;0&gt;{signedInAs}&lt;/0&gt;. התחברות למטה תחליף את החשבון. | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 718 | You authenticated with the signing provider | ביצעתם אימות מול ספק החתימה | packages/lib/utils/document-audit-logs.ts |
| 719 | You authorised the remote signature | אישרתם את החתימה המרוחקת | packages/lib/utils/document-audit-logs.ts |
| 720 | You can also copy and paste this link into your browser: {confirmationLink} (link expires in 1 hour) | ניתן גם להעתיק את הקישור הבא ולהדביק אותו בדפדפן: {confirmationLink} (תוקף הקישור יפוג בעוד שעה) | packages/email/template-components/template-confirmation-email.tsx |
| 721 | You can also copy and paste this link into your browser: {resetPasswordLink} (link expires in 24 hours) | ניתן גם להעתיק את הקישור הבא ולהדביק אותו בדפדפן: {resetPasswordLink} (תוקף הקישור יפוג בעוד 24 שעות) | packages/email/template-components/template-admin-user-created.tsx |
| 722 | You can close this window. | ניתן לסגור חלון זה. | apps/remix/app/routes/embed+/auth+/complete.tsx |
| 723 | You can revoke access at any time in your team settings on Documenso &lt;0&gt;here&lt;/0&gt;. | ניתן לבטל את הגישה בכל עת בהגדרות הצוות &lt;0&gt;כאן&lt;/0&gt;. | packages/email/templates/confirm-team-email.tsx |
| 724 | You can view the created documents in your dashboard under the "Documents created from template" section. | ניתן לצפות במסמכים שנוצרו בלוח הבקרה, בקטע "מסמכים שנוצרו מתבנית". | packages/email/templates/bulk-send-complete.tsx |
| 725 | You can view the document and its status by clicking the button below. | ניתן לצפות במסמך ובסטטוס שלו בלחיצה על הכפתור שלמטה. | packages/email/template-components/template-document-rejected.tsx |
| 726 | You cancelled the document | ביטלתם את המסמך | packages/lib/utils/document-audit-logs.ts |
| 727 | You CC'd the document | קיבלתם עותק של המסמך | packages/lib/utils/document-audit-logs.ts |
| 728 | You completed your task | השלמתם את המשימה שלכם | packages/lib/utils/document-audit-logs.ts |
| 729 | You created an envelope item with title {0} | יצרתם פריט מעטפה בשם {0} | packages/lib/utils/document-audit-logs.ts |
| 730 | You created the document | יצרתם את המסמך | packages/lib/utils/document-audit-logs.ts |
| 731 | You deleted an envelope item with title {0} | מחקתם פריט מעטפה בשם {0} | packages/lib/utils/document-audit-logs.ts |
| 732 | You deleted the document | מחקתם את המסמך | packages/lib/utils/document-audit-logs.ts |
| 733 | You don't need to sign it anymore. | אין עוד צורך לחתום עליו. | packages/email/template-components/template-document-cancel.tsx |
| 734 | You failed to validate a 2FA token for the document | אימות קוד ה-2FA שלכם למסמך נכשל | packages/lib/utils/document-audit-logs.ts |
| 735 | You have been invited to join the following organisation | הוזמנתם להצטרף לארגון הבא | packages/email/templates/organisation-invite.tsx |
| 736 | You have been removed from a document | הוסרתם ממסמך | packages/email/template-components/template-recipient-removed-by-admin.tsx, packages/lib/jobs/definitions/emails/send-admin-recipient-removed-emails.handler.ts, packages/lib/jobs/definitions/emails/send-recipient-removed-email.handler.ts |
| 737 | You have been removed from the document "{documentName}" by an administrator, typically at the request of the document sender. | הוסרתם מהמסמך "{documentName}" על ידי מנהל מערכת, בדרך כלל לבקשת שולח המסמך. | packages/email/template-components/template-recipient-removed-by-admin.tsx |
| 738 | You have been removed from the document "{documentName}" by an administrator. | הוסרתם מהמסמך "{documentName}" על ידי מנהל מערכת. | packages/email/templates/recipient-removed-by-admin.tsx |
| 739 | You have been requested to sign the following documents. Review each document carefully and complete the signing process. | התבקשתם לחתום על המסמכים הבאים. נא לעיין בכל מסמך בקפידה ולהשלים את תהליך החתימה. | apps/remix/app/components/embed/multisign/multi-sign-document-list.tsx |
| 740 | You have initiated the document {0} that requires you to {recipientActionVerb} it. | יזמתם את המסמך {0}, ויש {recipientActionVerb}. | packages/lib/jobs/definitions/emails/send-signing-email.handler.ts, packages/lib/server-only/document/resend-document.ts |
| 741 | You have rejected the document '{documentName}' | דחיתם את המסמך '{documentName}' | packages/email/templates/document-rejection-confirmed.tsx |
| 742 | You have rejected this document | דחיתם מסמך זה | apps/remix/app/components/embed/embed-document-rejected.tsx, apps/remix/app/routes/_recipient+/sign.$token+/rejected.tsx |
| 743 | You have signed “{documentName}” | חתמתם על „{documentName}” | packages/email/template-components/template-document-self-signed.tsx |
| 744 | You have the right to withdraw your consent to use electronic signatures at any time before completing the signing process. To withdraw your consent, please contact the sender of the document. In failing to contact the sender you may reach out to &lt;0&gt;{SUPPORT_EMAIL}&lt;/0&gt; for assistance. Be aware that withdrawing consent may delay or halt the completion of the related transaction or service. | באפשרותכם לבטל את הסכמתכם לשימוש בחתימות אלקטרוניות בכל עת לפני השלמת תהליך החתימה. לביטול ההסכמה, נא לפנות לשולח המסמך. אם לא ניתן ליצור קשר עם השולח, ניתן לפנות לקבלת סיוע אל &lt;0&gt;{SUPPORT_EMAIL}&lt;/0&gt;. לתשומת לבכם, ביטול ההסכמה עלול לעכב או לעצור את השלמת העסקה או השירות הקשורים. | apps/remix/app/routes/_unauthenticated+/articles.signature-disclosure.tsx |
| 745 | You moved the document to team | העברתם את המסמך לצוות | packages/lib/utils/document-audit-logs.ts |
| 746 | You need to be logged in as &lt;0&gt;{email}&lt;/0&gt; to view this page. | כדי לצפות בדף זה יש להתחבר בתור &lt;0&gt;{email}&lt;/0&gt;. | apps/remix/app/components/general/document-signing/document-signing-auth-page.tsx |
| 747 | You need to be logged in to view this page. | כדי לצפות בדף זה יש להתחבר. | apps/remix/app/components/general/direct-template/direct-template-signing-auth-page.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-page.tsx |
| 748 | You need to setup 2FA to approve this document. | כדי לאשר מסמך זה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 749 | You need to setup 2FA to approve this field. | כדי לאשר שדה זה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 750 | You need to setup 2FA to assist with this document. | כדי לסייע במסמך זה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 751 | You need to setup 2FA to assist with this field. | כדי לסייע בשדה זה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 752 | You need to setup 2FA to mark this document as viewed. | כדי לסמן מסמך זה כנצפה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 753 | You need to setup 2FA to sign this document. | כדי לחתום על מסמך זה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 754 | You need to setup 2FA to sign this field. | כדי לחתום על שדה זה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 755 | You need to setup 2FA to view this document. | כדי לצפות במסמך זה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 756 | You need to setup 2FA to view this field. | כדי לצפות בשדה זה יש להגדיר 2FA. | apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-2fa.tsx |
| 757 | You need to setup a passkey to approve this document. | כדי לאשר מסמך זה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 758 | You need to setup a passkey to approve this field. | כדי לאשר שדה זה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 759 | You need to setup a passkey to assist with this document. | כדי לסייע במסמך זה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 760 | You need to setup a passkey to assist with this field. | כדי לסייע בשדה זה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 761 | You need to setup a passkey to mark this document as viewed. | כדי לסמן מסמך זה כנצפה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 762 | You need to setup a passkey to sign this document. | כדי לחתום על מסמך זה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 763 | You need to setup a passkey to sign this field. | כדי לחתום על שדה זה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 764 | You need to setup a passkey to view this document. | כדי לצפות במסמך זה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 765 | You need to setup a passkey to view this field. | כדי לצפות בשדה זה יש להגדיר מפתח גישה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 766 | You opened the document | פתחתם את המסמך | packages/lib/utils/document-audit-logs.ts |
| 767 | You prefilled a field | מילאתם שדה מראש | packages/lib/utils/document-audit-logs.ts |
| 768 | You rejected the document | דחיתם את המסמך | packages/lib/utils/document-audit-logs.ts |
| 769 | You removed a field | הסרתם שדה | packages/lib/utils/document-audit-logs.ts |
| 770 | You removed a recipient | הסרתם נמען | packages/lib/utils/document-audit-logs.ts |
| 771 | You removed a recipient as an administrator | הסרתם נמען בהרשאת מנהל מערכת | packages/lib/utils/document-audit-logs.ts |
| 772 | You replaced the PDF for envelope item {0} | החלפתם את קובץ ה-PDF של פריט המעטפה {0} | packages/lib/utils/document-audit-logs.ts |
| 773 | You requested a 2FA token for the document | ביקשתם קוד 2FA למסמך | packages/lib/utils/document-audit-logs.ts |
| 774 | You requested a remote signature | ביקשתם חתימה מרוחקת | packages/lib/utils/document-audit-logs.ts |
| 775 | You resent an email to {0} | שלחתם שוב דוא״ל אל {0} | packages/lib/utils/document-audit-logs.ts |
| 776 | You sent an email to {0} | שלחתם דוא״ל אל {0} | packages/lib/utils/document-audit-logs.ts |
| 777 | You sent the document | שלחתם את המסמך | packages/lib/utils/document-audit-logs.ts |
| 778 | You signed a field | חתמתם על שדה | packages/lib/utils/document-audit-logs.ts |
| 779 | You signed the document | חתמתם על המסמך | packages/lib/utils/document-audit-logs.ts |
| 780 | You unsigned a field | ביטלתם חתימה על שדה | packages/lib/utils/document-audit-logs.ts |
| 781 | You updated a field | עדכנתם שדה | packages/lib/utils/document-audit-logs.ts |
| 782 | You updated a recipient | עדכנתם נמען | packages/lib/utils/document-audit-logs.ts |
| 783 | You updated an envelope item | עדכנתם פריט מעטפה | packages/lib/utils/document-audit-logs.ts |
| 784 | You updated the document | עדכנתם את המסמך | packages/lib/utils/document-audit-logs.ts |
| 785 | You updated the document access auth requirements | עדכנתם את דרישות האימות לגישה למסמך | packages/lib/utils/document-audit-logs.ts |
| 786 | You updated the document external ID | עדכנתם את המזהה החיצוני של המסמך | packages/lib/utils/document-audit-logs.ts |
| 787 | You updated the document signing auth requirements | עדכנתם את דרישות האימות לחתימה על המסמך | packages/lib/utils/document-audit-logs.ts |
| 788 | You updated the document title | עדכנתם את כותרת המסמך | packages/lib/utils/document-audit-logs.ts |
| 789 | You updated the document visibility | עדכנתם את נראות המסמך | packages/lib/utils/document-audit-logs.ts |
| 790 | You validated a 2FA token for the document | אימתתם קוד 2FA למסמך | packages/lib/utils/document-audit-logs.ts |
| 791 | You viewed the document | צפיתם במסמך | packages/lib/utils/document-audit-logs.ts, packages/lib/utils/document-audit-logs.ts |
| 792 | You will be redirected to sign in, then returned here. | תועברו להתחברות, ולאחר מכן תוחזרו לכאן. | apps/remix/app/routes/embed+/auth+/popup.tsx |
| 793 | You will receive an email copy of the signed document once everyone has signed. | עותק של המסמך החתום יישלח אליכם בדוא״ל לאחר שכל הנמענים יחתמו. | apps/remix/app/routes/_recipient+/sign.$token+/complete.tsx |
| 794 | You won't be able to sign in or send documents while it is disabled. | כל עוד החשבון מושבת, לא ניתן להתחבר או לשלוח מסמכים. | packages/email/template-components/template-account-disabled.tsx |
| 795 | Your account does not have a password and password sign in is disabled for this instance. Please contact the document sender to use a different authentication method. | לחשבון שלכם לא הוגדרה סיסמה, וההתחברות באמצעות סיסמה מושבתת במערכת זו. נא לפנות לשולח המסמך כדי להשתמש בשיטת אימות אחרת. | apps/remix/app/components/general/document-signing/document-signing-auth-set-password.tsx |
| 796 | Your account has been disabled | החשבון שלכם הושבת | packages/email/template-components/template-account-disabled.tsx |
| 797 | Your browser blocked the sign in window. Allow popups for this site and try again. | הדפדפן חסם את חלון ההתחברות. יש לאפשר חלונות קופצים לאתר זה ולנסות שוב. | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 798 | Your browser does not support passkeys, which is required to approve this document. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לאישור מסמך זה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 799 | Your browser does not support passkeys, which is required to approve this field. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לאישור שדה זה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 800 | Your browser does not support passkeys, which is required to assist with this document. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לסיוע במסמך זה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 801 | Your browser does not support passkeys, which is required to assist with this field. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לסיוע בשדה זה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 802 | Your browser does not support passkeys, which is required to mark this document as viewed. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לסימון מסמך זה כנצפה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 803 | Your browser does not support passkeys, which is required to sign this document. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לחתימה על מסמך זה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 804 | Your browser does not support passkeys, which is required to sign this field. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לחתימה על שדה זה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 805 | Your browser does not support passkeys, which is required to view this document. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לצפייה במסמך זה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 806 | Your browser does not support passkeys, which is required to view this field. | הדפדפן שלכם אינו תומך במפתחות גישה, הנדרשים לצפייה בשדה זה. | apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx, apps/remix/app/components/general/document-signing/document-signing-auth-passkey.tsx |
| 807 | Your browser is blocking the cookies needed to keep you signed in inside this embed. Open this document in a new tab instead. | הדפדפן שלכם חוסם את קובצי ה-Cookie הנדרשים כדי לשמור על החיבור בתוך ההטמעה. נא לפתוח מסמך זה בלשונית חדשה. | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 808 | Your browser needs permission to keep you signed in inside this embed. Press Continue and allow access when Safari asks. | הדפדפן זקוק להרשאה כדי לשמור על החיבור שלכם בתוך ההטמעה. לחצו על "המשך" ואשרו את הגישה כש-Safari יבקש זאת. | apps/remix/app/components/embed/embed-popup-auth.tsx |
| 809 | Your bulk send operation for template "{templateName}" has completed. | השליחה המרובה עבור התבנית "{templateName}" הושלמה. | packages/email/templates/bulk-send-complete.tsx |
| 810 | Your Documenso account has been disabled | החשבון שלכם הושבת | packages/email/templates/account-disabled.tsx, packages/lib/jobs/definitions/emails/send-account-disabled-email.handler.ts |
| 811 | Your document has been deleted by an admin! | המסמך שלכם נמחק על ידי מנהל מערכת! | packages/email/template-components/template-document-super-delete.tsx |
| 812 | Your Email | כתובת הדוא״ל שלכם | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 813 | Your Name | השם שלכם | apps/remix/app/components/general/document-signing/document-signing-complete-dialog.tsx |
| 814 | Your organisation has been deleted | הארגון שלכם נמחק | packages/email/templates/organisation-delete.tsx, packages/email/templates/organisation-delete.tsx |
| 815 | Your organisation is generating API requests faster than normal, so some requests are being temporarily throttled. | הארגון שלכם מבצע בקשות API בקצב גבוה מהרגיל, ולכן חלק מהבקשות מוגבלות זמנית. | packages/email/templates/organisation-limit-alert.tsx |
| 816 | Your organisation is generating documents faster than normal, so some requests are being temporarily throttled. | הארגון שלכם יוצר מסמכים בקצב גבוה מהרגיל, ולכן חלק מהבקשות מוגבלות זמנית. | packages/email/templates/organisation-limit-alert.tsx |
| 817 | Your organisation is generating emails faster than normal, so some requests are being temporarily throttled. | הארגון שלכם שולח הודעות דוא״ל בקצב גבוה מהרגיל, ולכן חלק מהבקשות מוגבלות זמנית. | packages/email/templates/organisation-limit-alert.tsx |
| 818 | Your organisation is nearing its fair use limits for creating documents on your current plan. Once the limit is reached, new document activity will be temporarily paused. | הארגון שלכם מתקרב למגבלות השימוש ההוגן ליצירת מסמכים בתוכנית הנוכחית. עם ההגעה למגבלה, פעילות מסמכים חדשה תושהה זמנית. | packages/email/templates/organisation-limit-alert.tsx |
| 819 | Your organisation is nearing its fair use limits for making API requests on your current plan. Once the limit is reached, new API activity will be temporarily paused. | הארגון שלכם מתקרב למגבלות השימוש ההוגן לבקשות API בתוכנית הנוכחית. עם ההגעה למגבלה, פעילות API חדשה תושהה זמנית. | packages/email/templates/organisation-limit-alert.tsx |
| 820 | Your organisation is nearing its fair use limits for sending email on your current plan. Once the limit is reached, new email activity will be temporarily paused. | הארגון שלכם מתקרב למגבלות השימוש ההוגן לשליחת דוא״ל בתוכנית הנוכחית. עם ההגעה למגבלה, שליחת דוא״ל חדשה תושהה זמנית. | packages/email/templates/organisation-limit-alert.tsx |
| 821 | Your organisation limits have been updated | מגבלות הארגון שלכם עודכנו | packages/email/templates/organisation-limits-updated.tsx |
| 822 | Your password has been updated. | הסיסמה שלכם עודכנה. | packages/email/template-components/template-reset-password.tsx |
| 823 | Your password was changed | הסיסמה שלכם שונתה | packages/email/templates/reset-password.tsx |
| 824 | Your password was just changed from your account security settings. | הסיסמה שלכם שונתה זה עתה דרך הגדרות האבטחה של החשבון. | packages/email/templates/reset-password.tsx |
| 825 | Your remote signature was applied | החתימה המרוחקת שלכם הוחלה | packages/lib/utils/document-audit-logs.ts |
| 826 | Your signing authorisation expired before the signature could be applied. Please reauthorise to retry. | תוקף הרשאת החתימה שלכם פג לפני שניתן היה להחיל את החתימה. נא לאשר מחדש כדי לנסות שוב. | apps/remix/app/components/general/document-signing/csc-recipient-signing-in-progress-page.tsx, apps/remix/app/components/general/envelope-signing/envelope-signing-csc-status.tsx |
| 827 | Your signing certificate is invalid, expired, or missing a required key. Contact your administrator or signing provider for assistance. | תעודת החתימה שלכם אינה תקינה, פג תוקפה או שחסר בה מפתח נדרש. לסיוע, נא לפנות למנהל המערכת או לספק החתימה. | apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx |
| 828 | Your signing provider authentication failed | האימות שלכם מול ספק החתימה נכשל | packages/lib/utils/document-audit-logs.ts |
| 829 | Your signing provider does not advertise a signing algorithm this document accepts. Contact your administrator or signing provider for assistance. | ספק החתימה שלכם אינו מציע אלגוריתם חתימה שמסמך זה מקבל. לסיוע, נא לפנות למנהל המערכת או לספק החתימה. | apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx |
| 830 | Your signing provider returned no usable credentials for this account. Contact your administrator or signing provider for assistance. | ספק החתימה שלכם לא החזיר אמצעי חתימה שמישים עבור חשבון זה. לסיוע, נא לפנות למנהל המערכת או לספק החתימה. | apps/remix/app/components/general/document-signing/csc-recipient-blocked-page.tsx |
| 831 | Your signing window for this document has expired. Please contact the sender for a new invitation. | חלון הזמן לחתימתכם על מסמך זה פג. נא לפנות לשולח לקבלת הזמנה חדשה. | apps/remix/app/components/embed/embed-recipient-expired.tsx |
| 832 | Your two-factor authentication code | קוד האימות הדו-שלבי שלכם | packages/lib/server-only/2fa/email/send-2fa-token-email.ts |
| 833 | Your verification code is {code} | קוד האימות שלכם הוא {code} | packages/email/templates/access-auth-2fa.tsx |
| 834 | Your verification code: | קוד האימות שלכם: | packages/email/template-components/template-access-auth-2fa.tsx |
| 835 | Zoom in | הגדלה | packages/ui/primitives/signature-pad/signature-pad-upload.tsx, packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
| 836 | Zoom out | הקטנה | packages/ui/primitives/signature-pad/signature-pad-upload.tsx, packages/ui/primitives/signature-pad/signature-pad-upload.tsx |
