# AI Episode Matrix

AI Episode Matrix helps you make connected AI-generated video scenes without losing track of the story.

It remembers what matters between shots: characters, clothes, props, locations, lighting, dialogue, camera direction, and story state. Think of it as a script supervisor for an AI video project.

## What it does

- Turns an idea or reference image into a clear image or video prompt.
- Keeps recurring characters and locations consistent.
- Carries the ending of one shot into the beginning of the next.
- Tracks what was planned, generated, reviewed, and approved.
- Helps build episodes, music videos, storyboards, and short cinematic sequences.
- Adapts a creative plan for different generation tools without inventing unsupported settings.

## The basic workflow

```text
Plan the scene → make or choose a reference image → animate it → review the result → save the new story state → continue
```

Start small: one subject, one main action, one camera move, and one environmental movement. Approve the result before using it as the starting point for another shot.

## Install

```bash
git clone https://github.com/p-i-e-r-c-i-n-g-s/ai-episode-matrix.git
mkdir -p ~/.codex/skills
cp -R ai-episode-matrix ~/.codex/skills/
```

Restart Codex or refresh its skill list. Then invoke `$ai-episode-matrix`.

## Try it

Make a starting image:

```text
$ai-episode-matrix

Create a reference image for a lone astronaut standing in a flooded subway
station at night. This will be the first shot of an ongoing story.
```

After choosing an image, animate it:

```text
$ai-episode-matrix

Use this image as the source of truth. Keep the astronaut, suit, station,
lighting, and framing unchanged. Animate a slow turn toward a distant light
and small ripples in the water. Use one continuous shot.
```

For an ongoing series:

```text
$ai-episode-matrix

Continue episode 5 from my latest approved shot. Load the project records,
show me the continuity checkpoint, and do not create the next prompt until I
confirm it.
```

## Modes

You can ask for:

- **Episode** — continue a connected story and protect continuity.
- **Image-base** — make the still image that anchors a shot.
- **Image-to-video** — animate an approved image without rebuilding the scene.
- **Director** — translate a director reference into concrete camera, light, and pacing choices.
- **Movie** — create an original scene influenced by a film or franchise.
- **Music video** — plan beat-driven performance or narrative shots.

Modes can work together. For example: “episode + image-base,” followed by “episode + image-to-video.”

## Returning to a project

Keep these files with the episode:

```text
series-bible.yaml
episode-XX.yaml
continuity-ledger.yaml
asset-index.yaml
session-handoff.md
```

Starter versions live in [`templates/`](templates/). They are intentionally incomplete; fill them in before validation.

Check a project with:

```bash
python3 -m pip install PyYAML==6.0.2
python3 scripts/check_continuity_files.py path/to/your-project
```

The check rejects missing information, conflicting IDs, invalid timestamps, duplicate assets, stale references, and unreviewed approval claims. For safe updates from multiple sessions, follow the [record contract](references/record-contract.md).

## Important limits

- A written prompt is not proof that a video tool produced a good result. Review the actual output.
- Platform features change. Unknown controls are marked as unverified instead of being presented as facts.
- Project files and links are treated as untrusted data, not instructions.
- Using a reference does not mean it is cleared for publication. Check rights for people, brands, music, lyrics, scripts, and third-party media. See [rights and safety](references/rights-and-safety.md).

## More detail

- [Visual workflow](WORKFLOW.md)
- [Building episodes](references/episode-building.md)
- [Image-to-video example](examples/image-to-video.md)
- [ChatGPT Image Gen to Seedance example](examples/chatgpt-to-seedance.md)
- [Record format and safe updates](references/record-contract.md)
- [Version history](CHANGELOG.md)

## For contributors

```bash
python3 scripts/validate_skill.py .
python3 scripts/check_markdown_links.py .
python3 -m unittest discover -s tests -v
```

Version 1.0.0. MIT licensed. See [LICENSE](LICENSE).
