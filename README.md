# llm_ipsum

Spiritual successor to lorem ipsum generators. Uses LLMs to generate placeholder text.

## Usage

Set `OPENAI_BASE_URL` and `OPENAI_API_KEY` in your environment (can point to any OpenAI-compatible API server). Alternatively, set `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY` for OpenRouter.

```bash
# 8 words
./llm_ipsum.py 8

# 8 words (appropriate for a title)
./llm_ipsum.py 8 --title

# 100 words in the given topic
./llm_ipsum.py 100 --topic "botany"

# Use a specific model
./llm_ipsum.py --model openai/gpt-4.1-nano 5
```

### Options

- `--topic TEXT`: Theme for the generated text.
- `--model MODEL`: Model identifier (default: `google/gemini-2.5-flash-lite`).
- `--title`: Generate title text (no trailing punctuation; prefer noun phrases).
