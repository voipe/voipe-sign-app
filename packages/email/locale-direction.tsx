/**
 * VoIPe fork (Track F2c): locale-aware <Html> and <Body> for the email templates.
 *
 * react-email defaults both to `lang="en" dir="ltr"`. These wrappers take the language from
 * the active lingui instance (the document/recipient language passed to `renderEmailWithI18N`)
 * and set `dir="rtl"` for RTL languages such as Hebrew. `Body` repeats `dir`/`lang` on its
 * inner table cell, which survives clients (e.g. Gmail) that strip <html>/<body> attributes.
 */
import { getLanguageDirection } from '@documenso/lib/constants/locales';
import { useLingui } from '@lingui/react';
import type { ComponentPropsWithoutRef } from 'react';
import { Body as ReactEmailBody, Html as ReactEmailHtml } from 'react-email';

const useEmailLocale = (lang?: string, dir?: string) => {
  const { i18n } = useLingui();

  const resolvedLang = lang ?? i18n.locale ?? 'en';

  return {
    lang: resolvedLang,
    dir: dir ?? getLanguageDirection(resolvedLang),
  };
};

export const Html = ({ lang, dir, ...props }: ComponentPropsWithoutRef<typeof ReactEmailHtml>) => {
  const locale = useEmailLocale(lang, dir);

  return <ReactEmailHtml {...props} lang={locale.lang} dir={locale.dir} />;
};

export const Body = ({ lang, dir, ...props }: ComponentPropsWithoutRef<typeof ReactEmailBody>) => {
  const locale = useEmailLocale(lang, dir);

  return <ReactEmailBody {...props} lang={locale.lang} dir={locale.dir} />;
};
