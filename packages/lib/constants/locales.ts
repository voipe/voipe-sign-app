import { z } from 'zod';

export const SUPPORTED_LANGUAGE_CODES = [
  'de',
  'en',
  'fr',
  'es',
  'it',
  'nl',
  'pl',
  'pt-BR',
  'ja',
  'ko',
  'zh',
  'he',
] as const;

export type SupportedLanguageCodes = (typeof SUPPORTED_LANGUAGE_CODES)[number];

export const APP_I18N_OPTIONS = {
  supportedLangs: SUPPORTED_LANGUAGE_CODES,
  sourceLang: 'en',
  defaultLocale: 'en-US',
} as const;

/**
 * Languages written right-to-left (VoIPe fork: Hebrew).
 */
export const RTL_LANGUAGE_CODES: readonly string[] = ['he'];

export const getLanguageDirection = (lang?: string | null): 'rtl' | 'ltr' =>
  lang && RTL_LANGUAGE_CODES.includes(lang) ? 'rtl' : 'ltr';

export const ZSupportedLanguageCodeSchema = z.enum(SUPPORTED_LANGUAGE_CODES).catch('en');
