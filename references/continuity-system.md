# Continuity system

For sequences, maintain:

```yaml
characters: {identity: "", wardrobe: "", hair_makeup: "", behavior: ""}
props: {state_before: "", state_after: "", handoff: ""}
world: {location: "", time: "", weather: "", palette: "", light_direction: ""}
camera: {format: "", lens_family: "", height: "", screen_direction: ""}
sequence: {dramatic_arc: "", motion_progression: "", edit_rhythm: ""}
```

Track each shot's entry and exit state. Flag contradictions instead of silently repairing them. Preserve screen direction, eyelines, prop position, wardrobe state, light direction, and subject scale unless change is narratively motivated.
