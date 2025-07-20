from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate_en_to_ka(text):
    # Load the tokenizer and model for NLLB 200 model

    # Tokenize the input text, specifying source and target languages
    inputs = tokenizer(text, return_tensors="pt")

    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids("kat_Geor"), max_length=30
    )
    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

