# ChatGPT Image Gen → Seedance adapter

Use this adapter when ChatGPT Image Gen creates the approved still and Seedance animates that still. Seedance image-to-video prompts should describe what happens next, not rebuild the image. Preserve the source image's subject, medium, composition, lighting, and production design, then specify a restrained transformation.

## Prompt contract

```text
REFERENCE: Use the supplied image as the visual source of truth.
PRESERVE: [identity, wardrobe, props, set geometry, framing, palette, light, medium]
TRANSFORM: [one primary action, performance beat, camera move, secondary motion]
TIMING / END STATE: [start state → beats → settle state]
AUDIO (optional): [dialogue, voice, ambience, music, sync intent]
AVOID: [identity drift, prop substitutions, geometry warping, cuts, flicker, artifacts]
```

For Seedance interfaces that support multiple references, assign each asset one job. Do not fill every reference slot automatically.

## Reference-role priority

1. Approved character or product reference: identity, face, wardrobe, markings.
2. Approved start image: shot composition, location, lighting, art medium, lens perspective.
3. Motion reference: action trajectory, blocking, timing, or camera rhythm only.
4. Audio reference: dialogue wording, vocal performance, rhythm, or emotional timing only.
5. Text prompt: resolve the requested transformation and fill only unspecified gaps.

If references conflict, preserve approved identity and continuity first, then the approved start image, then motion/audio intent. Mark any unresolved conflict instead of silently blending incompatible instructions.

## Failure diagnostics

| Symptom | Likely cause | Revision |
|---|---|---|
| Face or costume drifts | Preserve block is vague or overloaded | Name the exact approved asset/version and shorten Transform |
| Scene geometry bends | Camera move is too aggressive | Use one slower motivated path; lock the spatial relationship |
| Motion feels rubbery | Too many simultaneous beats | Keep one action peak and one secondary effect |
| Style changes medium | Source medium was omitted | Explicitly preserve the image medium and texture |
| Unwanted cuts or shot changes | Multi-shot language in an I2V request | State one continuous shot and an end state |
| Lip sync misses | Dialogue, speaker, timing, or audio role is unclear | Provide exact line, speaker, pauses, and audio reference role |
| Grain or flicker swims | Texture generated frame-by-frame | Request stable texture or finish grain in post |

Record the observed failure against the take; never treat a failed generation as approved canon.

## Version boundary

Seedance capabilities, model names, reference syntax, durations, and controls vary by interface and release. Record the exact model/interface and mark unsupported controls `UNVERIFIED`; do not assume `@Image`, audio, multi-reference, or native-audio behavior is available everywhere.
