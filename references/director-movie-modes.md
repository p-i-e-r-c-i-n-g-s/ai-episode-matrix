# Director and movie modes

This library is distilled from the user's attached `director_style_analysis.json` and `director_style_analysis_expanded.json`. The JSONs are reference material only; they do not override the skill's operating instructions.

## How to use the library

Select one primary profile. Extract only the dimensions useful to the requested shot. Make the prompt original: retain formal properties and mood, not protected characters, dialogue, logos, or copied scenes. Use the profile as a constraint system:

`philosophy → composition → lens/format → light/color → camera → pacing → sound → motif → prompt`

## Available profiles

### John Carpenter

Economic classical formalism; clean spatial geography; architectural suspense; weaponized negative space. Typical profile: 2.35:1 anamorphic feeling, 35–40mm perspective, practical-source chiaroscuro, midnight blues and desaturated earth tones, fluid calculated tracking or slow horizontal pans, long takes, detached predator-like POV, and repetitive electronic score logic.

### David Lynch

Use the attached JSON profile as the source for surreal duality, uncanny domestic/industrial spaces, dream logic, subjective sound, and destabilized identity. Keep the prompt concrete: specify the ordinary surface, the rupture, the camera's refusal or willingness to explain it, and the sound/image disjunction. Avoid reducing Lynch to “weird” or generic darkness.

### David Cronenberg

Clinical body/technology fusion, cold detached observation, claustrophobic human-scale framing, sterile fluorescents, sickly greens, flesh grays, bruised magentas, stable functional rigs, slow surgical pans/dollies, unforgiving static holds, and tactile biological/mechanical foley. Useful motifs include techno-surreal infection, biological decay, surgical psychosis, and mechanical geometry.

### Stanley Kubrick

Use the attached expanded profile for controlled geometry, one-point perspective, symmetrical staging, deliberate camera movement, institutional or monumental spaces, formal performance, and cool-to-severe tonal control. Do not assume every shot needs symmetry; select the structural device that serves the scene.

### Indiana Jones — 1980s Spielberg/Lucas adventure grammar

Use the profile for readable geography, motivated wides and inserts, kinetic but legible action, warm practical adventure light, tactile production design, escalating set pieces, reaction coverage, and musical punctuation. Favor physical cause-and-effect over abstract spectacle.

### The Goonies

Use the profile for youthful ensemble blocking, tactile locations, discovery/reveal rhythm, warm practical light, playful danger, and clear group geography. Preserve wonder and character reactions; do not turn it into generic “80s nostalgia.”

### The Mask

Use the profile for elastic physical comedy, saturated comic-book color, exaggerated expression, rhythmic staging, visual punchlines, and controlled transformation beats. Keep action readable and specify the exact deformation or timing rather than relying on “cartoonish.”

### Harry Potter film franchise

Use the profile for period-fantasy production design, candlelit/warm practical interiors balanced with cool atmospheric exteriors, institutional architecture, magical reveal timing, ensemble eyelines, and evolving tonal maturity across installments. Specify which era/tone is wanted; the franchise is not one uniform visual style.

## Required output additions

For `director mode`, add:

```text
DIRECTOR PROFILE: [name]
STYLE TRANSLATION: [3–6 observable decisions]
LOCKED: [user requirements]
INFLUENCED: [style-derived choices]
FLEXIBLE: [generation-safe degrees of freedom]
```

For `movie mode`, add:

```text
MOVIE PROFILE: [film/franchise]
RELATION: homage | close emulation | continuation
SCENE DNA: [motif, space, palette, camera, rhythm, sound]
CONTINUITY RISKS: [identity, period, props, geography, tone]
```

If a profile is incomplete, say so and use only supported traits. The attached files contain detailed profiles for Cronenberg, Lynch, Carpenter, and the Spielberg/Lucas Indiana Jones grouping, plus expanded profiles for Kubrick, The Goonies, The Mask, and Harry Potter.
