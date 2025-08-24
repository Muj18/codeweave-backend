### LLM Timeout / Slow Response Troubleshooting

**Key Symptoms**
- API calls to LLM provider exceed timeout thresholds
- Users experience long latency (>30s) or request failures
- Logs show `DeadlineExceeded`, `504 Gateway Timeout`, or socket hang-ups
- High concurrency leads to queued or dropped requests

**Immediate Triage**
- Check provider status page (e.g., OpenAI, Anthropic, Azure OpenAI)
- Verify client timeout settings in application code
- Inspect API logs for request latency and retry attempts
- Confirm network connectivity and DNS resolution to LLM endpoints

**Safe Fix**
~~~python
import openai
import backoff
import requests

# Add timeout + retries to handle LLM slowness
@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException,))
def call_llm(prompt):
    return openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        request_timeout=30  # seconds
    )
~~~

**Scaling Fix**
~~~python
# Batch requests to reduce latency impact
prompts = ["q1", "q2", "q3"]
responses = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": p} for p in prompts],
    request_timeout=60
)
~~~

**Cloud & Platform Notes**
- Ensure autoscaling is enabled for backend services handling LLM calls
- Cache frequent responses to reduce repeated requests
- For streaming APIs, prefer event-driven architecture to avoid blocking
- If on Kubernetes, configure proper readiness/liveness probes for services calling the LLM

**Monitoring & Prevention**
- Track latency percentiles (P50, P95, P99) for LLM calls
- Alerts on error rate >5% or latency >20s
- Implement circuit breaker: fallback to cached or degraded responses
- Regular load tests to validate scaling under peak usage