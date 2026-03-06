# Ansible

## What is Ansible?
Ansible is an **open-source IT automation tool** for configuration management, application deployment, and task automation. It is **agentless** (uses SSH/WinRM), uses **YAML-based playbooks**, and follows a **push model**.

## What is agentless automation?
Ansible does not require any **agent software** installed on managed nodes. It connects via **SSH** (Linux) or **WinRM** (Windows) and runs Python modules remotely. Only requires Python on the target.

## What are the core Ansible components?

| Component   | Description |
|-------------|-------------|
| **Inventory** | List of managed hosts (static or dynamic) |
| **Playbook** | YAML file defining automation tasks |
| **Task** | A single unit of work (call a module) |
| **Module** | A reusable function (e.g., `apt`, `copy`, `service`) |
| **Role** | Organized collection of tasks, handlers, variables, templates |
| **Handler** | Task triggered by a `notify` (e.g., restart a service) |
| **Variable** | Dynamic values used in playbooks |
| **Template** | Jinja2 template for generating config files |
| **Fact** | Information gathered from managed hosts |

## What does a simple Ansible playbook look like?
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes           # Run as sudo

  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

## What is an Ansible inventory file?
A file listing managed hosts, optionally grouped:
```ini
[webservers]
web1.example.com
web2.example.com ansible_user=ubuntu

[databases]
db1.example.com ansible_host=10.0.0.5

[production:children]
webservers
databases
```

## What is an Ansible role?
A structured way to organize playbook content:
```
roles/webserver/
├── tasks/main.yml      # Main task list
├── handlers/main.yml   # Handlers
├── templates/          # Jinja2 templates
├── files/              # Static files
├── vars/main.yml       # Variables
├── defaults/main.yml   # Default variables
└── meta/main.yml       # Role dependencies
```

## What is `become` in Ansible?
The Ansible privilege escalation directive. `become: yes` runs tasks with `sudo`. Equivalent to running commands as root.

## What is an Ansible handler?
A task that is **only triggered by a `notify`** directive and runs **once at the end of a play** (not multiple times if notified multiple times):
```yaml
tasks:
  - name: Copy nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx

handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

## What is the difference between `ansible` and `ansible-playbook`?
- `ansible`: Run **ad-hoc single tasks** against hosts
  ```bash
  ansible webservers -m ping
  ansible web1 -m shell -a "df -h"
  ```
- `ansible-playbook`: Run a **full playbook** file
  ```bash
  ansible-playbook site.yml
  ansible-playbook -i inventory.ini deploy.yml --check
  ```

## What are Ansible facts?
**System information automatically gathered** from managed hosts at the start of a play (CPU, OS, IP addresses, etc.). Access via `ansible_facts` or `ansible_hostname`:
```yaml
- debug:
    msg: "OS is {{ ansible_distribution }} {{ ansible_distribution_version }}"
```

## What is Ansible Vault?
A feature to **encrypt sensitive data** (passwords, API keys) in playbooks and variable files:
```bash
ansible-vault encrypt secrets.yml
ansible-vault edit secrets.yml
ansible-playbook site.yml --ask-vault-pass
```

## What is dynamic inventory in Ansible?
Instead of a static file, inventory is **generated dynamically** from cloud APIs, CMDB, etc. AWS, GCP, Azure, and Docker all have dynamic inventory plugins. Returns JSON listing current hosts and groups.

## What is idempotency in Ansible?
Most Ansible modules are **idempotent** — running a playbook twice results in the same system state (no unnecessary changes on the second run). Modules check current state before making changes.
