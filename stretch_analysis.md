# Stretch Assignment Analysis: Custom NER Rules

### How Custom Rules Changed the Results
After adding the EntityRuler, I noticed a clear improvement in how the system identifies specific climate terms. In the base spaCy model, "Paris Agreement" was often labeled as 'LAW' or sometimes not recognized at all. By adding a custom rule, I forced the model to categorize it as an 'AGREEMENT'. Similarly, "COP28" was frequently missed by the standard model because it's a specific shorthand, but the custom rule captured it perfectly as a 'CLIMATE_EVENT'.

### Pipeline Position Impact
When I placed the EntityRuler **before** the 'ner' component, the custom rules took priority. This was better for terms like "Paris Agreement" because it prevented the statistical model from giving it a generic label. If I put it **after**, the statistical model would sometimes "steal" the entity and label it incorrectly before my rules could see it.

### Qualitative Examples
- **Before:** "Paris Agreement" -> LAW
- **After:** "Paris Agreement" -> AGREEMENT
- **Before:** "COP28" -> (No entity found)
- **After:** "COP28" -> CLIMATE_EVENT

One issue I found was that my rules are very strict. If the text said "The 2015 Accord" instead of "Paris Agreement", my rule didn't fire. This shows that while rules are great for precision, they don't have the flexibility of the statistical model.
