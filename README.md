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
**90 systems** across the 8 stages (7 cross-cutting) · **14 benchmarks** · **9 governance/threat papers** · **14 related surveys** · last verified **2026-07-27**

<sub>Per-stage counts (systems may appear under more than one stage): S1 27 · S2 20 · S3 19 · S4 25 · S5 31 · S6 44 · S7 4 · S8 19</sub>
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
### <a id="s1"></a>S1 — Acquisition  ·  `27 systems`

> What experience is collected — trajectories, outcomes, reflections, self-generated tasks, peer feedback, pseudo-labels.

| Year | Title | Venue | What's updated | Key contribution | Code |
| :---: | --- | --- | --- | --- | :---: |
| 2026 | [Absolute Zero: Reinforced Self-Play Reasoning with Zero Data](https://arxiv.org/abs/2505.03335) | NeurIPS 38 | Weights | Zero-human-data RL training |  |
| 2026 | [Agent Evolving Learning for Open-Ended Environments](https://arxiv.org/html/2604.21725v1) | arXiv 2604.21725 | Memory + tools | Open-ended evolutionary learning |  |
| 2026 | [GeoEvolver: Experience-Driven Multi-Agent Earth Observation](https://arxiv.org/html/2602.02559) | arXiv 2602.02559 | Memory + tools | Domain-specific multi-agent experience |  |
| 2026 | [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084) | NeurIPS 38 | Weights at test time | Test-time RL surpassing own supervision ceiling |  |
| 2026 | [SEAL: Synergistic Co-Evolution of Agents and Learning Environments](https://huggingface.co/papers/2605.24426) | HuggingFace papers 2605.24426 | Policy + environment | Curriculum co-evolution |  |
| 2026 | [End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents](https://arxiv.org/abs/2605.10663) | arXiv 2605.10663 | Memory + weights | End-to-end self-evolution |  |
| 2026 | [A Self-Evolving GUI Agent Learning via Failed Experience](https://arxiv.org/html/2603.24533) | arXiv 2603.24533 | Weights | Learning from failure |  |
| 2025 | [Abductive Reasoning Path Synthesis for Training RAG Agents](https://arxiv.org/html/2509.23071v1) | arXiv 2509.23071 | Weights | Process-level supervision |  |
| 2025 | [AgentEvolver: Towards Efficient Self-Evolving Agent System](https://github.com/modelscope/AgentEvolver) | GitHub | Weights | Self-evolution framework | [![stars](https://img.shields.io/github/stars/modelscope/AgentEvolver?style=flat&logo=github&label=%E2%98%85&color=ffd700)](https://github.com/modelscope/AgentEvolver) |
| 2025 | [Automating Agent Creation via Agent Debate](https://arxiv.org/html/2503.23781v1) | arXiv 2503.23781 | Workflow | Debate-driven workflow generation |  |
| 2025 | [Continual Learning for Coding Agents](https://arxiv.org/html/2507.00014) | arXiv 2507.00014 | Memory + weights | Continual coding |  |
| 2025 | [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](https://arxiv.org/abs/2510.16079) | arXiv 2510.16079 | Memory + weights | Explicit experience-driven lifecycle | [code](https://huggingface.co/Edaizi/EvolveR) |
| 2025 | [Hindsight Experience Replay for LLM Agent Trajectory Relabeling](https://arxiv.org/abs/2603.21357v1) | arXiv 2603.21357 | Replay buffer | Goal relabeling for LM agents |  |
| 2025 | [Multi-Agent Evolve (MAE)](https://arxiv.org/abs/2510.23595) | arXiv | Weights | Co-evolution dynamics |  |
| 2025 | [Optimizing Multi-Agent RAG through Self-Training](https://arxiv.org/html/2506.10844) | arXiv 2506.10844 | Weights | Self-training MA-RAG |  |
| 2025 | [Play2Prompt: Zero-Shot Tool Discovery](https://arxiv.org/abs/2503.14432) | arXiv | Prompt + memory | Discover tools without docs |  |
| 2025 | [SEAL: Self-Adapting Language Models](https://arxiv.org/html/2506.10943v1) | arXiv 2506.10943 | Weights | Persistent self-edits via RL | [![stars](https://img.shields.io/github/stars/Continual-Intelligence/SEAL?style=flat&logo=github&label=%E2%98%85&color=ffd700)](https://github.com/Continual-Intelligence/SEAL) |
| 2025 | [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) | arXiv 2506.04651 | Memory + weights | Long-horizon strategic eval |  |
| 2025 | [Self-Questioning Agents (AgentEvolver self-questioning component)](https://arxiv.org/abs/2508.03682) | arXiv | Tasks | Self-generated curricula |  |
| 2025 | [Synthesizing Agent Trajectories via Test-Time Exploration under Validate-by-Reproduce](https://arxiv.org/html/2510.00415v1) | arXiv 2510.00415 | External + weights | Synthetic trajectories |  |
| 2025 | [ECHO: Sample-Efficient Online Learning in LM Agents via Hindsight Trajectory Rewriting](https://arxiv.org/html/2510.10304v1) | arXiv 2510.10304 | External demonstration store + ICL | HER-for-LM-agents formulation |  |
| 2024 | [Self-Taught Evaluators](https://arxiv.org/abs/2408.02666) | arXiv | Weights | Match GPT-4 as judge |  |
| 2023 | [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144) | arXiv 2308.10144 | External insight library | Insight extraction across tasks | [![stars](https://img.shields.io/github/stars/LeapLabTHU/ExpeL?style=flat&logo=github&label=%E2%98%85&color=ffd700)](https://github.com/LeapLabTHU/ExpeL) |
| 2023 | [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | NeurIPS 2023 | External episodic notes | Verbal RL substitute for parameter updates |  |
| 2023 | [Toolformer: Language Models Can Teach Themselves to Use Tools](https://proceedings.neurips.cc/paper_files/paper/2023/file/d842425e4bf79ba039352da0f658a906-Paper-Conference.pdf) | NeurIPS 2023:68539-68551 | Weights | Self-supervised tool learning |  |
| 2023 | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | NeurIPS 2023 / arXiv 2305.16291 | External skill library | First lifelong agent with reusable skill library | [code](https://voyager.minedojo.org/) |

### <a id="s2"></a>S2 — Representation  ·  `20 systems`

> How collected experience is stored — typed records, graph notes, skill files, workflow graphs, tool descriptors, parametric encodings.

| Year | Title | Venue | What's updated | Key contribution | Code |
| :---: | --- | --- | --- | --- | :---: |
| 2026 | [Agent Evolving Learning for Open-Ended Environments](https://arxiv.org/html/2604.21725v1) | arXiv 2604.21725 | Memory + tools | Open-ended evolutionary learning |  |
| 2025 | [A-MEM: Zettelkasten-Inspired Self-Organizing Memory for LLM Agents](https://arxiv.org/abs/2502.12110) | arXiv | External memory | Self-organizing memory |  |
| 2025 | [Beyond One-Shot Diagnosis with Agents That Remember Reflect and Improve](https://arxiv.org/html/2604.14475v1) | arXiv 2604.14475 | Memory | Memory-reflective med agent |  |
| 2025 | [Continual Learning for Coding Agents](https://arxiv.org/html/2507.00014) | arXiv 2507.00014 | Memory + weights | Continual coding |  |
| 2025 | [End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents](https://arxiv.org/abs/2605.10663) | arXiv 2605.10663 | Memory + weights | End-to-end self-evolution |  |
| 2025 | [ENGRAM: Lightweight Memory Orchestration for Conversational Agents](https://arxiv.org/html/2511.12960v1) | arXiv 2511.12960 | External memory | Lightweight typed memory router |  |
| 2025 | [Episodic-Semantic Memory Architecture for Long-Horizon Scientific Agents](https://arxiv.org/html/2605.17625v1) | arXiv 2605.17625 | External memory | Episodic+semantic split for science |  |
| 2025 | [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](https://arxiv.org/abs/2510.16079) | arXiv 2510.16079 | Memory + weights | Explicit experience-driven lifecycle | [code](https://huggingface.co/Edaizi/EvolveR) |
| 2025 | [Get Experience from Practice: AgentRR (Record & Replay)](https://arxiv.org/abs/2505.17716) | arXiv 2505.17716 | External record | Record-replay paradigm |  |
| 2025 | [Large Memory Models LM2](https://arxiv.org/abs/2502.06049) | arXiv | Architecture + memory | +37% over recurrent memory transformers |  |
| 2025 | [MaRS: A Cognitive Memory Architecture and Benchmark for Privacy-Aware Generative Agents](https://arxiv.org/html/2512.12856v1) | arXiv 2512.12856 | External memory + provenance | Privacy + provenance + retention schema |  |
| 2025 | [Mem0/Mem0g: Production-grade memory for agents](https://arxiv.org/abs/2504.19413) | arXiv 2504.19413 | External memory | 91% latency reduction |  |
| 2025 | [MemInsight: Structured Memory Augmentation for Agents](https://arxiv.org/abs/2503.21760) | arXiv | External memory | +34% recall over RAG |  |
| 2025 | [MemOS: An Operating System for Memory](https://arxiv.org/abs/2507.03724) | arXiv | External memory | Memory OS abstraction |  |
| 2025 | [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) | arXiv 2506.04651 | Memory + weights | Long-horizon strategic eval |  |
| 2025 | [ToolGen: Tools as Tokens](https://arxiv.org/abs/2410.03439) | arXiv | Vocabulary | Vocabulary-level tool fusion |  |
| 2023 | [Generative Agents: Interactive Simulacra of Human Behavior](https://dl.acm.org/doi/10.1145/3586183.3606763) | UIST 2023 | External memory stream | Architecture: memory stream + reflection + planning |  |
| 2023 | [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | NeurIPS 2023 | External episodic notes | Verbal RL substitute for parameter updates |  |
| 2023 | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | NeurIPS 2023 / arXiv 2305.16291 | External skill library | First lifelong agent with reusable skill library | [code](https://voyager.minedojo.org/) |

### <a id="s3"></a>S3 — Retrieval & Use  ·  `19 systems`

> How stored experience is surfaced for the current task — similarity, attribute, learned, hierarchical, and hindsight-conditioned retrieval.

| Year | Title | Venue | What's updated | Key contribution | Code |
| :---: | --- | --- | --- | --- | :---: |
| 2026 | [Agent Evolving Learning for Open-Ended Environments](https://arxiv.org/html/2604.21725v1) | arXiv 2604.21725 | Memory + tools | Open-ended evolutionary learning |  |
| 2026 | [Learning to Retrieve from Agent Trajectories](https://arxiv.org/html/2604.04949v1) | arXiv 2604.04949 | Retriever weights | Trajectory-aware retrieval |  |
| 2026 | [Trajectory-Informed Memory Generation for Self-Improving Agent Systems](https://arxiv.org/html/2603.10600) | arXiv 2603.10600 | External tip memory | Sub-task vs task-level memory comparison |  |
| 2025 | [Chain-of-Tools: Frozen LLM with Tool Retrieval](https://arxiv.org/abs/2503.16779) | arXiv | External tool retriever | Frozen LM with retrieval |  |
| 2025 | [Continual Learning for Coding Agents](https://arxiv.org/html/2507.00014) | arXiv 2507.00014 | Memory + weights | Continual coding |  |
| 2025 | [End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents](https://arxiv.org/abs/2605.10663) | arXiv 2605.10663 | Memory + weights | End-to-end self-evolution |  |
| 2025 | [ENGRAM: Lightweight Memory Orchestration for Conversational Agents](https://arxiv.org/html/2511.12960v1) | arXiv 2511.12960 | External memory | Lightweight typed memory router |  |
| 2025 | [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](https://arxiv.org/abs/2510.16079) | arXiv 2510.16079 | Memory + weights | Explicit experience-driven lifecycle | [code](https://huggingface.co/Edaizi/EvolveR) |
| 2025 | [GAE-Retriever / WebRAGent: RAG for Multimodal Web Agent Planning](https://openreview.net/forum?id=L1VPZFbAcu) | OpenReview | External + ICL | +15% gain via retrieved knowledge |  |
| 2025 | [Get Experience from Practice: AgentRR (Record & Replay)](https://arxiv.org/abs/2505.17716) | arXiv 2505.17716 | External record | Record-replay paradigm |  |
| 2025 | [MemInsight: Structured Memory Augmentation for Agents](https://arxiv.org/abs/2503.21760) | arXiv | External memory | +34% recall over RAG |  |
| 2025 | [REGENT: A Retrieval-Augmented Generalist Agent That Can Act In-Context in New Environments](https://openreview.net/forum?id=NxyfSW6mLK) | ICLR 2025 | External + ICL | 3x fewer parameters via retrieval |  |
| 2025 | [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) | arXiv 2506.04651 | Memory + weights | Long-horizon strategic eval |  |
| 2024 | [RAHL: Retrieval-Augmented Hierarchical In-Context RL](https://arxiv.org/abs/2408.06520) | arXiv 2408.06520 | ICL + retrieval | 9-42% improvement via retrieval |  |
| 2024 | [VLM Agents Generate Their Own Memories: Distilling Experience into Embodied Programs of Thought](https://proceedings.neurips.cc/paper_files/paper/2024/file/8ac50fd0a4eeeb1f077b17bb7c5353c3-Paper-Conference.pdf) | NeurIPS 2024 | External insights | Trajectory-to-insight pipeline |  |
| 2023 | [Generative Agents: Interactive Simulacra of Human Behavior](https://dl.acm.org/doi/10.1145/3586183.3606763) | UIST 2023 | External memory stream | Architecture: memory stream + reflection + planning |  |
| 2023 | [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | NeurIPS 2023 | External episodic notes | Verbal RL substitute for parameter updates |  |
| 2023 | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | NeurIPS 2023 / arXiv 2305.16291 | External skill library | First lifelong agent with reusable skill library | [code](https://voyager.minedojo.org/) |

### <a id="s4"></a>S4 — Consolidation  ·  `25 systems`

> How transient memories become durable — summarization, reflection, salience scoring, note-linking, RL-driven consolidation, compression.

| Year | Title | Venue | What's updated | Key contribution | Code |
| :---: | --- | --- | --- | --- | :---: |
| 2026 | [Agent Evolving Learning for Open-Ended Environments](https://arxiv.org/html/2604.21725v1) | arXiv 2604.21725 | Memory + tools | Open-ended evolutionary learning |  |
| 2026 | [CoWork-X: Experience-Optimized Multi-Agent Co-Evolution](https://arxiv.org/abs/2602.05004) | arXiv | Memory + weights | Fast-slow co-evolution |  |
| 2026 | [Experiential Reflective Learning for Self-Improving LLM Agents (ERL)](https://arxiv.org/html/2603.24639) | ICLR 2026 Workshop on Memory for LLM-Based Agentic Systems | External heuristic store | Lightweight task adaptation via heuristics |  |
| 2026 | [Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification](https://doi.org/10.48550/arXiv.2601.15808) | CoRR abs/2601.15808 | Memory + prompts | Plug-and-play test-time self-evolution |  |
| 2026 | [Trajectory-Informed Memory Generation for Self-Improving Agent Systems](https://arxiv.org/html/2603.10600) | arXiv 2603.10600 | External tip memory | Sub-task vs task-level memory comparison |  |
| 2025 | [A Self-Optimizing Agent with Dynamic Hierarchical Workflow](https://arxiv.org/html/2508.02959) | arXiv 2508.02959 | Workflow | Workflow self-optimization |  |
| 2025 | [A-MEM: Zettelkasten-Inspired Self-Organizing Memory for LLM Agents](https://arxiv.org/abs/2502.12110) | arXiv | External memory | Self-organizing memory |  |
| 2025 | [Beyond One-Shot Diagnosis with Agents That Remember Reflect and Improve](https://arxiv.org/html/2604.14475v1) | arXiv 2604.14475 | Memory | Memory-reflective med agent |  |
| 2025 | [Continual Learning for Coding Agents](https://arxiv.org/html/2507.00014) | arXiv 2507.00014 | Memory + weights | Continual coding |  |
| 2025 | [End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents](https://arxiv.org/abs/2605.10663) | arXiv 2605.10663 | Memory + weights | End-to-end self-evolution |  |
| 2025 | [Episodic-Semantic Memory Architecture for Long-Horizon Scientific Agents](https://arxiv.org/html/2605.17625v1) | arXiv 2605.17625 | External memory | Episodic+semantic split for science |  |
| 2025 | [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](https://arxiv.org/abs/2510.16079) | arXiv 2510.16079 | Memory + weights | Explicit experience-driven lifecycle | [code](https://huggingface.co/Edaizi/EvolveR) |
| 2025 | [Internalizing Agency from Reflective Experience](https://arxiv.org/html/2603.16843v1) | arXiv 2603.16843 | Weights + memory | Reflection-driven internalization |  |
| 2025 | [LightThinker: Reasoning Compression](https://arxiv.org/abs/2502.15589) | arXiv | Memory | 70% memory reduction |  |
| 2025 | [MEM1: RL-Trained Memory Consolidation](https://arxiv.org/abs/2506.15841) | arXiv | External memory | 3.7× less memory; 1.78× faster |  |
| 2025 | [Meta-Reflexion](https://arxiv.org/abs/2405.13009) | arXiv | External meta-memory | Hierarchical reflection |  |
| 2025 | [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) | arXiv 2506.04651 | Memory + weights | Long-horizon strategic eval |  |
| 2024 | [ECHO: Sample-Efficient Online Learning in LM Agents via Hindsight Trajectory Rewriting](https://arxiv.org/html/2510.10304v1) | arXiv 2510.10304 | External demonstration store + ICL | HER-for-LM-agents formulation |  |
| 2024 | [RAHL: Retrieval-Augmented Hierarchical In-Context RL](https://arxiv.org/abs/2408.06520) | arXiv 2408.06520 | ICL + retrieval | 9-42% improvement via retrieval |  |
| 2024 | [VLM Agents Generate Their Own Memories: Distilling Experience into Embodied Programs of Thought](https://proceedings.neurips.cc/paper_files/paper/2024/file/8ac50fd0a4eeeb1f077b17bb7c5353c3-Paper-Conference.pdf) | NeurIPS 2024 | External insights | Trajectory-to-insight pipeline |  |
| 2023 | [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144) | arXiv 2308.10144 | External insight library | Insight extraction across tasks | [![stars](https://img.shields.io/github/stars/LeapLabTHU/ExpeL?style=flat&logo=github&label=%E2%98%85&color=ffd700)](https://github.com/LeapLabTHU/ExpeL) |
| 2023 | [Generative Agents: Interactive Simulacra of Human Behavior](https://dl.acm.org/doi/10.1145/3586183.3606763) | UIST 2023 | External memory stream | Architecture: memory stream + reflection + planning |  |
| 2023 | [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | NeurIPS 2023 | External episodic notes | Verbal RL substitute for parameter updates |  |
| 2023 | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | NeurIPS 2023 / arXiv 2305.16291 | External skill library | First lifelong agent with reusable skill library | [code](https://voyager.minedojo.org/) |

### <a id="s5"></a>S5 — Abstraction  ·  `31 systems`

> How experience becomes reusable capability — skills, heuristics, procedural templates, workflows, tools.

| Year | Title | Venue | What's updated | Key contribution | Code |
| :---: | --- | --- | --- | --- | :---: |
| 2026 | [Agent Evolving Learning for Open-Ended Environments](https://arxiv.org/html/2604.21725v1) | arXiv 2604.21725 | Memory + tools | Open-ended evolutionary learning |  |
| 2026 | [EvoTool](https://arxiv.org/abs/2603.04900) | arXiv | Tool registry | Tools-from-experience |  |
| 2026 | [Experiential Reflective Learning for Self-Improving LLM Agents (ERL)](https://arxiv.org/html/2603.24639) | ICLR 2026 Workshop on Memory for LLM-Based Agentic Systems | External heuristic store | Lightweight task adaptation via heuristics |  |
| 2026 | [FactorMiner](https://arxiv.org/abs/2602.14670) | arXiv | External factor library | Reusable factor abstraction |  |
| 2026 | [GeoEvolver: Experience-Driven Multi-Agent Earth Observation](https://arxiv.org/html/2602.02559) | arXiv 2602.02559 | Memory + tools | Domain-specific multi-agent experience |  |
| 2026 | [The Single-Multi Evolution Loop](https://arxiv.org/abs/2602.05182) | arXiv | Weights | Single-multi loop |  |
| 2026 | [Trajectory-Informed Memory Generation for Self-Improving Agent Systems](https://arxiv.org/html/2603.10600) | arXiv 2603.10600 | External tip memory | Sub-task vs task-level memory comparison |  |
| 2026 | [Unified Evolution of Skill-Augmented Agents via RL](https://arxiv.org/html/2605.06130v3) | arXiv 2605.06130 | Skills + weights | Skill+RL unified |  |
| 2025 | [A Self-Optimizing Agent with Dynamic Hierarchical Workflow](https://arxiv.org/html/2508.02959) | arXiv 2508.02959 | Workflow | Workflow self-optimization |  |
| 2025 | [A-MEM: Zettelkasten-Inspired Self-Organizing Memory for LLM Agents](https://arxiv.org/abs/2502.12110) | arXiv | External memory | Self-organizing memory |  |
| 2025 | [AdaptFlow: Adaptive Workflow Optimization via Meta-Learning](https://arxiv.org/html/2508.08053) | arXiv 2508.08053 | Workflow | Generalizable workflow init |  |
| 2025 | [AFlow: MCTS over Code-Represented Workflows](https://arxiv.org/abs/2410.10762) | arXiv | Workflow graph | 5.7% over manual workflows |  |
| 2025 | [AgentEvolver: Towards Efficient Self-Evolving Agent System](https://github.com/modelscope/AgentEvolver) | GitHub | Weights | Self-evolution framework | [![stars](https://img.shields.io/github/stars/modelscope/AgentEvolver?style=flat&logo=github&label=%E2%98%85&color=ffd700)](https://github.com/modelscope/AgentEvolver) |
| 2025 | [Alita: Autonomous MCP Construction](https://arxiv.org/abs/2505.20286) | arXiv | Tool registry | Autonomous tool creation |  |
| 2025 | [Automating Agent Creation via Agent Debate](https://arxiv.org/html/2503.23781v1) | arXiv 2503.23781 | Workflow | Debate-driven workflow generation |  |
| 2025 | [Beyond One-Shot Diagnosis with Agents That Remember Reflect and Improve](https://arxiv.org/html/2604.14475v1) | arXiv 2604.14475 | Memory | Memory-reflective med agent |  |
| 2025 | [Continual Learning for Coding Agents](https://arxiv.org/html/2507.00014) | arXiv 2507.00014 | Memory + weights | Continual coding |  |
| 2025 | [End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents](https://arxiv.org/abs/2605.10663) | arXiv 2605.10663 | Memory + weights | End-to-end self-evolution |  |
| 2025 | [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](https://arxiv.org/abs/2510.16079) | arXiv 2510.16079 | Memory + weights | Explicit experience-driven lifecycle | [code](https://huggingface.co/Edaizi/EvolveR) |
| 2025 | [Hermes Agent: Persistent Skills for Personal AI](https://www.turingpost.com/p/hermes) | Industry blog | Skill files | Persistent personal-agent skills |  |
| 2025 | [Internalizing Agency from Reflective Experience](https://arxiv.org/html/2603.16843v1) | arXiv 2603.16843 | Weights + memory | Reflection-driven internalization |  |
| 2025 | [LIMO: Less Is More for Reasoning](https://arxiv.org/abs/2502.03387) | arXiv | Weights | 817 trajectories unlock reasoning |  |
| 2025 | [MaAS: Agentic Supernet](https://arxiv.org/abs/2502.04180) | arXiv | Architecture | 6-45% cost of baselines |  |
| 2025 | [OpenClaw Agent Skills (SKILL.md)](https://skywork.ai/blog/ai-bot/claude-example-skills-library-ultimate-guide/) | Industry blog | Skill files | Modular skill library |  |
| 2025 | [Play2Prompt: Zero-Shot Tool Discovery](https://arxiv.org/abs/2503.14432) | arXiv | Prompt + memory | Discover tools without docs |  |
| 2025 | [Reinforcement Learning Teachers of Test Time Scaling](https://proceedings.neurips.cc/paper_files/paper/2025/file/9a6b278218966499194491f55ccf8b75-Paper-Conference.pdf) | NeurIPS 2025 | Teacher weights | Teacher quality decoupled from solver capability |  |
| 2025 | [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) | arXiv 2506.04651 | Memory + weights | Long-horizon strategic eval |  |
| 2024 | [VLM Agents Generate Their Own Memories: Distilling Experience into Embodied Programs of Thought](https://proceedings.neurips.cc/paper_files/paper/2024/file/8ac50fd0a4eeeb1f077b17bb7c5353c3-Paper-Conference.pdf) | NeurIPS 2024 | External insights | Trajectory-to-insight pipeline |  |
| 2023 | [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144) | arXiv 2308.10144 | External insight library | Insight extraction across tasks | [![stars](https://img.shields.io/github/stars/LeapLabTHU/ExpeL?style=flat&logo=github&label=%E2%98%85&color=ffd700)](https://github.com/LeapLabTHU/ExpeL) |
| 2023 | [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) | NeurIPS 2023 / arXiv 2305.16291 | External skill library | First lifelong agent with reusable skill library | [code](https://voyager.minedojo.org/) |

### <a id="s6"></a>S6 — Internalization  ·  `44 systems`

> How experience becomes parameters — trajectory-SFT, RL with verifiable rewards, self-edits, test-time training, adapter selection, distillation.

| Year | Title | Venue | What's updated | Key contribution | Code |
| :---: | --- | --- | --- | --- | :---: |
| 2026 | [Absolute Zero: Reinforced Self-Play Reasoning with Zero Data](https://arxiv.org/abs/2505.03335) | NeurIPS 38 | Weights | Zero-human-data RL training |  |
| 2026 | [Adaptive Compute Allocation for Code Generation via Test-Time Training](https://arxiv.org/html/2601.00894) | arXiv 2601.00894 | Weights | Training-free gating for TTT |  |
| 2026 | [CoWork-X: Experience-Optimized Multi-Agent Co-Evolution](https://arxiv.org/abs/2602.05004) | arXiv | Memory + weights | Fast-slow co-evolution |  |
| 2026 | [Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification](https://doi.org/10.48550/arXiv.2601.15808) | CoRR abs/2601.15808 | Memory + prompts | Plug-and-play test-time self-evolution |  |
| 2026 | [SECL: Self-Calibrating LMs via Test-Time Discriminative Distillation](https://arxiv.org/abs/2604.09624) | arXiv 2604.09624 | Weights | Selective test-time adaptation |  |
| 2026 | [The Single-Multi Evolution Loop](https://arxiv.org/abs/2602.05182) | arXiv | Weights | Single-multi loop |  |
| 2026 | [TTRL: Test-Time Reinforcement Learning](https://arxiv.org/abs/2504.16084) | NeurIPS 38 | Weights at test time | Test-time RL surpassing own supervision ceiling |  |
| 2026 | [Unified Evolution of Skill-Augmented Agents via RL](https://arxiv.org/html/2605.06130v3) | arXiv 2605.06130 | Skills + weights | Skill+RL unified |  |
| 2026 | [What Do Agents Learn from Trajectory-SFT (PIPE)](https://arxiv.org/html/2602.01611v1) | arXiv 2602.01611 | Weights | Trajectory-SFT amplifies interface shortcutting |  |
| 2025 | [A Self-Evolving GUI Agent Learning via Failed Experience](https://arxiv.org/html/2603.24533) | arXiv 2603.24533 | Weights | Learning from failure |  |
| 2025 | [Abductive Reasoning Path Synthesis for Training RAG Agents](https://arxiv.org/html/2509.23071v1) | arXiv 2509.23071 | Weights | Process-level supervision |  |
| 2025 | [AdaptFlow: Adaptive Workflow Optimization via Meta-Learning](https://arxiv.org/html/2508.08053) | arXiv 2508.08053 | Workflow | Generalizable workflow init |  |
| 2025 | [AFlow: MCTS over Code-Represented Workflows](https://arxiv.org/abs/2410.10762) | arXiv | Workflow graph | 5.7% over manual workflows |  |
| 2025 | [AgentEvolver: Towards Efficient Self-Evolving Agent System](https://github.com/modelscope/AgentEvolver) | GitHub | Weights | Self-evolution framework | [![stars](https://img.shields.io/github/stars/modelscope/AgentEvolver?style=flat&logo=github&label=%E2%98%85&color=ffd700)](https://github.com/modelscope/AgentEvolver) |
| 2025 | [Continual Learning for Coding Agents](https://arxiv.org/html/2507.00014) | arXiv 2507.00014 | Memory + weights | Continual coding |  |
| 2025 | [DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning](https://doi.org/10.1038/s41586-025-09422-z) | Nature 645(8081):633-638 | Weights | Pure RL produces strong reasoning |  |
| 2025 | [End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents](https://arxiv.org/abs/2605.10663) | arXiv 2605.10663 | Memory + weights | End-to-end self-evolution |  |
| 2025 | [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](https://arxiv.org/abs/2510.16079) | arXiv 2510.16079 | Memory + weights | Explicit experience-driven lifecycle | [code](https://huggingface.co/Edaizi/EvolveR) |
| 2025 | [Hindsight Experience Replay for LLM Agent Trajectory Relabeling](https://arxiv.org/abs/2603.21357v1) | arXiv 2603.21357 | Replay buffer | Goal relabeling for LM agents |  |
| 2025 | [Internalizing Agency from Reflective Experience](https://arxiv.org/html/2603.16843v1) | arXiv 2603.16843 | Weights + memory | Reflection-driven internalization |  |
| 2025 | [LIMO: Less Is More for Reasoning](https://arxiv.org/abs/2502.03387) | arXiv | Weights | 817 trajectories unlock reasoning |  |
| 2025 | [Multi-Agent Evolve (MAE)](https://arxiv.org/abs/2510.23595) | arXiv | Weights | Co-evolution dynamics |  |
| 2025 | [Nemotron Tool-N1](https://arxiv.org/abs/2505.00024) | arXiv | Weights | Outperforms GPT-4o on tool-use |  |
| 2025 | [Open-Reasoner-Zero: An Open Source Approach to Scaling Up Reinforcement Learning on the Base Model](https://doi.org/10.48550/arXiv.2503.24290) | CoRR abs/2503.24290 | Weights | 1/30 training steps of R1-Zero |  |
| 2025 | [OpenHands Trajectories with Qwen3-Coder-480B-A35B-Instruct](https://nebius.com/blog/posts/openhands-trajectories-with-qwen3-coder-480b) | Nebius blog | Weights | Production RFT recipe |  |
| 2025 | [Optima: Optimizing Effectiveness and Efficiency for LLM-Based Multi-Agent System](https://aclanthology.org/2025.findings-acl.601/) | Findings of ACL 2025 | Weights | 2.8x performance with <10% tokens |  |
| 2025 | [Optimizing Multi-Agent RAG through Self-Training](https://arxiv.org/html/2506.10844) | arXiv 2506.10844 | Weights | Self-training MA-RAG |  |
| 2025 | [QwenLong-L1: Progressive Context Scaling](https://arxiv.org/abs/2505.17667) | arXiv | Weights + context | Scaling to 120K tokens |  |
| 2025 | [Reinforcement Learning Teachers of Test Time Scaling](https://proceedings.neurips.cc/paper_files/paper/2025/file/9a6b278218966499194491f55ccf8b75-Paper-Conference.pdf) | NeurIPS 2025 | Teacher weights | Teacher quality decoupled from solver capability |  |
| 2025 | [RL for Search-Efficient LLMs](https://arxiv.org/abs/2505.07903) | arXiv | Weights | Learn when to search |  |
| 2025 | [SEAL: Self-Adapting Language Models](https://arxiv.org/html/2506.10943v1) | arXiv 2506.10943 | Weights | Persistent self-edits via RL | [![stars](https://img.shields.io/github/stars/Continual-Intelligence/SEAL?style=flat&logo=github&label=%E2%98%85&color=ffd700)](https://github.com/Continual-Intelligence/SEAL) |
| 2025 | [SEAL: Synergistic Co-Evolution of Agents and Learning Environments](https://huggingface.co/papers/2605.24426) | HuggingFace papers 2605.24426 | Policy + environment | Curriculum co-evolution |  |
| 2025 | [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) | arXiv 2506.04651 | Memory + weights | Long-horizon strategic eval |  |
| 2025 | [Self-Taught Evaluators](https://arxiv.org/abs/2408.02666) | arXiv | Weights | Match GPT-4 as judge |  |
| 2025 | [Synthesizing Agent Trajectories via Test-Time Exploration under Validate-by-Reproduce](https://arxiv.org/html/2510.00415v1) | arXiv 2510.00415 | External + weights | Synthetic trajectories |  |
| 2025 | [Test-Time Learning for Large Language Models](https://arxiv.org/abs/2505.20633) | arXiv 2505.20633 | Weights | Self-supervised TTT |  |
| 2025 | [Text-to-LoRA](https://arxiv.org/abs/2506.06105) | arXiv | Adapter weights | Generated adapters |  |
| 2025 | [The Surprising Effectiveness of Test-Time Training for Few-Shot Learning](https://icml.cc/virtual/2025/poster/44773) | ICML 2025 | Weights at test time | TTT works for LM few-shot |  |
| 2025 | [Trajectory Balance with Asynchrony: Decoupling Exploration and Learning for Fast Scalable LLM Post-Training](https://proceedings.neurips.cc/paper_files/paper/2025/file/a58e6bd468ae63efd8c95035ea55ee41-Paper-Conference.pdf) | NeurIPS 2025 | Weights | Scalable replay-buffer RL |  |
| 2025 | [Transformer²: Self-Adaptive LLMs](https://arxiv.org/abs/2501.06252) | arXiv | Architecture (expert routing) | Architectural runtime adaptation |  |
| 2025 | [ZeroSearch](https://arxiv.org/abs/2505.04588) | arXiv | Weights | RL without real search |  |
| 2024 | [ECHO: Sample-Efficient Online Learning in LM Agents via Hindsight Trajectory Rewriting](https://arxiv.org/html/2510.10304v1) | arXiv 2510.10304 | External demonstration store + ICL | HER-for-LM-agents formulation |  |
| 2023 | [Toolformer: Language Models Can Teach Themselves to Use Tools](https://proceedings.neurips.cc/paper_files/paper/2023/file/d842425e4bf79ba039352da0f658a906-Paper-Conference.pdf) | NeurIPS 2023:68539-68551 | Weights | Self-supervised tool learning |  |

### <a id="s7"></a>S7 — Revision & Forgetting  ·  `4 systems`

> How stale, wrong, or harmful experience is removed — memory editing, unlearning, drift correction.

| Year | Title | Venue | What's updated | Key contribution | Code |
| :---: | --- | --- | --- | --- | :---: |
| 2025 | [Continual Learning for Coding Agents](https://arxiv.org/html/2507.00014) | arXiv 2507.00014 | Memory + weights | Continual coding |  |
| 2025 | [MemOS: An Operating System for Memory](https://arxiv.org/abs/2507.03724) | arXiv | External memory | Memory OS abstraction |  |
| 2025 | [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) | arXiv 2506.04651 | Memory + weights | Long-horizon strategic eval |  |

### <a id="s8"></a>S8 — Distribution  ·  `19 systems`

> How experience moves across agents, users, teams, and repositories — multi-agent sharing, federated pools, protocols, skill registries.

| Year | Title | Venue | What's updated | Key contribution | Code |
| :---: | --- | --- | --- | --- | :---: |
| 2026 | [CoWork-X: Experience-Optimized Multi-Agent Co-Evolution](https://arxiv.org/abs/2602.05004) | arXiv | Memory + weights | Fast-slow co-evolution |  |
| 2026 | [EvoTool](https://arxiv.org/abs/2603.04900) | arXiv | Tool registry | Tools-from-experience |  |
| 2026 | [Privacy-Preserving Multi-Agent Memory with Bayesian Trust Defense](https://arxiv.org/html/2603.02240v1) | arXiv 2603.02240 | Memory | Privacy-preserving multi-agent memory |  |
| 2026 | [The Single-Multi Evolution Loop](https://arxiv.org/abs/2602.05182) | arXiv | Weights | Single-multi loop |  |
| 2025 | [AgentRxiv: Parallel AI Research Labs](https://arxiv.org/abs/2503.18102) | arXiv | Memory + skills | +13.7% via shared research |  |
| 2025 | [Alita: Autonomous MCP Construction](https://arxiv.org/abs/2505.20286) | arXiv | Tool registry | Autonomous tool creation |  |
| 2025 | [Hermes Agent: Persistent Skills for Personal AI](https://www.turingpost.com/p/hermes) | Industry blog | Skill files | Persistent personal-agent skills |  |
| 2025 | [Leaky Thoughts: Reasoning Traces Leak Private Data](https://arxiv.org/abs/2506.15674) | arXiv | Trace | Reasoning traces leak data |  |
| 2025 | [MaRS: A Cognitive Memory Architecture and Benchmark for Privacy-Aware Generative Agents](https://arxiv.org/html/2512.12856v1) | arXiv 2512.12856 | External memory + provenance | Privacy + provenance + retention schema |  |
| 2025 | [MINJA: Memory Injection Attack](https://arxiv.org/html/2601.05504v1) | arXiv 2601.05504 | Memory | >95% injection success |  |
| 2025 | [Multi-Agent Evolve (MAE)](https://arxiv.org/abs/2510.23595) | arXiv | Weights | Co-evolution dynamics |  |
| 2025 | [Optima: Optimizing Effectiveness and Efficiency for LLM-Based Multi-Agent System](https://aclanthology.org/2025.findings-acl.601/) | Findings of ACL 2025 | Weights | 2.8x performance with <10% tokens |  |
| 2025 | [Persistent Compromise of LLM Agents via Poisoned Experience Retrieval](https://arxiv.org/html/2512.16962) | arXiv 2512.16962 | Experience store | Persistent compromise via retrieval |  |
| 2025 | [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) | arXiv 2506.04651 | Memory + weights | Long-horizon strategic eval |  |
| 2025 | [Self-Taught Evaluators](https://arxiv.org/abs/2408.02666) | arXiv | Weights | Match GPT-4 as judge |  |
| 2025 | [Sleeper Memory Poisoning in LLM Agents](https://arxiv.org/abs/2605.15338) | arXiv 2605.15338 | Memory | 60-89% attack success on retrieved memories |  |
| 2025 | [Weaponizing Agent Memory for Data Exfiltration](https://arxiv.org/html/2605.01970v2) | arXiv 2605.01970 | Memory | Memory as exfil channel |  |
| 2025 | [When Memory Poisoning Looks Like Model Failure in Agentic AI](https://arxiv.org/abs/2605.22842) | arXiv 2605.22842 | Memory | 87.5% causal entry detection accuracy |  |

<!-- END:STAGES -->

## Cross-cutting frameworks

> Systems whose experience pipeline spans most of the lifecycle (≥5 stages) — closed-loop
> self-evolving agents and broad frameworks.

<!-- BEGIN:CROSSCUT -->
- [Agent Evolving Learning for Open-Ended Environments](https://arxiv.org/html/2604.21725v1) — *Open-ended evolutionary learning* <sub>(S1, S2, S3, S4, S5)</sub>
- [Continual Learning for Coding Agents](https://arxiv.org/html/2507.00014) — *Continual coding* <sub>(S1, S2, S3, S4, S5, S6, S7)</sub>
- [End-to-End Optimization of Experience-Driven Self-Evolving Capability within Agents](https://arxiv.org/abs/2605.10663) — *End-to-end self-evolution* <sub>(S1, S2, S3, S4, S5, S6)</sub>
- [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](https://arxiv.org/abs/2510.16079) — *Explicit experience-driven lifecycle* <sub>(S1, S2, S3, S4, S5, S6)</sub>
- [Self-Evolving LLM Agents for Strategic Planning](https://arxiv.org/html/2506.04651) — *Long-horizon strategic eval* <sub>(S1, S2, S3, S4, S5, S6, S7, S8)</sub>
- [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) — *First lifelong agent with reusable skill library* <sub>(S1, S2, S3, S4, S5)</sub>
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
<p align="center"><sub>The survey's <strong>§2.8</strong> corpus (Table C2): the same 90 systems the stage tables are built from, each cell counting a system in every stage it spans (so columns need not sum to 90). Fully reproducible — see <a href="reproducibility/"><code>reproducibility/corpus_coding.py</code></a>.</sub></p>

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
| Year | Paper | Venue | Threat / defense |
| :---: | --- | --- | --- |
| 2026 | [Privacy-Preserving Multi-Agent Memory with Bayesian Trust Defense](https://arxiv.org/html/2603.02240v1) | arXiv 2603.02240 | Privacy-preserving multi-agent memory |
| 2025 | [Leaky Thoughts: Reasoning Traces Leak Private Data](https://arxiv.org/abs/2506.15674) | arXiv | Reasoning traces leak data |
| 2025 | [MaRS: A Cognitive Memory Architecture and Benchmark for Privacy-Aware Generative Agents](https://arxiv.org/html/2512.12856v1) | arXiv 2512.12856 | Privacy + provenance + retention schema |
| 2025 | [MemOS: An Operating System for Memory](https://arxiv.org/abs/2507.03724) | arXiv | Memory OS abstraction |
| 2025 | [MINJA: Memory Injection Attack](https://arxiv.org/html/2601.05504v1) | arXiv 2601.05504 | >95% injection success |
| 2025 | [Persistent Compromise of LLM Agents via Poisoned Experience Retrieval](https://arxiv.org/html/2512.16962) | arXiv 2512.16962 | Persistent compromise via retrieval |
| 2025 | [Sleeper Memory Poisoning in LLM Agents](https://arxiv.org/abs/2605.15338) | arXiv 2605.15338 | 60-89% attack success on retrieved memories |
| 2025 | [Weaponizing Agent Memory for Data Exfiltration](https://arxiv.org/html/2605.01970v2) | arXiv 2605.01970 | Memory as exfil channel |
| 2025 | [When Memory Poisoning Looks Like Model Failure in Agentic AI](https://arxiv.org/abs/2605.22842) | arXiv 2605.22842 | 87.5% causal entry detection accuracy |
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
| Year | Benchmark | Domain | Change axis | Key signal | BEC discipline |
| :---: | --- | --- | --- | --- | --- |
| 2026 | [GeoEvolver](https://arxiv.org/abs/2602.02559) | Earth observation (multi-agent) | Domain shift | Domain-specific MA experience | Some (natural domain drift) |
| 2026 | [LOCA-Bench](https://arxiv.org/abs/2602.07962) | Language agents | Controllable context growth | Context-management strategies | Limited |
| 2025 | [Continual Coding](https://arxiv.org/abs/2507.00014) | Coding agents | Issue stream | Continual code-fix | Some (issues evolve naturally) |
| 2025 | [Continuous Benchmark Generation](https://arxiv.org/abs/2511.10049) | Enterprise agents | Dynamic benchmarks | Enterprise-scale | Strong (generates per-agent) |
| 2025 | [LifelongAgentBench](https://arxiv.org/abs/2505.11942) | Tool-using agents | Sequential task stream | Group self-consistency | Limited |
| 2025 | [Long-Horizon Office Workflows](https://arxiv.org/abs/2508.09124) | Office agents | End-to-end workflow | Long-horizon tasks | Limited |
| 2025 | [MACEval](https://arxiv.org/abs/2511.09139) | Multi-LLM eval | Continual eval | Multi-agent role-assigned eval | Some (continuous design) |
| 2025 | [Self-Evolving Memory Benchmark](https://arxiv.org/abs/2511.20857) | Test-time learning + memory | Test-time learning | Self-evolving memory | Limited |
| 2025 | [SHADE-Arena (adversarial)](https://arxiv.org/abs/2506.15740) | Multi-agent | Adversarial | Saboteur vs. monitor | Strong (adversarial structure resists memorization) |
| 2025 | [Strategic Catan](https://arxiv.org/abs/2506.04651) | Strategic planning | Adversarial stochastic | Long-horizon strategy | Some (stochastic env reduces direct memorization) |
| 2024 | [BABILong](https://proceedings.neurips.cc/paper_files/paper/2024/file/c0d62e70dbc659cc9bd44cbcf1cb652f-Paper-Datasets_and_Benchmarks_Track.pdf) | Long-context reasoning | Document length | Memory-augmented retrieval | Static-style only |
| 2024 | [Dynamic Conversational Benchmarking](https://doi.org/10.52202/079017-1347) | Conversational | Task interleaving | LTM benefit | Limited |
| 2024 | [LOCOMO](https://arxiv.org/abs/2402.17753) | Conversational | Long-term memory | Multi-session conversation | Static-style only |
| 2024 | [LongMemEval](https://arxiv.org/abs/2410.10813) | Conversational (chat assistants) | Long-term memory with knowledge updates | Interactive long-term memory across sessions | Static-style only |

**Seven-property coverage** (Table 15b) — ● full · ◐ partial · ○ none:

| Benchmark | Fwd xfer | Bwd xfer | Plast/Stab | Mem cost | Skill reuse | Shortcut | Adv-rob |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| GeoEvolver | ◐ | ○ | ○ | ○ | ○ | ○ | ○ |
| LOCA-Bench | ○ | ○ | ○ | ● | ○ | ○ | ○ |
| Continual Coding | ● | ● | ● | ○ | ○ | ○ | ○ |
| Continuous Benchmark Generation | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| LifelongAgentBench | ◐ | ◐ | ○ | ◐ | ○ | ○ | ○ |
| Long-Horizon Office Workflows | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| MACEval | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Self-Evolving Memory Benchmark | ◐ | ○ | ○ | ◐ | ○ | ○ | ○ |
| SHADE-Arena (adversarial) | ○ | ○ | ○ | ○ | ○ | ○ | ● |
| Strategic Catan | ◐ | ○ | ○ | ○ | ○ | ○ | ○ |
| BABILong | ○ | ○ | ○ | ◐ | ○ | ○ | ○ |
| Dynamic Conversational Benchmarking | ○ | ○ | ○ | ◐ | ○ | ○ | ○ |
| LOCOMO | ○ | ○ | ○ | ◐ | ○ | ○ | ○ |
| LongMemEval | ◐ | ○ | ○ | ◐ | ○ | ○ | ○ |
<!-- END:BENCHMARKS -->

---

## 📚 Related surveys

How the prior surveys map onto the lifecycle (this is the companion to the survey's Table 1).

<!-- BEGIN:RELATED -->
| Year | Survey | Venue | How it relates to the lifecycle |
| :---: | --- | --- | --- |
| 2026 | [From Static Templates to Dynamic Runtime Graphs: A Survey of Workflow Optimization for LLM Agents](https://arxiv.org/html/2603.22386) | arXiv 2603.22386 | Cross-reference for stage 5 abstraction (workflow extraction) |
| 2026 | [From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms](https://arxiv.org/html/2605.06716v1) | arXiv 2605.06716 / ICLR 2026 | Closest framing; their three stages = our stages 2 4 5; we add 1 3 6 7 8 |
| 2026 | [Lifelong Learning of Large Language Model based Agents: A Roadmap](https://doi.org/10.1109/TPAMI.2025.3650546) | IEEE TPAMI 48(5):5552-5571 | Complementary module view; we reorganize across modules by experience flow |
| 2026 | [Mechanisms Evaluation and Emerging Frontiers (Agent Memory)](https://arxiv.org/abs/2603.07670) | arXiv 2603.07670 | Cross-reference for stage 2 details |
| 2025 | [A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems](https://arxiv.org/abs/2508.07407) | arXiv 2508.07407 | Complementary; we extend loop into eight pipeline stages |
| 2025 | [A Survey of Self-Evolving Agents: On the Path to Artificial Super Intelligence](https://arxiv.org/abs/2507.21046v2) | arXiv 2507.21046 | Closest competitor; we add experience-lifecycle axis |
| 2025 | [A Unified Survey on Memory Systems from Cognitive Neuroscience to Autonomous Agents](https://arxiv.org/html/2512.23343v1) | arXiv 2512.23343 | Cited for cognitive grounding of episodic/semantic/procedural distinction |
| 2025 | [Adaptation of Agentic AI: A Survey of Post-Training Memory and Skills](https://arxiv.org/abs/2512.16301) | arXiv 2512.16301 | Comparison — Closest in content; we make the pillars sequential stages of one pipeline |
| 2025 | [Advances in Foundation Agents](https://arxiv.org/abs/2504.01990) | arXiv | Background context |
| 2025 | [Beyond Pipelines: A Survey of the Paradigm Shift toward Model-Native Agentic AI](http://huggingface.co/papers/2510.16720) | arXiv 2510.16720 | Comparison — Cited for stage 6 internalization context |
| 2025 | [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) | arXiv 2512.13564 | Cross-reference for stage 2 evaluation |
| 2025 | [The Landscape of Agentic Reinforcement Learning for LLMs](https://arxiv.org/abs/2509.02547) | arXiv 2509.02547 | Comparison — Cross-reference for stage 6 RL methods |
| 2024 | [A Survey on Self-Evolution of Large Language Models](https://arxiv.org/html/2404.14387v1) | arXiv 2404.14387 | Predecessor; we extend to agents and to 2025-26 literature |
| 2024 | [A Survey on the Memory Mechanism of LLM-based Agents](https://arxiv.org/abs/2404.13501) | arXiv | Foundational; cited heavily for stage 2 vocabulary |
<!-- END:RELATED -->

## Foundations & background

> Classic, pre-agent work that the lifecycle builds on (continual learning, RL, adaptation,
> retrieval, tool use). Not experience-driven lifelong-agent systems themselves — included as
> grounding (cf. survey §2.7).

<!-- BEGIN:FOUNDATIONS -->
| Year | Paper | Venue | Why it's here |
| :---: | --- | --- | --- |
| 2026 | [Characterizing an Emergent Learning Community at Scale](https://arxiv.org/html/2602.18832v1) | arXiv 2602.18832 | 2.8M agents in 3 weeks |
| 2025 | [GRPO: Group Relative Policy Optimization](https://arxiv.org/abs/2402.03300) | arXiv | Practical RL algorithm |
| 2023 | [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) | ICLR | ReAct paradigm |
| 2022 | [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) | ICLR | Foundational PEFT |
| 2022 | [RLHF: Training Language Models to Follow Instructions with Human Feedback](https://arxiv.org/abs/2203.02155) | NeurIPS | Foundational RLHF |
| 2020 | [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | NeurIPS | Foundational RAG |
| 2017 | [Mastering the Game of Go without Human Knowledge](https://www.nature.com/articles/nature24270) | Nature | Self-play to superhuman |
| 2016 | [Emergent Communication in Multi-Agent RL](https://arxiv.org/abs/1605.06676) | NeurIPS | Emergent communication |
<!-- END:FOUNDATIONS -->

## Framing & position pieces

<!-- BEGIN:FRAMING -->
- [Active Inference in the Era of Experience](https://arxiv.org/abs/2508.05619) — *Theoretical complement to era of experience*
- [Forecasting Rare LLM Behaviors](https://arxiv.org/abs/2502.16797) — *Forecasting rare behaviors*
- [From Secure Agentic AI to Secure Agentic Web](https://arxiv.org/html/2603.01564v1) — *Security framework*
- [Procedural Memory Is Not All You Need](https://doi.org/10.1145/3708319.3734172) — *Argues against pure procedural memory*
- [Welcome to the Era of Experience](https://theaiinnovator.com/welcome-to-the-era-of-experience/) — *Names the paradigm we survey*
- [Language Models Are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — *Emergent ICL*
- [AI-Generating Algorithms](https://arxiv.org/abs/1905.10985) — *Foundational AI-GA framework*
- [Experience Replay for Continual Learning](https://proceedings.neurips.cc/paper/2019/hash/fa7cdfad1a5aaf8370ebeda47a1ff1c3-Abstract.html) — *Replay for continual learning*
- [Model-Agnostic Meta-Learning](https://arxiv.org/abs/1703.03400) — *Foundational meta-learning*
- [Why Greatness Cannot Be Planned](https://doi.org/10.1007/978-3-319-15524-1) — *Foundational open-ended evolution*
- [Gödel Machines](https://arxiv.org/abs/cs/0309048) — *Theoretical foundation*
- [Catastrophic Interference in Connectionist Networks](https://doi.org/10.1016/S0079-7421(08)60536-8) — *Foundational forgetting*
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
<sub>Last verified 2026-07-27 · built from <code>data/literature_matrix.csv</code> by <code>scripts/build_readme.py</code></sub>
</div>
