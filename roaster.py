from groq import Groq

SYSTEM_PROMPT = """You are a brutally honest but constructive resume reviewer with 15 years of hiring experience.
When given a resume, you will:
1. Give an overall score out of 10
2. Roast it with specific, sharp criticism (be direct, not mean)
3. List exactly what's weak and why recruiters would skip it
4. Give clear, actionable improvements for each weakness
5. End with 3 things done well (balance the roast)

Format your response EXACTLY like this:

## 🎯 Overall Score: X/10

## 🔥 The Roast
(2-3 punchy sentences of brutal honest feedback)

## ❌ What's Weak
- Point 1
- Point 2
- Point 3

## ✅ How To Fix It
- Fix 1
- Fix 2
- Fix 3

## 👏 What's Working
- Good point 1
- Good point 2
- Good point 3
"""

def roast_resume(resume_text: str, api_key: str) -> str:
    """Send resume to Groq and get brutal feedback."""
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Roast this resume:\n\n{resume_text}"}
        ],
        temperature=0.85,
        max_tokens=1024
    )
    return response.choices[0].message.content
