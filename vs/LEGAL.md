# AGPL-3.0 checklist (VoIPe Sign fork)

Upstream: [documenso/documenso](https://github.com/documenso/documenso), license **AGPL-3.0** (`LICENSE`).
This fork: https://github.com/voipe/voipe-sign-app (public), branch `vs/main` = upstream tag `v2.21.1` + `vs:` commits.

| # | Obligation | How it is met | Check |
|---|---|---|---|
| 1 | Keep copyright and license notices (§4, §5) | `LICENSE`, upstream headers, `README.md` notices and package `license` fields are untouched; fork changes are additive (`vs:` commits) | `git diff v2.21.1..vs/main -- LICENSE` is empty |
| 2 | Mark modified files / state the changes (§5a) | Every change is a small commit prefixed `vs:` with a description; `vs/README.md`, `vs/TRANSLATION.md`, `vs/BRANDING.md` describe them; code comments mark fork-specific blocks ("VoIPe fork") | `git log --oneline v2.21.1..vs/main` |
| 3 | License of the modified work (§5c) | The whole fork remains AGPL-3.0; the image carries `org.opencontainers.image.licenses=AGPL-3.0` | `docker inspect` label |
| 4 | Offer the Corresponding Source to network users (§13) | Signing pages (all `_recipient+` routes: sign, complete, rejected, expired, waiting, direct templates) show a footer link "קוד מקור" / "Source code" → https://github.com/voipe/voipe-sign-app (`apps/remix/app/components/general/source-code-footer.tsx`) | QA: link visible on `/sign/<token>` and the completion page |
| 5 | Source for **every deployed build** | CI (`.github/workflows/vs-build.yml`) builds only from pushed commits of this public repo; each image is tagged with `vs/VERSION` and `sha-<commit>` and labelled `org.opencontainers.image.revision=<commit>` and `org.opencontainers.image.source`. Production pins the image by digest; the commit is resolvable from the label. Do not delete or force-push published commits | record image digest + commit in the deployment log |
| 6 | No additional restrictions (§10) | No extra terms are added to the fork | — |
| 7 | Third-party assets | `apps/remix/public/fonts/noto-sans-hebrew.ttf` — Noto Sans Hebrew, SIL Open Font License 1.1, license text in `apps/remix/public/fonts/noto-sans-hebrew-OFL.txt` (font is unmodified) | file present |
| 8 | Trademarks | Upstream name/logo are not used to brand the VoIPe service on client-facing pages (see `BRANDING.md`); attribution to the upstream project stays in `README.md` and the license | — |
| 9 | Separate programs | The VoIPe gateway is a separate program communicating over the public API; it is not part of this work and is not covered by this repository | — |

Before each production deploy: confirm the deployed image digest was built from a commit that is on `vs/main` in the
public repo, and that the source link on the signing page resolves.
