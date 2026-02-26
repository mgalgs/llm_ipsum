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
- `--timeout SECONDS`: Timeout for the API call (default: 7).

## Recommended models (OpenRouter)

Models were benchmarked on **speed**, **vocabulary diversity**, and **output quality** across 15 generations of 8-word phrases. All models tend toward some degree of repetitive vocabulary (an inherent LLM trait), but speed and diversity vary significantly.

| Model                           | Avg time | Diversity | Cost (in/out per 1M) | Notes                                                   |
|---------------------------------|----------|-----------|----------------------|---------------------------------------------------------|
| `google/gemini-2.5-flash-lite`  | **1.4s** | **71%**   | $0.01 / $0.04        | **Default.** Best speed/diversity/cost balance.         |
| `openai/gpt-4o-mini`            | 1.6s     | 69%       | $0.15 / $0.60        | Consistent quality, slightly pricier.                   |
| `amazon/nova-micro-v1`          | 1.6s     | 67%       | $0.035 / $0.14       | Very cheap, decent quality.                             |
| `qwen/qwen-turbo`               | 1.4s     | 62%       | $0.05 / $0.20        | Fast but repetitive ("dances" in 40% of outputs).       |
| `openai/gpt-4.1-nano`           | 1.6s     | 62%       | $0.10 / $0.40        | Repetitive ("beneath", "crimson").                      |
| `bytedance-seed/seed-1.6-flash` | 5.9s     | **85%**   | $0.075 / $0.30       | Best diversity, but slow (p95=19s) and leaks reasoning. |

Free-tier models (`:free` suffix) are not recommended due to aggressive rate limiting.
