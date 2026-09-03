# Continuity and episode building

Use this reference when the user wants multiple connected clips, an episode, a season, or a repeatable visual world. The goal is to make every generated shot inherit the same world state while still allowing deliberate evolution.

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

## Episode workflow

1. Define the series bible and visual contract.
2. Define the episode’s beginning state, ending state, and arc beats.
3. Break the episode into scenes with purpose and entry/exit states.
4. Assign stable IDs and build the continuity ledger.
5. Generate one reference image per major setup, inheriting the bible.
6. Animate short image-to-video tests, preserving the approved setup.
7. Approve shots individually and update the ledger after each approval.
8. Build transitions using match-on-action, eyeline, screen direction, sound lead/lag, or a deliberate state change.
9. Run a continuity audit before assembling the episode.

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
