theory EIRA_Refinement
  imports Main "EIRA_Formal_Runtime"
begin

(* ================================================ *)
(* Simulation Relation                              *)
(* ================================================ *)

definition simulation_relation :: "abstract_state \<Rightarrow> concrete_state \<Rightarrow> bool" where
  "simulation_relation abs conc \<longleftrightarrow>
    sensor_value abs   = c_sensor conc \<and>
    confidence abs     = c_conf conc \<and>
    uncertainty abs    = c_uncert conc \<and>
    radiation_flag abs = c_rad_flag conc"

(* ================================================ *)
(* Abstract Safe Transition                         *)
(* ================================================ *)

definition safe_transition :: "abstract_state \<Rightarrow> abstract_state" where
  "safe_transition a =
    (if radiation_flag a then
       a\<lparr> actuator := False, estatus := ABSTAIN \<rparr>
     else if confidence a > verified_threshold \<and> uncertainty a < uncertainty_limit then
       a\<lparr> actuator := True,  estatus := VERIFIED \<rparr>
     else
       a\<lparr> actuator := False, estatus := ABSTAIN \<rparr>)"

(* ================================================ *)
(* Low-Level Equivalence (for non-interference)     *)
(* ================================================ *)

definition low_equiv :: "abstract_state \<Rightarrow> abstract_state \<Rightarrow> bool" where
  "low_equiv abs1 abs2 \<longleftrightarrow>
    radiation_flag abs1 = radiation_flag abs2 \<and>
    confidence abs1     = confidence abs2 \<and>
    uncertainty abs1    = uncertainty abs2"

(* ================================================ *)
(* Non-Interference Theorem                         *)
(* ================================================ *)

theorem non_interference:
  assumes "low_equiv abs1 abs2"
  shows "actuator (safe_transition abs1) = actuator (safe_transition abs2)"
  using assms
  unfolding low_equiv_def safe_transition_def
  by simp

end
