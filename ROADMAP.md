# Roadmap

## v0.3 Focus: Evidence-Based Cost and Vendor Choices

v0.3 is about making stack advice harder to fool with marketing copy.

Completed:

- Add pricing and operating-cost checks to `SKILL.md`.
- Require recommendations to distinguish "free to start" from "cheap to operate."
- Add blunt tradeoff requirements: what you gain, what you give up, what becomes harder later, and when the recommendation becomes wrong.
- Clarify that `SKILL.md` is portable beyond Claude/Codex.
- Add a pricing-focused example.

Next useful work:

- Add more day-in-the-life examples contributed by users.
- Run cross-model evals on the same prompts: Claude, Codex, Tenki, Gemma, and other agent harnesses.
- Add more vendor-cost examples: Vercel, Firebase, Neon, PlanetScale, Render, Railway, Fly.io, object storage, observability, and AI API usage.
- Collect "bad generic stack advice" test cases through the issue template.
- Improve the README demo with a before/after output that includes cost and vendor reality.

## Contribution Format for Examples

The most useful example format:

1. User situation.
2. Generic AI answer that would be too shallow.
3. Evidence/repo/comparable/pricing checks the agent should do.
4. Better final recommendation.
5. What would make the recommendation wrong.
