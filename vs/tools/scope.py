import re
CLIENT_PATTERNS = [
    r'^apps/remix/app/routes/_recipient\+/',
    r'^apps/remix/app/routes/_share\+/',
    r'^apps/remix/app/components/general/document-signing/',
    r'^apps/remix/app/components/general/envelope-signing/',
    r'^apps/remix/app/components/general/direct-template/',
    r'^apps/remix/app/components/general/pdf-viewer/',
    r'^apps/remix/app/components/general/generic-error-layout',
    r'^apps/remix/app/components/general/source-code-footer',
    r'^apps/remix/app/components/general/document/document-certificate-qr-view',
    r'^apps/remix/app/components/dialogs/sign-field-',
    r'^apps/remix/app/components/embed/(?!authoring/)',
    r'^apps/remix/app/routes/embed\+/(_v0\+|auth\+|v1\+/multisign)',
    r'^apps/remix/app/routes/_internal\+/\[__htmltopdf\]\+/',
    r'^apps/remix/app/routes/_unauthenticated\+/articles\.signature-disclosure',
    r'^packages/email/',
    r'^packages/lib/jobs/definitions/emails/',
    r'^packages/lib/jobs/definitions/internal/process-signing-reminder',
    r'^packages/lib/server-only/document/resend-document',
    r'^packages/lib/server-only/2fa/',
    r'^packages/lib/server-only/pdf/',
    r'^packages/lib/utils/document-audit-logs',
    r'^packages/lib/constants/recipient-roles',
    r'^packages/lib/constants/pdf-viewer-i18n',
    r'^packages/lib/utils/fields\.ts',
    r'^packages/ui/primitives/signature-pad/',
    r'^packages/ui/components/document/document-read-only-fields',
    r'^packages/ui/primitives/document-flow/field-content',
    r'^packages/ui/primitives/(dialog|sheet)\.tsx',
]
CLIENT_RE = [re.compile(p) for p in CLIENT_PATTERNS]
def is_client(refs):
    return any(r.search(f) for f in refs for r in CLIENT_RE)
