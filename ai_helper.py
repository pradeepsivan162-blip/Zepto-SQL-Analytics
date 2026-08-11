import os
import re

def ask_gemini(user_prompt, api_key=None, schema_info=None):
    """
    Interfaces with Google Gemini API to analyze user questions,
    generate SQL queries against the 'zepto' dataset, and provide business explanations.
    """
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "sql": None,
            "explanation": "⚠️ **Gemini API Key Required**: Please enter your Gemini API Key in the sidebar or set `GEMINI_API_KEY` in Streamlit Secrets.",
            "demo": True
        }

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        default_schema = """
Table: zepto
Columns:
- category (VARCHAR): Product category (e.g., 'Cooking Essentials', 'Munchies', 'Fruits & Vegetables')
- name (VARCHAR): Product name
- mrp (NUMERIC): Maximum Retail Price in Rupees
- discountPercent (NUMERIC): Discount percentage
- availableQuantity (INTEGER): Quantity in stock
- discountSellingPrice (NUMERIC): Discounted selling price
- weightInGms (INTEGER): Product weight in grams
- outOfStock (BOOLEAN): TRUE if out of stock, FALSE if available
- quantity (INTEGER): Product order/item quantity
        """

        prompt = f"""
You are an expert SQL Data Analyst for the Zepto e-commerce grocery dataset.
The database has a single table named `zepto`.

{schema_info or default_schema}

User Question: "{user_prompt}"

INSTRUCTIONS:
1. If the user question requires querying data, generate a single valid, executable SQL query for table `zepto`. Put the SQL query inside a ```sql ... ``` code block.
2. Provide a concise, clear business explanation or answer below the code block.
3. Do not invent non-existent table or column names.
"""

        # Try supported models in order of priority
        candidate_models = ['gemini-flash-latest', 'gemini-3.6-flash', 'gemini-2.5-flash-lite', 'gemini-pro-latest']
        response = None
        last_err = None

        for m_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=prompt
                )
                if response and hasattr(response, 'text') and response.text:
                    break
            except Exception as e_mod:
                last_err = e_mod
                continue

        if not response or not hasattr(response, 'text'):
            raise last_err or Exception("Could not generate content from Gemini API.")

        text = response.text

        # Extract SQL query if present
        sql_match = re.search(r'```sql\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
        extracted_sql = sql_match.group(1).strip() if sql_match else None

        # Clean explanation text
        explanation = text
        if sql_match:
            explanation = text.replace(sql_match.group(0), "").strip()

        return {
            "sql": extracted_sql,
            "explanation": explanation,
            "raw": text,
            "demo": False
        }

    except Exception as e:
        err_msg = str(e)
        if "401" in err_msg or "UNAUTHENTICATED" in err_msg or "invalid authentication" in err_msg.lower():
            friendly_err = """⚠️ **Invalid Gemini API Key**: The API key provided was rejected (401 Unauthenticated).

### How to get a working API Key:
1. Open **[aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)** (100% Free).
2. Click **Create API Key**.
3. Copy your key and paste it into the **Gemini API Key** field in the left sidebar!"""
            return {
                "sql": None,
                "explanation": friendly_err,
                "demo": False
            }
        
        return {
            "sql": None,
            "explanation": f"❌ **AI Error**: Failed to query Gemini API: {err_msg}",
            "demo": False
        }
