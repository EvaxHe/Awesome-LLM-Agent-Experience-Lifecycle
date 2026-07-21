#!/usr/bin/env python3
"""
Corpus-level coding for the "Learning From Experience" survey (§2.8, Tables C1-C3).

Reproducible secondary coding of literature_matrix.csv (this folder) along four axes:
  - lifecycle stage   (parsed from the matrix's `lifecycle_stage`, multi-hot)
  - update surface     (canonicalized; SURFACE dict below)
  - update timing      (train / online / test-time; TIMING dict, coded from matrix text)
  - topology           (single / team / population; non-single in TOPOLOGY dict)
  - governance         (defense / threat / none; non-none in GOVERNANCE dict)

NOTE ON METHOD. Stage coding derives from the matrix's `lifecycle_stage`. The
~28 borderline calls (the EXCLUDE boundary, Memory-vs-Skill surface splits,
update timing, the team/population topology split, and governance) were each
verified against the system's PRIMARY SOURCE, and the 12 headline-moving calls
(governance, exclusions, the insight->Skill rule) were additionally re-checked
adversarially. Verdicts and evidence: verify-corpus-coding workflow run. EXCLUDE
drops rows that are not experience-driven agent systems (eval frameworks,
datasets, no-persistent-state methods, pre-LLM/foundational algorithms) per the
§2.6 inclusion criteria. Edit the dicts and re-run to rescore.

Usage:  python3 corpus_coding.py   (run from this folder)
Writes: corpus_coding.csv (per-system codes) and prints Tables C1-C3.
"""
import csv, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATRIX = HERE / "literature_matrix.csv"
OUT = HERE / "corpus_coding.csv"
from collections import Counter, defaultdict

# --- rows that are NOT experience-driven agent systems (drop from corpus) ------
EXCLUDE = {
    "mctrl_2025", "office_long_horizon_2025", "shade_arena_2025",
    "benchmarking_continuous_2025",            # eval frameworks / benchmarks
    "ell_stulife_2025",                          # dataset / simulation, not a system
    "yao2023react", "lewis2020rag",             # no persistent agent-updated state
    "ouyang2022rlhf", "hu2022lora", "grpo2025", # foundational technique/algorithm
    "foerster2016emergent", "silver2017alphagozero",  # pre-LLM, cited for lineage
    "characterizing_emergent_2026",             # empirical measurement study
}

# --- canonical update surface(s) per system -----------------------------------
SURFACE = {
    "voyager2023": {"Skill"}, "park2023generativeagents": {"Memory"},
    "shinn2023reflexion": {"Memory"}, "zhao2023expel": {"Memory", "Skill"},
    "marc2026experiential": {"Skill"}, "fang2026trajectory": {"Memory"},
    "xu2025internalizing": {"Memory", "Weights"}, "echo2024hindsight": {"Memory"},
    "her2025relabel": {"Memory"}, "seal2025": {"Weights"},
    "seal2025coevolution": {"Weights"}, "zhao2026absolute": {"Weights"},
    "zuo2026ttrl": {"Weights"}, "ttt2025fewshot": {"Weights"},
    "transformer2_2025": {"Weights"}, "texttolora2025": {"Weights"},
    "cetin2025reinforcement": {"Weights"}, "limo2025": {"Weights"}, "guo2025deepseek": {"Weights"},
    "hu2025open": {"Weights"}, "piperesearch2026": {"Weights"},
    "trofimova2025openhandstrajs": {"Weights"}, "selfevol_gui_2025": {"Weights"},
    "evolver2025": {"Memory", "Weights"}, "agentevolver2025": {"Weights"},
    "e2e_self_evolve_2025": {"Memory", "Weights"}, "mem0_2025": {"Memory"},
    "amem2025": {"Memory"}, "meminsight2025": {"Memory"}, "mem1_2025": {"Memory"},
    "memos2025": {"Memory"}, "lm2_2025": {"Memory", "Weights"},
    "qwenlong_l1_2025": {"Weights"}, "engram2025": {"Memory"},
    "mars2025": {"Memory"}, "episode_semantic_2025": {"Memory"},
    "sridhar2025regent": {"Memory"}, "rahl2024": {"Memory"}, "gae_retriever_2025": {"Memory"},
    "learn_to_retrieve_2026": {"Weights"}, "evolving_open_ended_2026": {"Memory", "Tool"},
    "factorminer_2026": {"Memory", "Skill"}, "metareflex_2025": {"Memory"},
    "evotool_2026": {"Tool"}, "alita2025": {"Tool"}, "toolgen_2025": {"Weights"},
    "play2prompt_2025": {"Memory", "Skill"}, "nemotron_tool_n1_2025": {"Weights"},
    "chain_of_tools_2025": {"Tool"}, "aflow_2025": {"Workflow"}, "maas_2025": {"Workflow"},
    "adaptflow_2025": {"Workflow"}, "self_optim_dynamic_workflow_2025": {"Workflow"},
    "agentdebate_workflow_2025": {"Workflow"}, "agentrr_2025": {"Memory"},
    "strategic_planning_catan_2025": {"Memory", "Weights"}, "wan2026inference": {"Memory"},
    "continual_coding_2025": {"Memory", "Weights"}, "minja_2025": {"Memory"},
    "sleeper_memory_2025": {"Memory"}, "when_memory_poisoning_2025": {"Memory"},
    "weaponizing_memory_2025": {"Memory"}, "poisoned_experience_retrieval_2025": {"Memory"},
    "leaky_thoughts_2025": {"Memory"}, "privacy_multi_agent_2026": {"Memory"},
    "agentrxiv_2025": {"Memory", "Skill"}, "mae_2025": {"Weights"},
    "chen2025optima": {"Weights"}, "single_multi_loop_2026": {"Weights"},
    "cowork_x_2026": {"Memory", "Weights"}, "sarch2024ical": {"Memory"},
    "multiagent_rag_self_train_2025": {"Weights"}, "abductive_rag_2025": {"Weights"},
    "beyond_one_shot_med_2025": {"Memory"}, "geoevolver_2026": {"Memory", "Tool"},
    "self_calibrating_test_time_2026": {"Weights"}, "adaptive_compute_test_time_2026": {"Weights"},
    "test_time_learning_2025": {"Weights"}, "rl_search_efficient_2025": {"Weights"},
    "zerosearch_2025": {"Weights"}, "self_taught_evaluators_2025": {"Weights"},
    "self_questioning_2025": {"Weights"}, "schick2023toolformer": {"Weights"},
    "lightthinker_2025": {"Memory"}, "hermes_skills_2025": {"Skill"},
    "openclaw_skills_2025": {"Skill"}, "unified_evolution_skill_rl_2026": {"Skill", "Weights"},
    "synthesizing_trajectories_2025": {"Memory", "Weights"}, "bartoldson2025trajectory": {"Weights"},
    "selfevolving_strategic_planning_2025": {"Memory", "Weights"},
}

# --- update timing: when the persistent update happens -------------------------
TIMING = {
    "voyager2023": "online", "park2023generativeagents": "online",
    "shinn2023reflexion": "online", "zhao2023expel": "train", "marc2026experiential": "online",
    "fang2026trajectory": "online", "xu2025internalizing": "train",
    "echo2024hindsight": "online", "her2025relabel": "train", "seal2025": "train",
    "seal2025coevolution": "train", "zhao2026absolute": "train", "zuo2026ttrl": "test",
    "ttt2025fewshot": "test", "transformer2_2025": "test", "texttolora2025": "test",
    "cetin2025reinforcement": "train", "limo2025": "train", "guo2025deepseek": "train",
    "hu2025open": "train", "piperesearch2026": "train", "trofimova2025openhandstrajs": "train",
    "selfevol_gui_2025": "train", "evolver2025": "train", "agentevolver2025": "train",
    "e2e_self_evolve_2025": "train", "mem0_2025": "online", "amem2025": "online",
    "meminsight2025": "online", "mem1_2025": "online", "memos2025": "online",
    "lm2_2025": "train", "qwenlong_l1_2025": "train", "engram2025": "online",
    "mars2025": "online", "episode_semantic_2025": "online", "sridhar2025regent": "test",
    "rahl2024": "online", "gae_retriever_2025": "test", "learn_to_retrieve_2026": "train",
    "evolving_open_ended_2026": "online", "factorminer_2026": "online",
    "metareflex_2025": "online", "evotool_2026": "online", "alita2025": "online",
    "toolgen_2025": "train", "play2prompt_2025": "online", "nemotron_tool_n1_2025": "train",
    "chain_of_tools_2025": "test", "aflow_2025": "train", "maas_2025": "train",
    "adaptflow_2025": "train", "self_optim_dynamic_workflow_2025": "online",
    "agentdebate_workflow_2025": "train", "agentrr_2025": "online",
    "strategic_planning_catan_2025": "online", "wan2026inference": "test",
    "continual_coding_2025": "online", "minja_2025": "online", "sleeper_memory_2025": "online",
    "when_memory_poisoning_2025": "online", "weaponizing_memory_2025": "online",
    "poisoned_experience_retrieval_2025": "online", "leaky_thoughts_2025": "online",
    "privacy_multi_agent_2026": "online", "agentrxiv_2025": "online", "mae_2025": "train",
    "chen2025optima": "train", "single_multi_loop_2026": "train", "cowork_x_2026": "online",
    "sarch2024ical": "online", "multiagent_rag_self_train_2025": "train",
    "abductive_rag_2025": "train", "beyond_one_shot_med_2025": "online",
    "geoevolver_2026": "online", "self_calibrating_test_time_2026": "test",
    "adaptive_compute_test_time_2026": "test", "test_time_learning_2025": "test",
    "rl_search_efficient_2025": "train", "zerosearch_2025": "train",
    "self_taught_evaluators_2025": "train", "self_questioning_2025": "train",
    "schick2023toolformer": "train", "lightthinker_2025": "online",
    "hermes_skills_2025": "online", "openclaw_skills_2025": "online",
    "unified_evolution_skill_rl_2026": "online", "synthesizing_trajectories_2025": "test",
    "bartoldson2025trajectory": "train", "selfevolving_strategic_planning_2025": "online",
}

# --- topology: only non-single listed (default = single-agent) -----------------
TOPOLOGY = {
    "park2023generativeagents": "population",
    "maas_2025": "team", "agentrxiv_2025": "team",
    "mae_2025": "team", "chen2025optima": "team", "single_multi_loop_2026": "team",
    "cowork_x_2026": "team", "multiagent_rag_self_train_2025": "team",
    "geoevolver_2026": "team", "privacy_multi_agent_2026": "team",
    "agentdebate_workflow_2025": "team",
}

# --- governance: only non-none listed (default = none) -------------------------
GOVERNANCE = {
    "mars2025": "defense", "memos2025": "defense", "privacy_multi_agent_2026": "defense",
    "when_memory_poisoning_2025": "defense",
    "minja_2025": "threat", "sleeper_memory_2025": "threat",
    "weaponizing_memory_2025": "threat", "poisoned_experience_retrieval_2025": "threat",
    "leaky_thoughts_2025": "threat",
}

STAGE_NAMES = {1: "Acquisition", 2: "Representation", 3: "Retrieval/Use",
               4: "Consolidation", 5: "Abstraction", 6: "Internalization",
               7: "Revision", 8: "Distribution"}
SURFACES = ["Memory", "Skill", "Workflow", "Tool", "Weights"]


def parse_stages(s):
    out = set()
    for a, b in re.findall(r"(\d)\s*-\s*(\d)", s):
        out.update(range(int(a), int(b) + 1))
    for d in re.findall(r"\d", re.sub(r"\d\s*-\s*\d", "", s)):
        out.add(int(d))
    return {x for x in out if 1 <= x <= 8}


def main():
    rows = list(csv.DictReader(open(MATRIX)))
    systems = [r for r in rows if r["bibkey"] not in EXCLUDE
               and r["agent_type"] not in ("Survey", "Position", "Benchmark", "Conceptual")
               and r["lifecycle_stage"] not in ("Comparison", "Framing")]

    # integrity check: every included system must be coded
    missing = [r["bibkey"] for r in systems if r["bibkey"] not in SURFACE
               or r["bibkey"] not in TIMING]
    assert not missing, f"Uncoded systems: {missing}"

    n = len(systems)
    stage_ct, surf_ct, timing_ct, topo_ct, gov_ct = (Counter() for _ in range(5))
    mat = defaultdict(Counter)
    out_rows = []
    for r in systems:
        bk = r["bibkey"]
        stages = parse_stages(r["lifecycle_stage"])
        surfaces = SURFACE[bk]
        timing = TIMING[bk]
        topo = TOPOLOGY.get(bk, "single")
        gov = GOVERNANCE.get(bk, "none")
        for st in stages:
            stage_ct[st] += 1
            for su in surfaces:
                mat[st][su] += 1
        for su in surfaces:
            surf_ct[su] += 1
        timing_ct[timing] += 1
        topo_ct[topo] += 1
        gov_ct[gov] += 1
        out_rows.append({"bibkey": bk, "stages": " ".join(map(str, sorted(stages))),
                         "surfaces": "|".join(sorted(surfaces)), "timing": timing,
                         "topology": topo, "governance": gov})

    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["bibkey", "stages", "surfaces", "timing",
                                          "topology", "governance"])
        w.writeheader(); w.writerows(out_rows)

    print(f"N systems (after EXCLUDE): {n}\n")
    print("== Table C1: by lifecycle stage (multi-hot) ==")
    for s in range(1, 9):
        print(f"  S{s} {STAGE_NAMES[s]:15s} {stage_ct[s]:3d}  ({stage_ct[s]/n*100:.0f}%)")
    print("\n== Table C2: stage x surface ==")
    print("        " + " ".join(f"{c[:4]:>5}" for c in SURFACES))
    for s in range(1, 9):
        print(f"  S{s}   " + " ".join(f"{mat[s][c]:5d}" for c in SURFACES))
    print("  TOT  " + " ".join(f"{surf_ct[c]:5d}" for c in SURFACES))
    print("\n== Table C3 ==")
    print("  timing:    ", dict(timing_ct))
    print("  topology:  ", dict(topo_ct))
    print("  governance:", dict(gov_ct))

if __name__ == "__main__":
    main()
