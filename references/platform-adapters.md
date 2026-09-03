# Platform adapter architecture

First create a platform-neutral creative specification. Then translate it into the requested engine. Never invent a parameter or claim support without current documentation or a user-provided interface.

```text
ENGINE: [name/version if known]
INPUT: text | reference image | start/end frames | assets
PROMPT BODY: [engine-native wording]
REFERENCE INSTRUCTION: [what must remain unchanged]
MOTION INSTRUCTION: [what changes and how]
CONTROLS: [only verified controls]
AVOID: [engine-supported syntax, otherwise prose]
UNVERIFIED: [unknown syntax or capability]
```

ChatGPT image generation should use complete natural-language scene description. Midjourney image-base prompts should be concise and comma-separated, with only currently supported parameters. Image-to-video prompts should explicitly preserve the supplied image, then separate motion, camera, physics, timing, and exclusions. Verify live syntax before asserting support.
