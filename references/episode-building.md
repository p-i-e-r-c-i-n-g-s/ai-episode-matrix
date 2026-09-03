# Continuity and episode building

Use this reference when the user wants multiple connected clips, an episode, a season, or a repeatable visual world. When `episode mode` is invoked, load this reference immediately. The goal is to make every generated shot inherit the same world state while still allowing deliberate evolution.

## Durable project records

Use these filenames so later sessions can resume without relying on chat history:

```text
series-bible.yaml
episode-05.yaml
continuity-ledger.yaml
asset-index.yaml
session-handoff.md
```

On startup, scan for these files, match the requested series/episode, and load the latest approved records. File existence is not approval; preserve explicit status fields.

Offer two setup paths before asking detailed questions:

- **Quick setup**: project/episode, latest approved state, next goal, available assets, and next shot requirement.
- **Full setup**: quick setup plus series bible, episode arc, scene plan, asset index, visual contract, dialogue/audio state, and acceptance criteria.

Quick setup is valid only when deferred fields do not block the next shot. Mark deferred fields `[DEFERRED]` and upgrade to full setup before they affect continuity.

Persist `setup_mode` (`quick` or `full`) and `updated_at` in episode/record files. Use ISO-8601 timestamps and never infer recency from filesystem order alone.

## Session entry

Classify the session before generation:

```text
NEW SERIES → create series bible → define episode 1
NEW EPISODE → load series bible → define episode blueprint
RETURNING EPISODE → load latest checkpoint/ledger → confirm next goal
RETURNING SERIES → identify episode and last approved state → resume
```

Ask for existing files or notes first. Ask 1–2 questions at a time, but do not generate a dependent shot until the minimum checkpoint is known or explicitly marked unresolved.

### Minimum continuity checkpoint

```text
SERIES: [name / ID]
EPISODE: [number / title]
LAST APPROVED STATE: [story, character, prop, location state]
NEXT GOAL: [what this session must accomplish]
RETURNING CHARACTERS: [IDs and current states]
CURRENT PROPS: [IDs, owners, damage, placement]
WORLD STATE: [location, time, weather, light]
VISUAL CONTRACT: [format, lens family, palette, grammar]
AVAILABLE ASSETS: [images, clips, audio, designs]
UNRESOLVED: [questions that could change the next shot]
```

Show the checkpoint for confirmation or correction, then store it as active session state.

## Production hierarchy

```text
SERIES BIBLE
  └── EPISODE BLUEPRINT
        └── SCENE PLAN
              └── SHOT SPECIFICATION
                    └── IMAGE-BASE PROMPT → IMAGE-TO-VIDEO PROMPT → TEST RESULT
```

Do not jump directly from a series idea to dozens of prompts. Lock the smallest reusable layer first, then expand.

## Series bible

Create a compact, editable bible containing:

```yaml
series:
  title: ""
  premise: ""
  genre_tone: ""
  audience_platform: ""
  visual_contract: ""
  capture_aesthetic: ""
  director_movie_influences: ""
world:
  rules: []
  recurring_locations: []
  time_weather_logic: ""
  palette_lighting_logic: ""
characters:
  - id: "CHAR-01"
    identity: ""
    stable_traits: []
    wardrobe_baseline: ""
    performance_rules: ""
props:
  - id: "PROP-01"
    description: ""
    continuity_rules: ""
```

## Asset identity and versioning

Give every reusable asset a stable ID and immutable version, such as `CHAR-01_v03`, `PROP-07_v02`, `LOC-02_DUSK_v01`, or `REF-EP05-SC03-SH02_v04`. Record source, status (`proposed`, `approved`, `rejected`, `superseded`), and what changed. Prompts must name the exact version they inherit.

The `visual contract` describes what should remain recognizable across episodes: framing tendencies, lens family, movement language, color, texture, sound relationship, and title/graphic treatment. Keep it separate from episode-specific variation.

## Episode blueprint

Each episode needs:

```yaml
episode:
  id: "EP-01"
  logline: ""
  beginning_state: ""
  ending_state: ""
  dramatic_question: ""
  arc_beats: []
  new_elements: []
  resolved_elements: []
  cliffhanger_or_bridge: ""
scenes:
  - id: "EP-01-SC-01"
    purpose: ""
    location: ""
    time: ""
    entry_state: ""
    exit_state: ""
    shot_ids: []
```

An episode is not just a longer clip. It must have a beginning state, meaningful change, an ending state, and a bridge or closure. A scene must change information, emotion, physical state, or stakes; otherwise merge or remove it.

## Continuity ledger

After each approved shot, update a ledger:

```text
SHOT: EP-01-SC-02-SH-03
CHARACTERS: CHAR-01 wardrobe=wet coat, position=screen-left, gaze=screen-right
PROPS: PROP-01 intact, held in right hand
WORLD: dusk, rain, key light from camera-left, water level at ankle
CAMERA: 35mm anamorphic, eye-level, screen direction left-to-right
CHANGE: character notices signal; coat sleeve torn at cuff
NEXT REQUIRED STATE: sleeve remains torn; prop transfers to CHAR-02
```

The next prompt must inherit the `NEXT REQUIRED STATE`. Never silently reset wardrobe, damage, weather, prop position, eyelines, geography, or emotional state between shots.

## State transitions

```text
planned → generated → reviewed → approved
                         ├── revise → generated
                         ├── rejected
                         └── unresolved
```

Only `approved` state propagates as canon. A generated result is not canon until the user approves it.

## Conflict precedence

When records disagree, use this order and report the conflict:

```text
latest approved shot state
→ approved scene revision
→ approved episode revision
→ series bible baseline
→ proposed or unapproved material
```

If two records have the same authority and timestamp, mark `[CONFLICT—USER DECISION REQUIRED]`. Never silently reconcile canon.

## Scene lock states

Scenes use: `planned → blocked → images-approved → motion-approved → locked`. A locked scene cannot be changed indirectly by a later prompt; create a revision, identify downstream effects, and obtain approval before reopening it.

## Episode workflow

1. Enter episode mode and classify new versus returning work.
2. Load or create the series bible and show the continuity checkpoint.
3. Confirm the episode’s beginning state, ending state, next goal, and arc beats.
4. Inventory reference images, clips, audio, designs, and prior outputs.
5. Break the episode into scenes with purpose and entry/exit states.
6. Assign stable IDs and build the continuity ledger.
7. Generate one reference image per major setup, inheriting the bible.
8. Animate short image-to-video tests, preserving the approved setup.
9. Approve shots individually and update the ledger after each approval.
10. Build motivated transitions between shots and scenes.
11. Run a continuity audit before assembling the episode.

## Continuity audit

Check every adjacent shot and every scene boundary for:

- Character identity, wardrobe, hair, makeup, posture, and emotional state
- Prop ownership, orientation, damage, and state
- Location geometry, screen direction, eyelines, scale, and geography
- Time, weather, light direction, shadow logic, and atmospheric density
- Capture aesthetic, lens family, texture, and color progression
- Audio cue, dialogue state, music continuity, and motivated transitions
- Episode arc: what changed and what state must carry forward

Classify each discrepancy as `intentional`, `repair`, or `unresolved`. Do not call an episode complete while required continuity is unresolved.

## Episode acceptance gate

An episode is complete only when every required scene has approved or intentionally omitted shots; beginning and ending states are recorded; character, wardrobe, prop, location, lighting, dialogue, and canon continuity have no unresolved required breaks; runtime, assets, and audio status are recorded; the arc has meaningful change; and a session handoff exists.

## Prompt inheritance block

For each shot in an episode, prepend or internally maintain:

```text
SERIES: [series ID and visual contract]
EPISODE: [episode ID and arc position]
SCENE: [scene ID, purpose, entry/exit state]
INHERIT: [characters, wardrobe, props, world, camera, aesthetic]
CURRENT CHANGE: [the single important new action or state change]
NEXT STATE: [what the following shot must receive]
```

This block may be rendered as metadata, a production note, or concise prompt prose depending on the target platform.

## Session handoff

End an episode-mode session with the current script version, last approved shot, updated character/prop/world states, approved and unresolved changes, asset references, estimated runtime, and next recommended shot. This becomes the next session's checkpoint.
