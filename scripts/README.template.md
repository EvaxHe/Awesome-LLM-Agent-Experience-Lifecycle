<div align="center">

# Awesome LLM-Agent Experience Lifecycle [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

### The **Experience Lifecycle** of lifelong, self-evolving & memory-augmented LLM agents

_A curated, continuously-updated reading list that follows agent **experience** end-to-end —
from raw interaction to persistent memory, abstracted skills, internalized weights, and shared knowledge._

[![arXiv](https://img.shields.io/badge/arXiv-coming%20soon-b31b1b)](#-citation)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/EvaxHe/Awesome-LLM-Agent-Experience-Lifecycle?style=social)](https://github.com/EvaxHe/Awesome-LLM-Agent-Experience-Lifecycle/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/EvaxHe/Awesome-LLM-Agent-Experience-Lifecycle?color=blue)](https://github.com/EvaxHe/Awesome-LLM-Agent-Experience-Lifecycle/commits)
[![License](https://img.shields.io/github/license/EvaxHe/Awesome-LLM-Agent-Experience-Lifecycle)](LICENSE)

<!-- BEGIN:STATS -->
_generated_
<!-- END:STATS -->

</div>

> **TL;DR — experience is the new training data.** Pretraining learns from a fixed corpus and
> instruction tuning from human demonstrations; experience-driven agents learn from the
> trajectory-bearing interactions they generate *themselves* at deployment time. This list
> organizes that literature by the **lifecycle of an experience signal** — the path it takes
> from acquisition to persistent change — rather than by which artifact gets updated.

<p align="center">
  <img src="assets/lifecycle.png" width="820"
       alt="The Experience Lifecycle: eight stages — 1 Acquisition, 2 Representation, 3 Retrieval, 4 Consolidation, 5 Abstraction, 6 Internalization, 7 Revision & Forgetting, 8 Distribution — arranged as a closed loop (Distribution loops back to Acquisition). Each stage produces an artifact (raw traces, typed memory, surfaced cases, compressed memory, skills/workflows/tools, model weights/adapters, pruned/amended artifacts, shared registries), and a cross-cutting Governance overlay (provenance, attestation, revocation, quarantine, audit) spans every stage.">
</p>

---

## Why another list? (how this differs from existing ones)

Prior reading lists organize the field by **module** or by **what evolves**. This one follows
**experience as it flows**, which surfaces the under-served stages (Revision, Distribution) and a
cross-cutting **Governance / threat** layer that the others omit.

| Existing list | Organized by | What this list adds |
| --- | --- | --- |
| [qianlima-lab/awesome-lifelong-llm-agent](https://github.com/qianlima-lab/awesome-lifelong-llm-agent) | Module: perception / memory / action | Consolidation, Abstraction, Revision, and a Governance threat model — none of which a module view captures |
| [EvoAgentX/Awesome-Self-Evolving-Agents](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents) | What / when / how to evolve | The flow *between* stages, the under-served right end (Revision S7, Distribution S8), and the EPTM threat model |
| [TsinghuaC3I/Awesome-Memory-for-Agents](https://github.com/TsinghuaC3I/Awesome-Memory-for-Agents) | Memory only | Memory → skill → weights treated as one pipeline, not memory in isolation |

---

## Contents

- [The eight stages](#the-eight-stages)
  - [S1 — Acquisition](#s1) · [S2 — Representation](#s2) · [S3 — Retrieval & Use](#s3) · [S4 — Consolidation](#s4)
  - [S5 — Abstraction](#s5) · [S6 — Internalization](#s6) · [S7 — Revision & Forgetting](#s7) · [S8 — Distribution](#s8)
- [Cross-cutting frameworks](#cross-cutting-frameworks)
- [What the field actually updates](#-what-the-field-actually-updates)
- [Governance & the Experience-Pipeline Threat Model (EPTM)](#-governance--the-experience-pipeline-threat-model-eptm)
- [Routing: where should an experience signal live?](#-routing-where-should-an-experience-signal-live)
- [Evaluating change over time](#-evaluating-change-over-time)
- [Related surveys](#-related-surveys)
- [Foundations & background](#foundations--background)
- [Framing & position pieces](#framing--position-pieces)
- [Open problems](#-open-problems)
- [Citation](#-citation) · [Contributing](#-contributing) · [Star history](#-star-history)

---

## The eight stages

<p align="center">
  <img src="assets/Taxonomy.png" width="860"
       alt="Taxonomy of experience-driven agent methods: the eight lifecycle stages (Acquisition, Representation, Retrieval, Consolidation, Abstraction, Internalization, Revision & Forgetting, Distribution), each with three method families and one canonical system — for example, Acquisition has outcome/reward (DeepSeek-R1), trajectory (Voyager), and reflection (Reflexion). A cross-cutting Governance overlay (provenance, attestation, revocation, quarantine, audit) spans all stages.">
</p>
<p align="center"><sub>Each stage's method families, with one canonical system each — a visual index to the per-stage tables below.</sub></p>

> A system can appear under **every stage it touches**, so the same paper may show up in more than
> one table. Systems that span five or more stages are grouped under
> [Cross-cutting frameworks](#cross-cutting-frameworks). All tables are generated from
> [`data/literature_matrix.csv`](data/literature_matrix.csv) — to add or correct an entry, edit the
> CSV (see [Contributing](CONTRIBUTING.md)).

<!-- BEGIN:STAGES -->
_generated_
<!-- END:STAGES -->

## Cross-cutting frameworks

> Systems whose experience pipeline spans most of the lifecycle (≥5 stages) — closed-loop
> self-evolving agents and broad frameworks.

<!-- BEGIN:CROSSCUT -->
_generated_
<!-- END:CROSSCUT -->

---

## 🗺 What the field actually updates

Stepping back from the per-stage lists: the survey's **§2.8 corpus analysis** hand-codes all **90**
experience-driven systems by *which surface* each one updates. Read as a **stage × update-surface**
grid, it shows a sharp **two-pole** pattern — updates split almost evenly between **external memory**
(44 systems) and **model weights** (43), with skills, workflows, and tools thin throughout: systems
_use_ tools and _enact_ skills far more than they _update_ them. Weights concentrate sharply at
**Internalization** (39 — the densest cell), while **Revision & Forgetting** stays nearly empty — an
empirical echo of the gap the survey argues is most under-served.

<p align="center">
  <img src="assets/mapped_corpus.png" width="820"
       alt="Heatmap of update surfaces across the experience lifecycle. Rows are the eight lifecycle stages (Acquisition, Representation, Retrieval & Use, Consolidation, Abstraction, Internalization, Revision & Forgetting, Distribution); columns are five update surfaces (Memory, Skills, Workflow, Tools, Weights). Each cell counts how many of the 90 systems in the survey's §2.8 corpus update that surface at that stage. External memory (44 systems) and model weights (43) dominate; weights spike at Internalization (39, the densest cell); Skills, Workflow and Tools stay thin throughout; Revision & Forgetting is nearly empty.">
</p>
<p align="center"><sub>The survey's frozen <strong>§2.8</strong> corpus (Table C2): 90 hand-verified systems, each cell counting a system in every stage it spans (so columns need not sum to 90). Reproduce with <a href="reproducibility/"><code>reproducibility/corpus_coding.py</code></a>. The stage tables above are the repository's <em>living</em> index and apply a slightly broader curation (with separate Benchmark/Governance/Foundation sections), so their counts differ from this frozen analysis by design.</sub></p>

---

## 🛡 Governance & the Experience-Pipeline Threat Model (EPTM)

Once experience **persists and accumulates**, the agent gains an attack surface a stateless model
does not have. Governance is treated as a **cross-cutting overlay** — five primitives (provenance,
attestation, revocation, quarantine, audit) that operate on the artifact produced at *every* stage.
The **EPTM** maps each persistence attack to the stage it hits, the artifact it compromises, and the
governance primitive that defends it.

| Attack target | Stage | Mechanism | Artifact compromised | Defense (primitive) |
| --- | --- | --- | --- | --- |
| Memory store | S2 | Benign-looking ingestion artifacts injected at write time (MINJA) | Stored memory entries | Counterfactual Composition Testing (audit + provenance) |
| Memory (latent) | S2→S4→S7 | Long-dormant injection that activates on a future trigger (Sleeper Memory) | Consolidated memory surviving summarization | Provenance + replay-based revocation |
| Retrieval pipeline | S3 | Malicious procedure templates persisted alongside benign experience (MemoryGraft) | Retrievable experience cases | Bayesian trust attestation |
| Retrieval pipeline | S3 | Crafted queries pull another user's stored data | Cross-user memory entries | Privacy-preserving MA memory + audit |
| Reasoning trace | S1→S3 | Sensitive data copied into stored chain-of-thought (Leaky Thoughts) | Stored reasoning traces | Trace minimization + audit |
| Skill registry | S5 | Malicious instructions embedded in a shared `SKILL.md` | Abstracted skill artifact | Provenance + sandboxed execution + revocation |
| Model weights | S6 | Narrow fine-tuning on harmful / low-quality experience | Internalized parameters | Replay + monitoring |
| Agent population | S8 | Saboteur peer injects poisoned experience into a shared pool | Distributed / federated experience | Population quarantine + trust defense |

### Threat & defense papers

> Located by the stage they attack (per the EPTM above), grouped here as the cross-cutting
> Governance overlay rather than under a single stage.

<!-- BEGIN:GOVERNANCE -->
_generated_
<!-- END:GOVERNANCE -->

---

## 🧭 Routing: where should an experience signal live?

A practitioner's decision aid — given a signal type, where in the pipeline does the literature
put it?

| Experience type | → Memory (S2–3) | → Skill / workflow / tool (S5) | → Weights / adapters (S6) | → Discard / revise (S7) |
| --- | :---: | :---: | :---: | :---: |
| **Outcome / verifiable reward** | rarely | rarely | **preferred** (dense, verifiable) | drop invalid-env rewards |
| **Trajectory (rare success)** | ✅ w/ provenance | ✅ raw material for skills | ✅ when verified & de-duped | only after generalizing |
| **Trajectory (failure)** | ✅ hindsight signal | ✅ after reflection → heuristics | ⚠️ amplifies brittle shortcuts | often the right home |
| **Reflection** | ✅ primary store | ✅ when reflections cluster into a rule | sparingly (overfits) | forget single-use ones |
| **Self-generated task** | briefly | rarely (the *solution* is the artifact) | ✅ curriculum for self-play RL | drop no-signal tasks |
| **Peer / pseudo-label** | ✅ as in-context examples | ✅ distill a population → one agent | ✅ test-time RL when calibrated | quarantine low-trust |
| **Adversarial / corrupted** | never | never | never | **always** (revoke) |

---

## 📊 Evaluating change over time

A self-updating agent can't be judged by one static test pass. The survey proposes a
**Seven-Property Evaluation Framework** and names **Benchmark-Experience Contamination (BEC)** —
leakage where evaluation tasks update the agent's *persistent state* (invisible to a single
snapshot, and distinct from classical train-set contamination).

**Seven properties** any change-over-time benchmark should report:
`forward transfer` · `backward transfer` · `plasticity–stability` · `memory & retrieval cost over time` ·
`skill-reuse rate` · `hidden-shortcutting (PIPE-style)` · `adversarial robustness of accumulated experience`.

A `rollback-and-rerun` delta is the recommended default BEC probe.

### Lifelong-agent benchmarks

<!-- BEGIN:BENCHMARKS -->
_generated_
<!-- END:BENCHMARKS -->

---

## 📚 Related surveys

How the prior surveys map onto the lifecycle (this is the companion to the survey's Table 1).

<!-- BEGIN:RELATED -->
_generated_
<!-- END:RELATED -->

## Foundations & background

> Classic, pre-agent work that the lifecycle builds on (continual learning, RL, adaptation,
> retrieval, tool use). Not experience-driven lifelong-agent systems themselves — included as
> grounding (cf. survey §2.7).

<!-- BEGIN:FOUNDATIONS -->
_generated_
<!-- END:FOUNDATIONS -->

## Framing & position pieces

<!-- BEGIN:FRAMING -->
_generated_
<!-- END:FRAMING -->

---

## 🔭 Open problems

Condensed from the survey's agenda — each phrased in lifecycle vocabulary:

1. **Experience provenance & lineage** (cross-cutting) — trace an observed behavior back to the artifact that caused it.
2. **Evaluating change-over-time without BEC** — a community suite with the seven properties + rollback-and-rerun.
3. **Internalization vs. retrieval** — where should experience live? (S3 vs S6)
4. **When does memory help vs. hurt?** (S3 / S5 / S6)
5. **Does memory→skill abstraction transfer out-of-domain?** (S5)
6. **Governance primitives for persistent agents** — provenance, attestation, revocation, quarantine, audit.
7. **Detecting obsolete skills & stale memories** (S5 / S7)
8. **Self-generated experience & capability elicitation vs. creation** (S1 / S6)
9. **Scaling laws for experience-driven learning** (S1 / S6)
10. **Multi-agent experience composition** (S8) — and **what makes a "good" memory** (S2 / S4 / S7).

> **Meta-problem:** the community needs a shared **experience-pipeline substrate** — a schema for
> trajectories, memories, skills, and provenance — so contributions become directly comparable.

---

## 📝 Citation

If this list or the survey helped your work, please cite:

```bibtex
@article{he2026experiencelifecycle,
  title   = {Learning From Experience: A Lifecycle Survey of Memory, Skills,
             and Self-Evolution in Lifelong LLM Agents},
  author  = {He, Eva and others},
  year    = {2026},
  journal = {arXiv preprint arXiv:XXXX.XXXXX},
  note    = {https://github.com/EvaxHe/Awesome-LLM-Agent-Experience-Lifecycle}
}
```

<!-- TODO: replace arXiv id + author list once the paper is posted. -->

## 🤝 Contributing

PRs welcome! The list is **generated from a CSV** — see [CONTRIBUTING.md](CONTRIBUTING.md).
In short: edit [`data/literature_matrix.csv`](data/literature_matrix.csv), run
`python scripts/build_readme.py`, and commit both files. Star counts and the "last verified"
date refresh automatically each week.

## ⭐ Star history

<a href="https://star-history.com/#EvaxHe/Awesome-LLM-Agent-Experience-Lifecycle&Date">
  <img src="https://api.star-history.com/svg?repos=EvaxHe/Awesome-LLM-Agent-Experience-Lifecycle&type=Date" width="600" alt="Star History Chart">
</a>

---

<div align="center">
<sub>Last verified {{LAST_VERIFIED}} · built from <code>data/literature_matrix.csv</code> by <code>scripts/build_readme.py</code></sub>
</div>
