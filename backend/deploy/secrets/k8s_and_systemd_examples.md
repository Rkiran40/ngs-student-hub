# Kubernetes and systemd secrets examples

## Kubernetes (Secret as env)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: studenthub-secrets
  namespace: production
type: Opaque
stringData:
  SMTP_SERVER: smtp.example.com
  SMTP_USER: user@example.com
  SMTP_PASSWORD: super-secret

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: studenthub
spec:
  template:
    spec:
      containers:
        - name: studenthub
          image: your-registry/studenthub:latest
          envFrom:
            - secretRef:
                name: studenthub-secrets
```

## systemd (/etc/studenthub.env)
Create `/etc/studenthub.env` with restricted permissions and reference it in the service file:

```
# /etc/studenthub.env
SMTP_SERVER=smtp.example.com
SMTP_USER=user@example.com
SMTP_PASSWORD=super-secret
```

Service snippet:
```
[Service]
EnvironmentFile=/etc/studenthub.env
ExecStart=/usr/bin/docker run --env-file /etc/studenthub.env ...
```

Ensure `/etc/studenthub.env` is owned by root and mode 600:
```
sudo chown root:root /etc/studenthub.env
sudo chmod 600 /etc/studenthub.env
```
