# Aesthetic knobs and capture references

Use this stack when the user wants a particular photographic, filmic, or presentation character. Each knob should produce an observable image consequence. Keep the values independent so they can be changed without rewriting the whole prompt.

## Aesthetic stack

```yaml
aesthetic:
  capture_format: "35mm | Super 35 | medium format | 65/70mm | IMAX"
  lens_perspective: "spherical | anamorphic | vintage | modern clinical | specified focal length"
  emulsion_influence: "Ektar 100 | Portra | Vision3-style | tungsten/daylight influence | custom"
  presentation_format: "standard theatrical | IMAX 70mm | IMAX HD | Maxivision | digital streaming"
  flash:
    mode: "none | direct on-camera | bounced | ring | paparazzi | strobing"
    color: ""
    intensity: ""
    shape_or_spread: ""
    falloff: ""
    timing: ""
  grain:
    amount: "none | fine | medium | coarse"
    character: "static | motion-consistent | organic"
  exposure_color: "highlight roll-off, halation, lifted/crushed blacks, saturation, color bias"
  optical_artifacts: "gate weave, dust, scratches, bloom, chromatic aberration, shutter smear, lens breathing"
  cinematic_grammar: "blocking, camera movement, pacing, sound-image relationship"
```

## Interpretation rules

- `Capture format` describes scale, perspective, depth, resolution, and capture character. Do not use it as a substitute for directing style.
- `Lens perspective` describes spatial rendering. Name a focal length only when it changes the relationship between subject and background.
- `Emulsion influence` describes color, contrast, skin-tone behavior, grain, and latitude. Ektar 100 and Portra are still-photography references; describe their visual qualities rather than claiming literal motion-picture stock.
- `Presentation format` describes the intended viewing/finishing experience. IMAX HD, IMAX 70mm, and “Magic Carpet” references belong here or under large-format presentation, not under emulsion. Maxivision is a motion-picture format/presentation reference, not a color stock.
- `Flash` must specify source direction, hardness, color, intensity, spread, falloff, and timing when relevant. “Camera flash” alone is incomplete.
- `Grain` must remain coherent across frames. For image-to-video, request motion-consistent grain or add it in finishing; do not ask the generator to create unstable grain that swims across the image.
- `Optical artifacts` are optional. Use no more than the scene can support; excessive gate weave, bloom, dust, and aberration compete with motion and identity preservation.
- `Cinematic grammar` is where director/movie influence belongs. It governs blocking, camera behavior, light motivation, pacing, and editorial intent—not the capture format alone.

## Director/movie associations

Associations are suggestive starting points, not automatic mappings. A format can support many traditions, and a director may work across formats. Present associations as “compatible visual traditions,” then let the user lock or reject them.

Useful examples:

- 35mm / Super 35: versatile theatrical grammar, practical scale, naturalistic perspective, optical finishing, and a broad range of genre traditions.
- 65/70mm / IMAX: monumental scale, deep environmental readability, large-format clarity, controlled movement, and spectacle that depends on geography rather than blur.
- Medium format: portrait intimacy, material detail, shallow-to-moderate depth, and editorial stillness; use cautiously for moving-image prompts.
- Direct flash / paparazzi flash: confrontational observation, social exposure, nightlife energy, tabloid immediacy, or unstable public/private boundaries.
- Fine-grain Ektar-like influence: crisp detail, clean saturated color, controlled grain, and graphic separation.
- Portra-like influence: gentle contrast, restrained saturation, warm or natural skin rendering, and softer highlight behavior.

Never assert that a named director or movie used a specific stock, format, or lens unless verified for the relevant production. If the user requests an association, describe the shared visual traits and label the association as a stylistic inference.

## Prompt rendering

Render the stack in concise prose after the scene description, for example:

```text
Capture aesthetic: 65/70mm large-format presentation, spherical 50mm perspective, fine-grain warm negative influence with restrained saturation, protected skin tones, gentle halation, subtle motion-consistent grain. No flash. Cinematic grammar: deliberate lateral track, clear ensemble geography, practical backlight, slow reveal.
```

For image-to-video, separate it into `preserve from reference` and `animate/change`. The aesthetic stack normally belongs in `preserve`, except for intentional animated light, flash timing, smoke, or exposure changes.
