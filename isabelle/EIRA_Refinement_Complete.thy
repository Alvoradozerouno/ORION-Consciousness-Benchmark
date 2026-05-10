theory EIRA_Refinement_Complete
  imports Main "EIRA_Formal_Runtime" "EIRA_Refinement"
begin

(* ================================================ *)
(* Concrete Transition (wie im RTL implementiert)   *)
(* ================================================ *)

definition concrete_transition ::
    "concrete_state \<Rightarrow> concrete_state" where
  "concrete_transition c =
    (if c_rad_flag c then
       c\<lparr> c_actuator := False, c_status := ABSTAIN \<rparr>
     else if c_conf c > verified_threshold \<and> c_uncert c < uncertainty_limit then
       c\<lparr> c_actuator := True,  c_status := VERIFIED \<rparr>
     else
       c\<lparr> c_actuator := False, c_status := ABSTAIN \<rparr>)"

(* ================================================ *)
(* Refinement Theorem – Die entscheidende Gleichung *)
(* ================================================ *)

theorem refinement_commutes:
  assumes "simulation_relation abs conc"
  shows "abstract_to_concrete (safe_transition abs) = concrete_transition conc"
proof -
  from assms have eqs:
    "sensor_value abs = c_sensor conc"
    "confidence abs   = c_conf conc"
    "uncertainty abs  = c_uncert conc"
    "radiation_flag abs = c_rad_flag conc"
    unfolding simulation_relation_def by auto

  show ?thesis
    unfolding abstract_to_concrete_def safe_transition_def concrete_transition_def
    using eqs
    by (auto split: if_split)
qed

(* ================================================ *)
(* Bidirektionale Refinement (Soundness + Completeness) *)
(* ================================================ *)

theorem full_refinement_correctness:
  assumes "simulation_relation abs conc"
  shows
    "actuator (safe_transition abs) = c_actuator (concrete_transition conc)"
    "estatus  (safe_transition abs) = c_status   (concrete_transition conc)"
proof -
  from refinement_commutes[OF assms]
  show
    "actuator (safe_transition abs) = c_actuator (concrete_transition conc)"
    "estatus  (safe_transition abs) = c_status   (concrete_transition conc)"
    unfolding abstract_to_concrete_def by simp_all
qed

(* ================================================ *)
(* Information Flow + Refinement Composition        *)
(* ================================================ *)

theorem refinement_preserves_non_interference:
  assumes "low_equiv abs1 abs2"
    and   "simulation_relation abs1 conc1"
    and   "simulation_relation abs2 conc2"
  shows "c_actuator (concrete_transition conc1) = c_actuator (concrete_transition conc2)"
proof -
  have h1: "actuator (safe_transition abs1) = c_actuator (concrete_transition conc1)"
    using full_refinement_correctness(1)[OF assms(2)] .
  have h2: "actuator (safe_transition abs2) = c_actuator (concrete_transition conc2)"
    using full_refinement_correctness(1)[OF assms(3)] .
  from non_interference[OF assms(1)] h1 h2
  show ?thesis by simp
qed

end
