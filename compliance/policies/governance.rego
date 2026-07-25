package modelgovernance

default allow = false

allow {
    input.bias.disparate_impact >= 0.8
    input.bias.disparate_impact <= 1.25
    input.performance.roc_auc >= 0.75
    input.privacy.epsilon <= 5.0
    input.explainability.method != ""
    input.owner != ""
    input.dataset.consent_obtained == true
}

deny[msg] {
    input.bias.disparate_impact < 0.8
    msg := "DI below 0.8 — fairness gate failed"
}

deny[msg] {
    input.bias.disparate_impact > 1.25
    msg := "DI above 1.25 — fairness gate failed"
}

deny[msg] {
    input.performance.roc_auc < 0.75
    msg := "AUC below 0.75"
}

deny[msg] {
    input.privacy.epsilon > 5.0
    msg := "Privacy budget ε too large"
}

deny[msg] {
    input.explainability.method == ""
    msg := "No explainability method declared"
}

deny[msg] {
    not input.dataset.consent_obtained
    msg := "Dataset consent not recorded"
}
