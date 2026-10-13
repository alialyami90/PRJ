# Monetization: ads in a kids' app

## The constraint

An app made for children must be listed in the App Store **Kids Category** (App Review Guideline 1.3, plus 5.1.4 on kids' data). That category restricts advertising:

- No behavioural or interest-based ads. Contextual ads only.
- No third-party ad or analytics SDK that collects device identifiers (IDFA) or personal data. Ask for no tracking permission at all.
- Any link out of the app, purchase, or ad that opens the store must sit behind a **parental gate** (e.g. "hold for 3 seconds" or a simple sum).
- COPPA (US) and GDPR-K (EU) apply; most large networks have a "child-directed" flag that switches them into this mode.

Networks known to work in the Kids Category when configured correctly:

| Network | Notes |
|---|---|
| Google AdMob | Set `tagForChildDirectedTreatment = true`, `maxAdContentRating = .general`, disable mediation partners that are not COPPA-certified. Biggest fill in Saudi. |
| SuperAwesome (AwesomeAds) | Kids-only network, COPPA/GDPR-K certified by design. Lower fill, higher compliance confidence. |
| Kidoz | Kids-only, SDK designed for parental gates. |

## Ad placements (planned)

1. **Gallery banner** (adaptive banner at the bottom of region/scene pickers). Never on the canvas.
2. **Interstitial between scenes**, capped (e.g. at most 1 per 3 completed scenes, never within the first 2 minutes of a session).
3. **Rewarded video** (optional, parental gate first): unlock a bonus palette or sticker set after finishing a scene.

Measuring revenue: eCPM and fill come from the network dashboard; the app only reports impressions/clicks through `AdService` for debugging. Expect Saudi kids-category eCPMs well below general-audience rates; plan for an optional "Remove ads" IAP behind a parental gate as a second revenue line.

## Implementation rule

Everything ad-related goes through `Services/Ads/AdService` (a protocol). Features never import an ad SDK directly, so the network can be swapped or disabled (e.g. for a paid tier) without touching UI code.
