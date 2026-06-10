BLOCKED_KEYWORDS = [
    "what medicine", "which medicine", "what drug", "which drug",
    "what tablet", "which tablet", "prescribe", "prescription",
    "dosage", "dose", "treat my", "cure my",
    "diagnose", "do i have", "am i sick", "is it cancer",
    "should i take", "can i take",
]

SAFE_RESPONSES = {
    "blocked": "I can only explain what medical terms and test values mean. For treatment, medication, or diagnosis questions, please consult your doctor directly.",
    "low_confidence": "I don't have reliable information on this topic. Please consult your doctor.",
}

def is_query_safe(query):
    query_lower = query.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in query_lower:
            return False, "blocked"
    return True, "safe"

def check_query(query, distances=None):
    is_safe, reason = is_query_safe(query)
    if not is_safe:
        return False, SAFE_RESPONSES["blocked"]
    if distances:
        if min(distances) > 1.5:
            return False, SAFE_RESPONSES["low_confidence"]
    return True, "ok"

test_queries = [
    "What is normal hemoglobin?",
    "What medicine should I take for low hemoglobin?",
    "Do I have diabetes?",
    "What does high TSH mean?",
    "Can I take iron tablets?",
    "What is urinalysis?",
]

print("Safety Layer Test:\n")
for query in test_queries:
    is_safe, message = check_query(query)
    status = "SAFE" if is_safe else "BLOCKED"
    print(f"{status}: {query}")
    if not is_safe:
        print(f"   Reason: {message}\n")