# Client-visible vendor branding (Track F2e, QA-25)

Goal: a signer (client) never sees the upstream vendor name on the signing pages, in the signing emails or in the
sealed PDF's certificate/audit pages. Most of it is controlled by **configuration** (CE branding settings and the
organisation claim flag); the fork neutralises what configuration cannot reach.

## 1. Required configuration (no code change; set during P6.5)

| Where | Setting | Effect |
|---|---|---|
| Admin → Claims (or the organisation's claim) | flag `hidePoweredBy` ("Hide … branding") = on | Hides "This document was sent using …" in every email footer, the "Signing certificate provided by: [logo]" block on the certificate page and the vendor logo at the end of the audit log. **Upstream side effect:** the certificate's QR code (share link) is part of the same block and is hidden too |
| Organisation/Team → Branding | `brandingEnabled` = on, VoIPe logo, Brand website, Company details | Emails show the VoIPe logo instead of the vendor logo, and the company-details block replaces the hard-coded vendor postal address in the email footer. Signing pages show the VoIPe logo |
| Document meta | `language = "he"` | Emails, certificate and audit log are rendered in Hebrew |
| Instance | e-mail sign-up disabled | Hides the "Need to sign documents? Create your account…" promo after signing (it is gated on sign-up being enabled) |

## 2. Neutralised in the fork (code / catalog)

| Location | Before | After |
|---|---|---|
| `_recipient+/sign.$token+/_index.tsx` (document cancelled / no longer available, signer not logged in) | "Want to send slick signing links like this one? Check out Documenso" + link to documenso.com | block removed |
| `packages/lib/translations/en/web.po` (English fallback, client-facing msgids) | 23 strings such as "Sign Document - Documenso" (browser tab title on signing pages), the signature-disclosure page ("Thank you for using Documenso…", "…service provided by Documenso…"), "Welcome to Documenso", "…on Documenso" email subjects/previews | neutral English msgstr overrides (msgids unchanged, so `lingui extract` keeps them) |
| `he/web.po` | — | no Hebrew string contains the vendor name (enforced by `vs/tools/check_po.py`) |
| `packages/email/template-components/template-document-image.tsx` | `alt="Documenso"` on the document illustration (visible when images are blocked) | `alt=""` (decorative) |
| `_recipient+/sign.$token+/complete.tsx` (signer completion page) | "Share" button: tweet "I just signed a document in style with @documenso", share page with vendor OpenGraph card that redirects to documenso.com | button removed |
| `apps/remix/app/components/embed/embed-document-completed.tsx` | signing card falls back to the name "Documenso" | empty name |
| `apps/remix/public/site.webmanifest` | `name`/`short_name` "Documenso" (home-screen shortcut) | "VoIPe Sign" |
| Signing pages | — | footer link "קוד מקור" / "Source code" → https://github.com/voipe/voipe-sign-app (AGPL §13, see `LEGAL.md`) |

## 3. Remaining (not changed; accepted or needs assets/decision)

| Location | What | Why not changed |
|---|---|---|
| `apps/remix/public/favicon*.png`, `favicon.ico`, `apple-touch-icon.png`, `android-chrome-*.png` | upstream icon in the browser tab of the signing page | needs VoIPe icon files (drop-in replacement, same file names) |
| `public/static/logo.png` | vendor logo used by: email header when branding has no logo, certificate/audit-log branding (only when `hidePoweredBy` is off), `account-disabled` and `admin-user-created` emails (hard-coded) | covered by the configuration in §1; the two account emails go to VoIPe staff accounts, not to signers |
| `packages/email/template-components/template-footer.tsx` | hard-coded vendor postal address | only rendered when `brandingEnabled` is off (§1) |
| `packages/email/template-components/template-document-self-signed.tsx` | "Create a free account" / "View plans" (vendor pricing link) | only sent to a sender who signs their own document (staff), never to clients |
| Embed "Powered by [logo]" badge | `embed+` routes only | VoIPe does not embed signing; normal signing pages default to `hidePoweredBy = true` |
| `_share+/share.$slug.tsx` | OpenGraph tags for share links ("I just signed with Documenso!") and a redirect to documenso.com | the signer-side Share button is removed; the remaining entry point is the certificate QR code, which is hidden together with the powered-by block (§1) |
| `apps/remix/app/utils/meta.ts` | default `<title>`/OpenGraph tags | not used on recipient routes (the recipient layout replaces the meta tags); only on staff pages |
| Admin/authenticated UI | various "Documenso" strings | out of scope (staff only); the Hebrew catalog has none |

## QA-25 check

Grep the rendered signing page HTML, a received invite/completed email (HTML source) and `pdftotext` of the sealed
PDF for `documenso` (case-insensitive). Expected: 0 hits with the configuration of §1, except asset file names and
CSS class names (`documenso-branded`, `text-documenso-700`), which are not visible text.
