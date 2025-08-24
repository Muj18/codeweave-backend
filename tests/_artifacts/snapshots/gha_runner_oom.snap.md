### GitHub Actions Runner Failure Troubleshooting — Production-Grade

**Key Symptoms**
- Jobs stuck in `queued` state, never picked up
- Runner logs show `Idle... waiting for jobs` but no jobs assigned
- Errors like `no available self-hosted runner` or capacity exhaustion
- Long queue times for workflows during peak hours

**Immediate Triage**
- Check runner status in GitHub: *Settings → Actions → Runners*
- Verify self-hosted runner service is active:
  ~~~bash
  sudo systemctl status actions.runner.*
  ~~~
- Inspect runner logs:
  ~~~bash
  tail -f _diag/Runner_*.log
  ~~~
- Confirm labels (`self-hosted`, `linux`, `x64`, custom tags) match workflow `runs-on` config
- Ensure network connectivity to GitHub Actions service endpoints

**Safe Fix — Workflow Example**
~~~yaml
jobs:
  build:
    runs-on: [self-hosted, linux, x64]   # Ensure label matches registered runner
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18"
~~~

**Scaling Fix — Self-Hosted Runner Container**
~~~bash
docker run -d --name gha-runner \
  -e RUNNER_SCOPE=repo \
  -e GITHUB_PAT=<token> \
  -e RUNNER_NAME=runner-$(uuidgen) \
  ghcr.io/actions/runner:latest
~~~
ℹ️ Add more runners or move to ephemeral runners for autoscaling.

**Cloud & Platform Notes**
- GitHub-hosted runners: 2000 free minutes/month, may hit concurrency limits
- Self-hosted: monitor CPU/memory usage on runner nodes
- Kubernetes: use `actions-runner-controller` for elastic scaling
- Ephemeral runners recommended for security + scale

**Monitoring & Prevention**
- Dashboards: runner availability, job queue times
- Alerts: high queue depth, >10min job wait time
- Autoscale runners during CI/CD peak hours
- Regularly patch/update runner software to latest release