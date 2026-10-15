# TestFlight

`.github/workflows/testflight.yml` archives the app on a macOS runner and uploads it to App Store Connect on every push to `main` that changes the app, and on demand (Actions > TestFlight > Run workflow). Apple processes the build, then it appears in the TestFlight app on every tester's iPhone or iPad. No Mac is needed.

Signing is Apple's cloud signing: no certificate or provisioning profile lives in the repo. The archive is built unsigned and `xcodebuild -exportArchive -allowProvisioningUpdates` signs it with the team's cloud-managed distribution certificate through an App Store Connect API key.

The build number is `<run number>.<attempt>` (for example `12.1`), so every upload, re-runs included, is higher than the last. The version is `MARKETING_VERSION` in `project.yml`.

## One-time setup (account holder, in a browser)

1. **Register the bundle ID.** developer.apple.com > Certificates, Identifiers & Profiles > Identifiers > **+** > App IDs > App. Description `Saudi Colors`, Bundle ID **Explicit** `com.alialyami.saudicolors`. No capabilities needed. Continue, Register.
2. **Create the app record.** appstoreconnect.apple.com > Apps > **+** > New App. Platform iOS, name `Saudi Colors` (or any free name), primary language, bundle ID `com.alialyami.saudicolors`, SKU `saudicolors`, User Access Full Access.
3. **Accept the agreements.** App Store Connect > Business: accept any pending agreement, or uploads are refused.
4. **Create the API key.** App Store Connect > Users and Access > Integrations > App Store Connect API > Team Keys > **+**. Name `GitHub TestFlight`, Access **Admin** (cloud signing needs it). Download the `.p8` file; Apple lets you download it only once. Note the **Key ID** next to it and the **Issuer ID** above the list.
5. **Find the Team ID.** developer.apple.com > Account > Membership details > Team ID (10 characters).
6. **Add four repository secrets.** github.com/alialyami90/PRJ > Settings > Secrets and variables > Actions > New repository secret:

   | Name | Value |
   |---|---|
   | `APP_STORE_CONNECT_KEY_ID` | the Key ID |
   | `APP_STORE_CONNECT_ISSUER_ID` | the Issuer ID |
   | `APP_STORE_CONNECT_KEY` | the whole text of the `.p8` file (open it in Notepad, copy everything including the `BEGIN`/`END` lines) |
   | `APPLE_TEAM_ID` | the Team ID |

   Secrets are never pasted anywhere else, including chat. Keep the `.p8` file somewhere safe or delete it; a new key can always be made.
7. **Run it.** Actions > TestFlight > Run workflow. When it is green, App Store Connect > the app > TestFlight shows the build as Processing, then Ready.
8. **Testers.** In TestFlight, create an Internal Testing group, add yourself (and up to 100 App Store Connect users), and install from the TestFlight app. External testers (by email or public link, up to 10,000) need a quick Beta App Review on their first build.
