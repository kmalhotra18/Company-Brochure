#Add translation function to translate the brochure into spanish

def translate_brochure_to_spanish(brochure_text):
    translation_prompt = (
        "You are a professional translator. Translate the following markdown brochure into natural, idiomatic Spanish. "
        "Preserve any formatting and tone (e.g., humorous, professional).\n\n"
        f"{brochure_text}"
    )

    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant who translates English content into Spanish."},
            {"role": "user", "content": translation_prompt}
        ]
    )
    translated = response.choices[0].message.content
    display(Markdown(translated))
    return translated

#Modify stream_brochure to Return Text

def stream_brochure(company_name, url):                                                  
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
        stream=True
    )

    response = ""
    display_handle = display(Markdown(""), display_id=True)                               
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```", "").replace("markdown", "")
        update_display(Markdown(response), display_id=display_handle.display_id)

    return response

#Add Call to Translation

english_brochure = stream_brochure(company_name, url)
translate = input("Would you like to translate the brochure to Spanish? (yes/no): ").strip().lower()
if translate == "yes":
    translate_brochure_to_spanish(english_brochure)
