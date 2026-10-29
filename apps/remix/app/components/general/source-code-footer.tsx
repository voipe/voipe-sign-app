import { Trans } from '@lingui/react/macro';

/**
 * VoIPe fork: AGPL-3.0 section 13. Every page a recipient (signer) interacts with offers
 * the Corresponding Source of this modified version. See vs/LEGAL.md.
 */
export const SOURCE_CODE_URL = 'https://github.com/voipe/voipe-sign-app';

export const SourceCodeFooter = () => {
  return (
    <footer className="py-4 text-center text-muted-foreground text-xs">
      <a
        href={SOURCE_CODE_URL}
        target="_blank"
        rel="noopener noreferrer"
        className="underline-offset-2 hover:underline"
      >
        <Trans>Source code</Trans>
      </a>
    </footer>
  );
};
