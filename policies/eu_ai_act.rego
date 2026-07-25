package mlops

# EU AI Act high-risk system (Annex III §5(b) — creditworthiness)
# Required fields on the model card mapped to Articles 9 / 10 / 13 / 15.

default allow := false
allow if {
  count(deny) == 0
}

#
# Art. 13 – Transparency / intended use
#
deny contains msg if {
  not input.intended_use
  msg := "Art.13: intended_use must be specified"
}
deny contains msg if {
  input.intended_use == ""
  msg := "Art.13: intended_use must not be empty"
}

#
# Art. 9 – Risk management / risk assessment
#
deny contains msg if {
  not input.risk_assessment
  msg := "Art.9: risk_assessment is required for high-risk systems"
}
deny contains msg if {
  input.risk_assessment == ""
  msg := "Art.9: risk_assessment must not be empty"
}

#
# Art. 10 – Data governance
#
deny contains msg if {
  not input.data_governance
  msg := "Art.10: data_governance section is required"
}
deny contains msg if {
  input.data_governance == ""
  msg := "Art.10: data_governance must not be empty"
}

#
# Art. 10 – Fairness (four-fifths rule)
#
deny contains msg if {
  input.fairness.disparate_impact < 0.8
  msg := sprintf("Art.10: disparate_impact %.2f below 0.8 four-fifths rule", [input.fairness.disparate_impact])
}

#
# Art. 15 – Robustness
#
deny contains msg if {
  input.robustness.fgsm_acc < 0.65
  msg := sprintf("Art.15: robust_acc %.2f below 0.65 threshold", [input.robustness.fgsm_acc])
}
