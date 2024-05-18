This is a monitoring app developped with python (flask) to get status of each services i self host

To deploy it, you just need install python3-pip python3-venv python3-gunicorn then source to activate your pip environment and create a systemd service to run you app with gunicorn.

##Create a systemd service called as you want i will call him monitor.service located in /lib/systemd/system :

```
[Unit]
Description=Gunicorn instance to serve my Flask application
After=network.target

[Service]
User=yourusername
Group=www-data
WorkingDirectory=/monitor/app
Environment="PATH=/monitor/venv/bin"
ExecStart=/monitor/gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app
[Install]
WantedBy=multi-user.target
```


## Relaunch systemd and start the web server
systemctl daemon-reload && systemctl start monitor

if the webserver run correctly, you can enable it at boot using the command `systemctl enable monitor`



## Configure the client

Create a shell script on the client which will retrieve status of each services you want to monitor :

```bash
#!/bin/bash

# Initialize status variables
sshd_status=""
wg_status=""

########### DEVICE #############

# Function to check the status of a service using systemctl
check_service_status() {
    local service_name=$1
    local service_var=$2
    if systemctl is-active --quiet "${service_name}"; then
        echo "${service_name} is running"
        eval "${service_var}='up'"
    else
        echo "${service_name} is not running"
        eval "${service_var}='down'"
    fi
}

# Check the status of services
check_service_status sshd sshd_status
check_service_status wg-quick@wg0 wg_status

# Generate JSON output for VM1
vm1_json=$(cat <<EOF
{
    "hostname": "vm1",
    "Local IP": "X.X.X.X",
    "Public IP": "X.X.X.X",
    "services": {
        "ssh": {
            "port": 1234,
            "status": "${ssh_status}"
        },
        "WireGuard": {
            "port": 61761,
            "status": "${wg_status}"
        }
    }
}
EOF
)

echo "${vm1_json}" > vm1.json
/usr/bin/rsync -e "ssh -i /path/to/privkey -p <ssh port>" /vm1.json <user>@<ip>:/monitor/vm1.json
```

Then add a cron to run this script every 5 seconds

```
crontab -e
* * * * * sleep 5; /bin/bash /path/your/script.sh
```

Then use rsync or salt to send it on the server on every 5 seconds for example.
