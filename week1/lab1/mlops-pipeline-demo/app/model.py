"""
This is the 'model'. Right now it's a dummy function so we can focus
on the pipeline (CI/CD) rather than the ML itself.

When you're ready to plug in something real, this is the ONLY file
you need to change — load a pickled sklearn model, a transformers
pipeline, an API call to Groq/Gemini, whatever. Everything around it
(API, tests, Docker, CI/CD) stays the same. That's the point of this
boundary.
"""


def predict(value: float) -> float:
    """Dummy 'model': multiplies the input by 2."""
    return value * 2
