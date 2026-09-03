# Prompt evaluation rubric

After an actual generation, score each dimension 0–3: `0 failed`, `1 weak`, `2 usable`, `3 strong`.

```text
identity preservation
composition/reference fidelity
action clarity
temporal coherence
physical plausibility
camera execution
lighting continuity
director/movie grammar
artifact severity (reverse score)
```

Record the observed failure, the smallest prompt change that should address it, and the next test's success criteria. Compare A/B prompts by changing one major variable at a time. Do not call a prompt improved without an observed result.
