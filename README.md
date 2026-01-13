# llm_ipsum

Spiritual successor to lorem ipsum generators. Uses LLMs to generate placeholder text.

## Usage

Set `OPENAI_BASE_URL` and `OPENAI_API_KEY` in your environment. `OPENAI_BASE_URL` can point to any OpenAI-compatible API server (e.g. OpenRouter).

```bash
# 8 words
./llm_ipsum.py 8

# 8 words (appropriate for a title)
./llm_ipsum.py 8 --title

# 100 words in the given topic
./llm_ipsum.py 100 --topic "botany"

# Use OpenRouter
OPENAI_BASE_URL=$OPENROUTER_BASE_URL OPENAI_API_KEY=$OPENROUTER_API_KEY ./llm_ipsum.py 5
```

### Options

- `--topic TEXT`: Theme for the generated text.
- `--model MODEL`: Model identifier (default: `google/gemini-2.5-flash-lite`).
- `--title`: Generate title text (no trailing punctuation; prefer noun phrases).
