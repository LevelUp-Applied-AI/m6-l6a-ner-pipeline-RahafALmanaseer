import spacy
import pandas as pd
from spacy.pipeline import EntityRuler

# Load the climate dataset
def get_data():
    return pd.read_csv("data/climate_articles.csv")

def setup_custom_pipeline(position="before"):
    """
    I am setting up a custom spaCy pipeline here. 
    The goal is to add an EntityRuler to catch climate-specific terms.
    """
    nlp = spacy.load("en_core_web_sm")
    
    # Adding the ruler either before or after the standard 'ner' component
    # to see how it affects the priority of matching.
    ruler = nlp.add_pipe("entity_ruler", before=position if position == "ner" else None)
    if position == "before":
        nlp.remove_pipe("entity_ruler") # reset to put it in the right place
        ruler = nlp.add_pipe("entity_ruler", before="ner")
    elif position == "after":
        ruler = nlp.add_pipe("entity_ruler", after="ner")

    # Defining at least 10 patterns for climate terminology
    # Labels used: AGREEMENT, CLIMATE_REPORT, and CLIMATE_EVENT
    patterns = [
        # Agreements
        {"label": "AGREEMENT", "pattern": "Paris Agreement"},
        {"label": "AGREEMENT", "pattern": "Kyoto Protocol"},
        {"label": "AGREEMENT", "pattern": "Montreal Protocol"},
        
        # Reports
        {"label": "CLIMATE_REPORT", "pattern": "IPCC AR6"},
        {"label": "CLIMATE_REPORT", "pattern": "Sixth Assessment Report"},
        {"label": "CLIMATE_REPORT", "pattern": "Emissions Gap Report"},
        
        # Events/Conferences
        {"label": "CLIMATE_EVENT", "pattern": "COP28"},
        {"label": "CLIMATE_EVENT", "pattern": "COP27"},
        {"label": "CLIMATE_EVENT", "pattern": "United Nations Climate Change Conference"},
        
        # Thresholds
        {"label": "THRESHOLD", "pattern": "1.5°C target"}
    ]
    
    ruler.add_patterns(patterns)
    return nlp

def run_extraction_comparison():
    df = get_data()
    # Filter for English texts just like we did in the lab
    en_texts = df[df["language"] == "en"]["text"].head(20).tolist()
    
    # 1. Using Base spaCy
    nlp_base = spacy.load("en_core_web_sm")
    print("--- BASE SPACY RESULTS ---")
    for text in en_texts[:3]: # Printing a few for the analysis
        doc = nlp_base(text)
        print([(ent.text, ent.label_) for ent in doc.ents if ent.label_ in ["LAW", "ORG", "EVENT"]])

    # 2. Using Custom spaCy (Ruler before NER)
    nlp_custom = setup_custom_pipeline(position="before")
    print("\n--- CUSTOM RULE-BASED RESULTS ---")
    for text in en_texts[:3]:
        doc = nlp_custom(text)
        # Checking if our custom labels show up
        print([(ent.text, ent.label_) for ent in doc.ents])

if __name__ == "__main__":
    # Small test to make sure the ruler works
    test_nlp = setup_custom_pipeline(position="before")
    test_doc = test_nlp("The Paris Agreement was discussed at COP28.")
    print("Entities found:", [(ent.text, ent.label_) for ent in test_doc.ents])
    
    # Run the full comparison
    run_extraction_comparison()
