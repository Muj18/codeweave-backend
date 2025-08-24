### Ansible SSH Failure Troubleshooting — Production-Grade

**Key Symptoms**
- Playbook fails with `UNREACHABLE!` or `Permission denied (publickey)`
- Long SSH timeouts or intermittent connectivity errors
- Connection refused, host unreachable, or fails only via Ansible but works manually
- Tasks hang or fail inconsistently across multiple hosts

**Immediate Triage**
- Verify inventory file has correct host/IP and SSH user
- Test SSH manually: `ssh -i ~/.ssh/key user@host`
- Ensure target host’s SSHD is running and listening on the correct port
- Confirm private key permissions: `chmod 600 ~/.ssh/id_rsa`
- Check that `ansible_user` and `ansible_ssh_private_key_file` are correctly set
- Validate `become` permissions and sudo access on the target host
- Check network/firewall rules for intermittent connectivity

**Safe Fix — Example Inventory & Playbook Configuration**
```yaml
# inventory/hosts.yml
[webservers]
192.168.1.10 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa
192.168.1.11 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa

# ansible.cfg
[defaults]
inventory = inventory/hosts.yml
remote_user = ubuntu
host_key_checking = False
timeout = 30

# Example Playbook
- name: Ensure webserver packages are installed
  hosts: webservers
  become: yes
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
    - name: Install Nginx
      apt:
        name: nginx
        state: latest