# Episode 5 continuation example

## Continuity checkpoint

```text
SERIES: NORTH SIGNAL / NS
EPISODE: EP-05 / The Return Pulse
LAST APPROVED: EP-05-SC-02-SH-04; Mara exits screen-right carrying PROP-07
NEXT GOAL: reveal that the signal responds to Mara's movement without explaining its source
CHARACTERS: CHAR-01 Mara; gray insulated coat, torn left cuff, right-hand limp
PROPS: PROP-07 analog receiver, cracked casing, carried in right hand
WORLD: arctic station corridor, pre-dawn, blue spill camera-left, dry frost
VISUAL CONTRACT: 35mm anamorphic feeling, midnight blues, practical light, spatial suspense
ASSETS: CHAR-01_v03, PROP-07_v02, LOC-02_PREDAWN_v01
UNRESOLVED: whether Mara hears the signal or only sees the receiver react
```

## Image-base prompt

Create an original cinematic film still for `EP-05-SC-03-SH-01`. Inherit `CHAR-01_v03`, `PROP-07_v02`, and `LOC-02_PREDAWN_v01`. Preserve Mara's gray insulated coat with torn left cuff, right-hand limp, cracked analog receiver, and arctic station corridor geometry. Mara stands just beyond the communications-room doorway, screen-left, facing a sealed exterior door in deep background. A weak blue practical spill enters from camera-left; a small amber emergency lamp creates a localized pool near the receiver. Wide 35mm anamorphic perspective, deliberate horizontal staging, deep negative space, restrained midnight blues and desaturated steel, subtle fine grain, tactile frost and worn metal, slow-burn spatial suspense. No new characters, repaired cuff, changed prop, visible creature, or explanatory text.

## Image-to-video first test

Use the supplied image as the visual source of truth. Preserve Mara's identity, face, gray coat and torn cuff, right-hand limp, cracked receiver, corridor geometry, framing, practical light direction, palette, and lens perspective. Animate one primary action: Mara takes one cautious step toward the sealed door, then stops. Add one secondary action: the receiver emits two subtle pulses, the second synchronized to a small change in breathing. Camera: restrained slow forward dolly of less than one body length, ending before the door. Keep screen direction, feet contact, shadows, frost, and background geometry stable. No new characters, creature reveal, prop substitution, wardrobe repair, face drift, cuts, text, flicker, or rubbery motion.

## Success criteria

- Mara and inherited asset details remain stable.
- The step and stop are readable and physically grounded.
- The receiver pulses twice without deforming.
- The camera advances subtly without changing corridor geography.

## Post-test record

Do not mark the shot approved until the generated result is reviewed. Record the actual result, failures, approval state, and next required state in `continuity-ledger.yaml`.
