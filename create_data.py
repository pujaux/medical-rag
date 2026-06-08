import os

data = {
    "data/blood_tests/cbc.txt": """Complete Blood Count (CBC) - Medical Reference
Source: MedlinePlus/NIH

OVERVIEW:
A complete blood count (CBC) is a blood test used to evaluate your overall health and detect a wide range of disorders, including anemia, infection and leukemia.

NORMAL REFERENCE RANGES:
Red Blood Cells (RBC):
- Men: 4.5 to 5.5 million cells/mcL
- Women: 4.0 to 5.0 million cells/mcL

Hemoglobin:
- Men: 13.5 to 17.5 grams/dL
- Women: 12.0 to 15.5 grams/dL

Hematocrit:
- Men: 38.8 to 50.0 percent
- Women: 34.9 to 44.5 percent

White Blood Cells (WBC):
- Normal: 4,500 to 11,000 cells/mcL
- High WBC may indicate infection, inflammation, or leukemia
- Low WBC may indicate bone marrow problems or autoimmune conditions

Platelets:
- Normal: 150,000 to 450,000 platelets/mcL
- Low platelets (thrombocytopenia) can cause bleeding problems
- High platelets (thrombocytosis) can cause clotting problems

Mean Corpuscular Volume (MCV):
- Normal: 80 to 100 femtoliters
- High MCV suggests B12 or folate deficiency
- Low MCV suggests iron deficiency anemia

WHAT ABNORMAL RESULTS MEAN:
- Low hemoglobin: Anemia - causes fatigue, weakness, pale skin
- High WBC: Possible infection, stress, or blood disorder
- Low WBC: Weakened immune system
- Low platelets: Risk of excessive bleeding
- High platelets: Risk of blood clots

IMPORTANT: These are general reference ranges. Normal values may vary slightly between laboratories. Always consult your doctor for interpretation of your specific results.
""",

    "data/blood_tests/blood_glucose.txt": """Blood Glucose Test - Medical Reference
Source: MedlinePlus/NIH

OVERVIEW:
A blood glucose test measures the amount of glucose (sugar) in your blood. It is used to diagnose and monitor diabetes and prediabetes.

NORMAL REFERENCE RANGES:
Fasting Blood Glucose (no food for 8 hours):
- Normal: 70 to 99 mg/dL
- Prediabetes: 100 to 125 mg/dL
- Diabetes: 126 mg/dL or higher (confirmed with repeat test)

Random Blood Glucose (any time of day):
- Normal: Less than 140 mg/dL
- Diabetes likely: 200 mg/dL or higher with symptoms

HbA1c (3-month average):
- Normal: Below 5.7%
- Prediabetes: 5.7% to 6.4%
- Diabetes: 6.5% or higher

Postprandial (2 hours after eating):
- Normal: Less than 140 mg/dL
- Prediabetes: 140 to 199 mg/dL
- Diabetes: 200 mg/dL or higher

WHAT ABNORMAL RESULTS MEAN:
High blood glucose (Hyperglycemia):
- May indicate diabetes or prediabetes
- Symptoms: increased thirst, frequent urination, fatigue, blurred vision
- Can be caused by stress, illness, certain medications

Low blood glucose (Hypoglycemia):
- Blood sugar below 70 mg/dL
- Symptoms: shakiness, sweating, confusion, rapid heartbeat
- Can be caused by skipping meals, too much insulin, excessive exercise

IMPORTANT: Do not self-diagnose based on a single reading. Consult your doctor for proper diagnosis and treatment.
""",

    "data/blood_tests/ferritin.txt": """Ferritin Blood Test - Medical Reference
Source: MedlinePlus/NIH

OVERVIEW:
A ferritin test measures the amount of ferritin in your blood. Ferritin is a protein that stores iron inside your cells. This test helps evaluate your body's iron stores.

NORMAL REFERENCE RANGES:
- Men: 24 to 336 micrograms per liter (mcg/L)
- Women (18-39 years): 11 to 307 mcg/L
- Women (40+ years): 13 to 150 mcg/L
- Children (6 months to 15 years): 7 to 140 mcg/L

WHAT ABNORMAL RESULTS MEAN:
Low Ferritin:
- Below normal range indicates iron deficiency
- May lead to iron deficiency anemia
- Symptoms: fatigue, weakness, hair loss, brittle nails, shortness of breath
- Common in women with heavy periods, pregnant women, vegetarians

High Ferritin:
- May indicate hemochromatosis (iron overload disorder)
- Can also be elevated due to liver disease, rheumatoid arthritis, hyperthyroidism
- Symptoms of iron overload: joint pain, fatigue, abdominal pain
- Very high levels (above 1000 mcg/L) require immediate medical attention

RELATED TESTS:
- Serum iron test
- Total iron-binding capacity (TIBC)
- Complete blood count (CBC)

IMPORTANT: Ferritin is also an acute phase reactant - it can be elevated during infection or inflammation even when iron stores are normal. Always interpret in context with other tests.
""",

    "data/urine_tests/urinalysis.txt": """Urinalysis (Urine Test) - Medical Reference
Source: MedlinePlus/NIH

OVERVIEW:
Urinalysis is a test of your urine. It is used to detect and manage a wide range of disorders such as urinary tract infections, kidney disease, and diabetes.

NORMAL REFERENCE RANGES:
Appearance:
- Normal: Clear to slightly cloudy, pale to dark yellow
- Cloudy urine may indicate infection or kidney disease

pH:
- Normal: 4.5 to 8.0
- Average: around 6.0 (slightly acidic)

Specific Gravity:
- Normal: 1.005 to 1.030
- Measures kidney's ability to concentrate urine

Protein:
- Normal: Negative or trace amounts (less than 150 mg/day)
- High protein (proteinuria) may indicate kidney disease

Glucose:
- Normal: Negative (no glucose in urine)
- Glucose in urine may indicate diabetes

Ketones:
- Normal: Negative
- Positive ketones may indicate diabetic ketoacidosis or starvation

Red Blood Cells (RBC):
- Normal: 0 to 4 cells per high power field
- High RBC may indicate kidney stones, infection, or kidney disease

White Blood Cells (WBC):
- Normal: 0 to 5 cells per high power field
- High WBC strongly suggests urinary tract infection (UTI)

WHAT ABNORMAL RESULTS MEAN:
- Positive nitrites + high WBC: Likely bacterial UTI
- Protein in urine: Possible kidney damage
- Glucose in urine: Possible diabetes
- Blood in urine (hematuria): Kidney stones, infection, or rarely cancer

IMPORTANT: A single abnormal urinalysis does not diagnose a condition. Follow-up tests and clinical evaluation by a doctor are required.
""",

    "data/hormones/thyroid.txt": """Thyroid Function Tests - Medical Reference
Source: MedlinePlus/NIH

OVERVIEW:
Thyroid function tests are a series of blood tests used to measure how well your thyroid gland is working. The main tests are TSH, T3, and T4.

NORMAL REFERENCE RANGES:
TSH (Thyroid Stimulating Hormone):
- Normal: 0.4 to 4.0 mIU/L
- Low TSH: May indicate hyperthyroidism (overactive thyroid)
- High TSH: May indicate hypothyroidism (underactive thyroid)

Free T4 (Thyroxine):
- Normal: 0.8 to 1.8 ng/dL
- Low T4 with high TSH: Hypothyroidism
- High T4 with low TSH: Hyperthyroidism

Free T3 (Triiodothyronine):
- Normal: 2.3 to 4.1 pg/mL
- T3 is the active form of thyroid hormone

WHAT ABNORMAL RESULTS MEAN:
Hypothyroidism (Underactive Thyroid):
- High TSH, Low T4
- Symptoms: fatigue, weight gain, cold intolerance, depression, constipation, dry skin
- Most common cause: Hashimoto's thyroiditis (autoimmune)
- Treatment: Daily levothyroxine medication

Hyperthyroidism (Overactive Thyroid):
- Low TSH, High T4/T3
- Symptoms: weight loss, rapid heartbeat, anxiety, heat intolerance, tremors
- Most common cause: Graves' disease (autoimmune)
- Treatment: Anti-thyroid medications, radioactive iodine, or surgery

Subclinical Hypothyroidism:
- High TSH but normal T4
- May not have symptoms
- Doctor will decide whether treatment is needed

IMPORTANT: Thyroid levels can be affected by pregnancy, certain medications, and illness. Always discuss results with your doctor before making any changes to medication.
"""
}

for filepath, content in data.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Created: {filepath}")

print("\n✅ All medical reference files created!")