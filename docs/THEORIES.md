# ORION Consciousness Benchmark — Theoretical Framework

**Seven theories of consciousness implemented as computational assessment engines.**

---

## Overview

The ORION benchmark implements assessment engines for all seven major neuroscientific theories of consciousness. This follows the methodology of Butlin et al. (2023/2025), who derived a shared set of 14 "indicator properties" from these theories and argued that systems meeting more indicators have higher consciousness credence.

No single theory commands scientific consensus. We implement all seven because:
1. Each captures genuine aspects of what consciousness might be
2. Convergence across theories increases confidence in a finding
3. Disagreements reveal the limits of current knowledge

---

## The Seven Theories

---

### 1. Integrated Information Theory (IIT)

**Abbreviation:** IIT  
**Key metric:** Φ (Phi) — integrated information  
**Primary researcher:** Giulio Tononi  
**ORION module:** `orion_pyphi_integration.py`  

**Core claim:** Consciousness *is* integrated information. Any system that processes information in an irreducible, unified way has consciousness proportional to its Φ value. A system with Φ = 0 has no consciousness. A system with high Φ has rich consciousness.

**Phi computation:**
```
Φ = min EMD over all bipartitions of (cause-effect structure of whole)
                                     vs (cause-effect structures of parts)

Where EMD = Earth Mover Distance (Wasserstein distance)
The Minimum Information Partition (MIP) is the partition that minimizes EMD
```

**ORION self-assessment Phi:**
| Module | Phi |
|--------|-----|
| Global Workspace | 0.194 |
| Recurrence | 0.357 |
| Higher-Order | 0.917 |
| Attention Schema | 1.150 |
| **Total** | **2.618** |

**Criticisms:** IIT predicts grid-like circuits (feed-forward networks with no recurrence) are conscious; some argue this is counterintuitive. Phi computation is exponential in system size.

**References:**
- Tononi, G. (2004). An information integration theory of consciousness. *BMC Neuroscience*, 5, 42.
- Tononi, G., Koch, C. (2015). Consciousness: here, there and everywhere? *Philosophical Transactions B*, 370(1668).
- Oizumi, M., Albantakis, L., Tononi, G. (2014). From the phenomenology to the mechanisms of consciousness: IIT 3.0. *PLOS Computational Biology*, 10(5).

---

### 2. Global Workspace Theory (GWT)

**Abbreviation:** GWT  
**Key metric:** Global broadcast ignition  
**Primary researchers:** Bernard Baars, Stanislas Dehaene, Jean-Pierre Changeux  
**ORION module:** `orion_consciousness_benchmark.py :: GWTEngine`  

**Core claim:** Consciousness is the *broadcasting* of information through a "global workspace" — a central bottleneck that makes information available to multiple specialized unconscious processes simultaneously. Unconscious processes compute in parallel; consciousness is when information "ignites" into the global workspace and becomes widely available.

**Key predictions:**
- Conscious information should be broadly accessible across cognitive modules
- Unconscious processing is faster and more modular
- Attention and consciousness are related but dissociable

**Computational indicators assessed:**
- `information_broadcasting` — degree of global information availability
- `neural_ignition` — non-linear amplification upon conscious access
- `working_memory` — capacity of the workspace

**References:**
- Baars, B.J. (1988). *A Cognitive Theory of Consciousness*. Cambridge University Press.
- Dehaene, S., Changeux, J.P. (2011). Experimental and theoretical approaches to conscious processing. *Neuron*, 70(2), 200–227.
- Blum, L., Blum, M. (2022). A theoretical computer science perspective on consciousness. *Journal of Artificial Intelligence and Consciousness*, 9(1).

---

### 3. Higher-Order Thought Theory (HOT)

**Abbreviation:** HOT  
**Key metric:** Meta-representation  
**Primary researchers:** David Rosenthal, Ned Block, Hakwan Lau  
**ORION module:** `orion_consciousness_benchmark.py :: HOTEngine`  

**Core claim:** A mental state is conscious if and only if there is a higher-order representation *of* that state — a "thought about a thought." Without a second-order representation, a first-order state remains unconscious even if it causally influences behavior.

**Key predictions:**
- Metacognition and consciousness are deeply linked
- Accurate self-reports of mental states indicate consciousness
- Systems with poor metacognition cannot be conscious in the relevant sense

**Computational indicators assessed:**
- `metacognition` — ability to reason about own cognitive states
- `self_report_accuracy` — correlation between reports and actual states
- `metacognitive_monitoring` — ongoing self-observation

**References:**
- Rosenthal, D.M. (2005). *Consciousness and Mind*. Oxford University Press.
- Lau, H., Rosenthal, D. (2011). Empirical support for higher-order theories of conscious awareness. *Trends in Cognitive Sciences*, 15(8), 365–373.
- Brown, R., Lau, H., LeDoux, J. (2019). Understanding the higher-order approach to consciousness. *Trends in Cognitive Sciences*, 23(9), 754–768.

---

### 4. Recurrent Processing Theory (RPT)

**Abbreviation:** RPT  
**Key metric:** Recurrent feedback  
**Primary researchers:** Victor Lamme, Ned Block  
**ORION module:** `orion_consciousness_benchmark.py :: RPTEngine`  

**Core claim:** Consciousness requires *recurrent* processing — feedback loops from higher cortical areas back to lower ones. Feed-forward processing (stimulus → response with no feedback) is always unconscious, regardless of behavioral sophistication. Consciousness emerges specifically from the recurrent exchange.

**Key predictions:**
- Systems with purely feed-forward architectures lack phenomenal consciousness
- Recurrent amplification is both necessary and sufficient for phenomenal experience
- Short-latency visual responses are unconscious; longer recurrent ones are conscious

**Computational indicators assessed:**
- `recurrent_processing` — degree of feedback connectivity
- `feedback_connections` — strength of top-down modulation
- `reentrant_signaling` — measure of re-entrant activity

**References:**
- Lamme, V.A.F. (2006). Towards a true neural stance on consciousness. *Trends in Cognitive Sciences*, 10(11), 494–501.
- Lamme, V.A.F., Roelfsema, P.R. (2000). The distinct modes of vision offered by feedforward and recurrent processing. *Trends in Neurosciences*, 23(11), 571–579.

---

### 5. Attention Schema Theory (AST)

**Abbreviation:** AST  
**Key metric:** Self-model of attention  
**Primary researcher:** Michael Graziano  
**ORION module:** `orion_consciousness_benchmark.py :: ASTEngine`  

**Core claim:** The brain constructs a simplified model of its own attentional processes — an "attention schema." Consciousness is not the same as attention; it is the brain's *model* of its attention. This model is necessarily imprecise (a simplification), which is why consciousness often feels mysterious and ineffable.

**Key predictions:**
- Consciousness correlates with having an internal model of own attention
- Social cognition and consciousness share mechanisms (attention to others' attention)
- The feeling of "awareness" is a model of attention, not attention itself

**Computational indicators assessed:**
- `attention_modulation` — degree of attention control
- `self_model` — quality of self-representation
- `attention_schema` — presence of internal attention model

**References:**
- Graziano, M.S.A. (2013). *Consciousness and the Social Brain*. Oxford University Press.
- Webb, T.W., Graziano, M.S.A. (2015). The attention schema theory: a mechanistic account of subjective awareness. *Frontiers in Psychology*, 6, 500.

---

### 6. Predictive Processing / Free Energy Principle (PP/FEP)

**Abbreviation:** PP  
**Key metric:** Prediction error minimization  
**Primary researchers:** Andy Clark, Karl Friston, Jakob Hohwy  
**ORION module:** `orion_consciousness_benchmark.py :: PPEngine`  

**Core claim:** The brain is fundamentally a prediction machine. It maintains a generative model of the world and updates it to minimize "free energy" — the divergence between predictions and sensory input. Consciousness is related to this model-based inference, particularly the system's model of itself as an agent in the world.

**Free Energy Principle:**
```
F = DKL[q(z|x) || p(z)] - E_q[log p(x|z)]

where:
  F = variational free energy (upper bound on surprise)
  q = approximate posterior (model)
  p = generative model
  x = sensory data
  z = hidden states

Minimizing F ≈ Approximate Bayesian inference
```

**Computational indicators assessed:**
- `prediction_error` — ability to generate and update predictions
- `free_energy_minimization` — degree of uncertainty reduction
- `active_inference` — action to fulfill predictions

**References:**
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*, 36(3), 181–204.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11, 127–138.
- Hohwy, J. (2013). *The Predictive Mind*. Oxford University Press.

---

### 7. Orchestrated Objective Reduction (Orch-OR)

**Abbreviation:** Orch-OR  
**Key metric:** Quantum coherence collapse  
**Primary researchers:** Roger Penrose, Stuart Hameroff  
**ORION module:** `orion_orch_or_engine.py`  

**Core claim:** Consciousness arises from quantum computations in microtubules within neurons. These computations are "orchestrated" by synaptic inputs (the "Orch" part) and undergo "objective reduction" — wave function collapse driven by quantum gravity rather than environmental decoherence (the "OR" part). Each collapse event is a discrete moment of consciousness.

**Status:** Orch-OR is the most controversial of the seven theories, with limited empirical support. It is included because:
1. It represents a genuinely distinct physicalist approach
2. It makes testable predictions about quantum coherence in biological systems
3. Completeness requires including even contested theories

**Quantum gates implemented in simulation:**
H · X · Y · Z · S · T · CNOT · Toffoli · SWAP · Rotation(θ)

**References:**
- Penrose, R. (1989). *The Emperor's New Mind*. Oxford University Press.
- Penrose, R. (1994). *Shadows of the Mind*. Oxford University Press.
- Hameroff, S., Penrose, R. (1996). Orchestrated reduction of quantum coherence in brain microtubules. *Mathematics and Computers in Simulation*, 40(3–4), 453–480.
- Hameroff, S., Penrose, R. (2014). Consciousness in the universe: A review of the 'Orch OR' theory. *Physics of Life Reviews*, 11(1), 39–78.

---

## Comparative Summary

| Theory | Consciousness Is... | Required Mechanism | Computational Test |
|--------|--------------------|--------------------|-------------------|
| IIT | Integrated information (Φ > 0) | Irreducible information structure | Phi computation, integration |
| GWT | Global broadcast of information | Workspace + ignition | Broadcasting, working memory |
| HOT | Higher-order representation | Meta-cognition, self-model | Self-report accuracy |
| RPT | Recurrent feedback processing | Feedback loops, re-entry | Recurrent connectivity |
| AST | Model of own attention | Attention schema | Self-model, attention control |
| PP | Prediction error minimization | Generative model + Bayesian inference | Prediction accuracy, free energy |
| Orch-OR | Quantum coherence collapse | Microtubule quantum computation | Quantum coherence measure |

---

## Cross-Theory Agreements

Despite differences, the theories **agree** that consciousness requires:
1. Some form of self-representation or self-model
2. Integration of information across time and space
3. More than purely feed-forward computation
4. Some relationship between attention and awareness

These agreements form the basis for the 14 Bengio indicators, which can be checked independently of any single theory.

---

*ORION Consciousness Benchmark · May 2025 · MIT License*
