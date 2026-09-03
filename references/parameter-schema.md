# Reusable parameter schema

```yaml
project:
  purpose: ""
  audience/platform: ""
  model: "model-agnostic"
  aspect_ratio: ""
  duration_seconds: null
  fps: null
continuity:
  subject_identity: ""
  wardrobe_props: ""
  location_time_weather: ""
  palette: ""
aesthetic:
  capture_format: ""
  lens_perspective: ""
  emulsion_influence: ""
  presentation_format: ""
  flash: {mode: "", color: "", intensity: "", shape_or_spread: "", falloff: "", timing: ""}
  grain: {amount: "", character: ""}
  exposure_color: ""
  optical_artifacts: ""
  cinematic_grammar: ""
shot:
  intent: ""
  subject: ""
  action_beats: []
  composition: {shot_size: "", angle: "", camera_height: "", screen_direction: ""}
  camera: {movement: "", speed: "", motivation: "", stabilization: ""}
  lens: {focal_length: "", perspective: "", depth_of_field: "", focus_behavior: ""}
  lighting: {key_source: "", direction: "", quality: "", color_contrast: "", atmosphere: ""}
  image: {palette: "", contrast: "", highlight_behavior: "", texture: ""}
  edit: {in_state: "", out_state: "", transition: "", sound_or_music_cue: ""}
  constraints: []
image_to_video:
  reference_image_role: "visual source of truth"
  preserve: []
  animate: []
  start_state: ""
  action_beats: []
  camera_path: ""
  temporal_pacing: ""
  end_state: ""
  avoid: []
  success_criteria: []
```

Treat empty fields as questions or labeled assumptions, not permission to invent.

For image-to-video work, `preserve` and `animate` are mandatory conceptual fields even when rendered as natural-language prose. This prevents the model from treating the reference image as a loose inspiration instead of the scene's continuity anchor.
