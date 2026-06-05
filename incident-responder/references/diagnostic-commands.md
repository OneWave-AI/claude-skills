# Diagnostic Commands and Techniques

When shell access is available, use these diagnostic patterns. Adapt to the specific environment.

## Application Log Analysis

```bash
# Find recent error logs (adapt path to project)
find /var/log -name "*.log" -mmin -60 -exec grep -l "ERROR\|FATAL\|CRITICAL" {} \;

# Tail application logs for real-time errors
tail -f /var/log/app/application.log | grep -i "error\|exception\|fatal"

# Count errors per minute in recent logs
awk '/ERROR/ {print substr($1,1,16)}' /var/log/app/application.log | sort | uniq -c | tail -20

# Find stack traces in logs
grep -A 20 "Exception\|Traceback" /var/log/app/application.log | tail -100
```

## System Resource Checks

```bash
# CPU and memory overview
top -bn1 | head -20

# Disk space
df -h

# Open file descriptors per process
lsof | awk '{print $1}' | sort | uniq -c | sort -rn | head -10

# Network connections by state
ss -s

# Memory details
free -h
cat /proc/meminfo | grep -i "mem\|swap\|cache"
```

## Container and Kubernetes Diagnostics

```bash
# Recent pod events
kubectl get events --sort-by='.lastTimestamp' -n <namespace> | tail -30

# Pod status and restarts
kubectl get pods -n <namespace> -o wide

# Pod logs (last 100 lines)
kubectl logs <pod-name> -n <namespace> --tail=100

# Describe failing pod
kubectl describe pod <pod-name> -n <namespace>

# Resource utilization
kubectl top pods -n <namespace>
kubectl top nodes
```

## Database Diagnostics

```bash
# PostgreSQL: Active connections and long-running queries
psql -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC LIMIT 20;"

# PostgreSQL: Connection count by state
psql -c "SELECT state, count(*) FROM pg_stat_activity GROUP BY state;"

# MySQL: Process list and slow queries
mysql -e "SHOW FULL PROCESSLIST;"
mysql -e "SHOW GLOBAL STATUS LIKE 'Slow_queries';"

# Redis: Memory and connection info
redis-cli INFO memory
redis-cli INFO clients
redis-cli SLOWLOG GET 10
```

## Git and Deployment History

```bash
# Recent commits on production branch
git log --oneline --since="24 hours ago" origin/main

# Changes in the most recent deployment
git diff HEAD~1..HEAD --stat

# Find who deployed what and when
git log --format="%h %ai %an %s" --since="48 hours ago" origin/main

# Check for database migration files in recent changes
git diff HEAD~3..HEAD --name-only | grep -i "migrat"
```
