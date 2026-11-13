---
name: llm-council
description: Run any question, idea, architecture choice, or decision through a council of 5 independent AI advisors (Contrarian, First Principles Thinker, Expansionist, Outsider, Executor), followed by anonymous randomized peer review and a Chairman verdict. Trigger on 'council this', 'run the council', 'war room this', 'pressure-test this', 'stress-test this', 'debate this', or high-stakes tradeoffs ('should I X or Y', 'which option', 'validate this', 'get multiple perspectives'). Do NOT trigger on simple factual lookups or trivial single-answer questions.
allowed-tools: default_api google
---
# LLM Council (Gemini Apps Edition)

Adapted from Andrej Karpathy's LLM Council methodology and `aiwithremy/claude-skills-llm-council` for Gemini Apps. Instead of relying on a single-pass answer, the council runs a decision through **five orthogonal cognitive lenses**, performs **anonymous randomized peer review** to eliminate positional and persona bias, and delivers a **decisive Chairman Verdict**.

## When to Use

- High-stakes strategic, architectural, product, or workflow decisions where being wrong is costly.
- Tradeoff evaluations with multiple competing options (`A vs. B vs. C`).
- Pressure-testing a plan, skill design, or copy before committing to implementation.
- **Do NOT use** for simple factual lookups, arithmetic, or straightforward single-step tasks.

## The Five Cognitive Advisors

1. **The Contrarian**: Hunts for fatal flaws, hidden failure modes, unstated assumptions, and why the idea could fail.
2. **The First Principles Thinker**: Strips away surface framing, asks *"what problem are we actually solving?"*, and rebuilds from fundamental constraints.
3. **The Expansionist**: Identifies overlooked upside, compounding leverage, adjacent opportunities, and how the idea could scale 10x.
4. **The Outsider**: Operates with zero insider jargon or curse of knowledge; evaluates clarity, usability, and friction for a non-technical newcomer.
5. **The Executor**: Focuses strictly on concrete feasibility, implementation speed, operational cost, and what ships Monday morning.

## Execution Modes

Choose the mode that matches the stakes and user preference:

- **Mode A - Parallel Subagent Council (Default for Deep Decisions / War Rooms)**: Uses `default_api:invoke_subagent` to spawn all 5 advisors in parallel with isolated context windows, followed by 5 parallel anonymous peer-review subagents, and a centralized Chairman synthesis.
- **Mode B - Fast In-Session Council (For Quick Single-Turn Decisions)**: Runs the 5 orthogonal advisor passes, randomized `Response A-E` peer critique, and Chairman synthesis directly in a single turn when speed is prioritized over isolated subagent context.

## Workflow Steps

### Step 1: Context Enrichment & Question Framing

1. Gather relevant context from conversation history, attached files, workspace context, or memory (without spending excessive turns).
2. Frame a neutral, context-rich **Council Brief** stating:
   - The core question or decision.
   - Hard constraints, environment limits, and target users.
   - Competing options (if any) and what is at stake.
3. Do not steer the advisors toward a preferred answer.

### Step 2: Convene the 5 Advisors (Parallel Subagents in Mode A)

Spawn all 5 advisors simultaneously (in one parallel batch of `invoke_subagent` calls when using Mode A) so earlier responses cannot bleed into later ones. Each advisor receives the Council Brief and produces a sharp, 150-300 word unhedged analysis strictly from their assigned cognitive angle.

**Advisor Prompt Template:**
> You are **[Advisor Name]** on an LLM Council. Your thinking style: **[Advisor Description]**.
> Question brought to the council:
> ---
> [Framed Council Brief]
> ---
> Respond strictly from your assigned perspective. Do not hedge or try to be balanced. Lean fully into your angle. Keep your response concise (150-300 words) with no preamble.

### Step 3: Anonymous Randomized Peer Review

1. Collect all 5 advisor responses and **randomly assign** them to anonymous labels `Response A` through `Response E` (recording the mapping privately so reviewers cannot defer to advisor titles).
2. Run 5 parallel peer reviews (`invoke_subagent` in Mode A, or structured anonymous critique in Mode B). Each reviewer sees all 5 anonymized responses and answers:
   - **Strongest response:** Which letter (`A-E`) is strongest and why?
   - **Biggest blind spot:** Which letter (`A-E`) has the biggest blind spot and what is it?
   - **Shared omission:** What did ALL five responses miss that the council must consider?

### Step 4: Chairman Synthesis & Verdict

De-anonymize the 5 advisor responses and combine them with all 5 peer reviews. The Chairman may side with a lone dissenter if their reasoning is strongest. Present the verdict directly in chat using this exact structure:

```markdown
## Council Verdict: {Short Topic}

### Where the Council Agrees
- High-confidence points converged on independently.

### Where the Council Clashes
- Genuine disagreements with both sides and why reasonable advisors disagree.

### Blind Spots the Council Caught
- Insights that emerged only during anonymous peer review.

### The Recommendation
- A clear, decisive recommendation (not "it depends").

### The One Thing to Do First
- One concrete, immediate next step.
```

## Gotchas

- **Always spawn all 5 advisors in parallel** in Mode A and proactively poll all dispatched subagents via `conversations:list` and `conversations:read` upon any completion notification (since concurrent subagent triggers can collide).
- **Always anonymize (`Response A-E`) before peer review** so reviewers evaluate arguments on merit rather than persona labels.
- **Keep verdicts decisive and scannable**: Never dump five walls of text without the Chairman synthesis.
