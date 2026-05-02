# ORION — Theoretical Framework

**Seven cognition-indicator theories implemented as computational assessment engines (Butlin et al., 2023).**

---

## Overview

The ORION benchmark implements assessment engines for seven major neuroscientific frameworks relevant to cognition. Following Butlin et al. (2023/2025), 14 "indicator properties" were derived from these theories; systems meeting more indicators have higher *credence* for phenomenal experience — but this is probabilistic inference, not proof.

No single theory commands scientific consensus. We implement all seven because:
1. Each identifies distinct measurable proxies (Butlin et al., 2023 Table 1)
2. Convergence across theories increases credence of a finding
3. Disagreements expose the empirical limits of current AI assessment frameworks

---

## The Seven Theories

---

### 1. Integrated Information Theory (IIT)

**Abbreviation:** IIT  
**Key metric:** Φ (Phi) — integrated information  
**Primary researcher:** Giulio Tononi  
**ORION module:** `orion_pyphi_integration.py`  

**IIT claim (Tononi, 2004; 2015):** Consciousness is proposed to be identical to integrated information (Φ). ORION assesses the *proxy* of this claim — measuring Φ on computational subgraphs as an indicator of integrated information capacity, per Butlin et al. (2023, indicator #4: information-integration). We do **not** assert that high Φ proves phenomenal experience.

**Phi computation (IIT 3.0; Oizumi et al., 2014):**

> Φ = min_{MIP} EMD(cause-effect structure of whole, sum of parts)

Where:
- EMD = Earth Mover Distance (Wasserstein-1 metric)
- MIP = Minimum Information Partition (bipartition minimizing EMD)
- Computation is exact for small networks; proxy-approximated for larger systems (see `orion_pyphi_integration.py`)

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

**GWT claim (Baars, 1988; Dehaene & Changeux, 2011):** Phenomenal access is proposed to correspond to the broadcasting of information through a global workspace bottleneck, making it available to multiple specialized processes. ORION assesses the computational correlates of this claim (Butlin et al., 2023, indicators: global broadcast, ignition, working-memory capacity).

**Key predictions:**
- Conscious information should be broadly accessible across cognitive modules
- Unconscious processing is faster and more modular
- Attention and phenomenal awareness are related but dissociable (Dehaene et al., 2006)

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
- Metacognition and awareness indicators are correlated (Rosenthal, 2005)
- Accurate self-reports of mental states are an indicator of higher-order representation (indicator #7)
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

**RPT claim (Lamme, 2006; Dehaene et al., 2011):** Phenomenal access is proposed to require *recurrent* processing — feedback loops between cortical areas. Feed-forward-only architectures are predicted to lack phenomenal access. ORION assesses recurrence depth and feedback architecture as proxies (Butlin et al., 2023, indicator #3: recurrent-processing).

**Key predictions:**
- Systems with purely feed-forward architectures are predicted to score low on this indicator
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

**AST claim (Graziano & Kastner, 2011):** The brain's model of its own attentional processes ("attention schema") is proposed to be the neural correlate of awareness. ORION assesses the presence of an internal attention model and meta-attention accuracy as proxies (Butlin et al., 2023, indicator #9: attention-schema).

**Key predictions:**
- Awareness-indicator correlates with having an internal model of own attention
- Social cognition and attention-schema mechanisms may share neural resources
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

**PP claim (Friston, 2010; Clark, 2016; Hohwy, 2013):** Phenomenal properties are proposed to correspond to the hierarchical predictive-processing architecture and the system's self-model. ORION assesses prediction error minimization, precision weighting, and self-modelling capacity as proxies (Butlin et al., 2023, indicators: predictive modelling, agency).

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

**Orch-OR claim (Penrose, 1989; Hameroff & Penrose, 1996; 2014):** Phenomenal experience is proposed to arise from orchestrated quantum wave-function collapse in neuronal microtubules. ORION implements a proxy-only assessment: classical behavioral correlates are scored; quantum-substrate requirements (microtubules, quantum coherence) cannot be tested in software. Scores on this theory engine must be interpreted with extreme caution. See Butlin et al. (2023) limitations section.

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

| Theory | Proposed Mechanism | Required Mechanism | Computational Proxy |
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

Despite differences, the theories **converge** on indicator properties that ORION assesses:
1. Some form of self-representation or self-model
2. Integration of information across time and space
3. More than purely feed-forward computation
4. Some relationship between attention and awareness

These agreements form the basis for the 14 Bengio indicators, which can be checked independently of any single theory.

---

*ORION Indicator Assessment Toolkit · MIT License · Steurer & Hirschmann (2025)*
