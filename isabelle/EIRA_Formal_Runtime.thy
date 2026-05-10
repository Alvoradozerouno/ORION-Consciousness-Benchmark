theory EIRA_Formal_Runtime
  imports Main
begin

(* ================================================ *)
(* Status type for actuator decisions               *)
(* ================================================ *)

datatype status = ABSTAIN | VERIFIED

(* ================================================ *)
(* Abstract and Concrete State Records              *)
(* ================================================ *)

record abstract_state =
  sensor_value   :: real
  confidence     :: real
  uncertainty    :: real
  radiation_flag :: bool
  actuator       :: bool
  estatus        :: status

record concrete_state =
  c_sensor   :: real
  c_conf     :: real
  c_uncert   :: real
  c_rad_flag :: bool
  c_actuator :: bool
  c_status   :: status

(* ================================================ *)
(* Threshold Constants                              *)
(* ================================================ *)

definition verified_threshold :: real where
  "verified_threshold = 0.8"

definition uncertainty_limit :: real where
  "uncertainty_limit = 0.2"

(* ================================================ *)
(* Abstract-to-Concrete Embedding                   *)
(* ================================================ *)

definition abstract_to_concrete :: "abstract_state \<Rightarrow> concrete_state" where
  "abstract_to_concrete a = \<lparr>
    c_sensor   = sensor_value a,
    c_conf     = confidence a,
    c_uncert   = uncertainty a,
    c_rad_flag = radiation_flag a,
    c_actuator = actuator a,
    c_status   = estatus a
  \<rparr>"

(* Convenience projection lemmas *)

lemma abstract_to_concrete_actuator [simp]:
  "c_actuator (abstract_to_concrete a) = actuator a"
  unfolding abstract_to_concrete_def by simp

lemma abstract_to_concrete_status [simp]:
  "c_status (abstract_to_concrete a) = estatus a"
  unfolding abstract_to_concrete_def by simp

lemma abstract_to_concrete_sensor [simp]:
  "c_sensor (abstract_to_concrete a) = sensor_value a"
  unfolding abstract_to_concrete_def by simp

lemma abstract_to_concrete_conf [simp]:
  "c_conf (abstract_to_concrete a) = confidence a"
  unfolding abstract_to_concrete_def by simp

lemma abstract_to_concrete_uncert [simp]:
  "c_uncert (abstract_to_concrete a) = uncertainty a"
  unfolding abstract_to_concrete_def by simp

lemma abstract_to_concrete_rad [simp]:
  "c_rad_flag (abstract_to_concrete a) = radiation_flag a"
  unfolding abstract_to_concrete_def by simp

end
