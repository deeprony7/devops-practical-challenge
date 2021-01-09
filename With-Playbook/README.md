## Ansible Playbook to deploy nginx

* Setting up passwordless connection between two servers for seamless workflow in the future
Execute on control node:
```
ssh-keygen
ssh-copy-id user_name@hostname
```
* Install ansible:```sudo apt install ansible -y```

* Set up our inventory file at /etc/ansible/hosts:
```
[web]
34.227.142.155 ansible_user=cloud_user ansible_connection=ssh

[web:vars]
ansible_python_interpreter=/usr/bin/python3
```
We add the python interpreter to make sure we don't use older python version

* Test connectivity: ```ansible 34.227.142.155 -m ping```

* Since executing install commands on remote will require sudo priviledges, setting up our user to be in sudo group by editing visudo in host
```
---
- hosts: web
  tasks:
    - lineinfile:
        path: /etc/sudoers
        state: present
        regexp: '^%sudo'
        line: '%sudo ALL=(ALL:ALL) NOPASSWD: ALL'
        validate: 'visudo -cf %s'
```
and execute using:```ansible-playbook set_sudoer.yml -b -K```
-b flag is to become root
and -K is to provide one time auth password

* Test by installing nginx:
```
ansible-playbook nginx_install.yml -b
```
nginx should now be running in the remote server

* Final Playbook which copies custom content to the remote server and deploys nginx: ```ansible-playbook nginx.yml```
```
---
- hosts: web
  tasks:
    - name: ensure nginx is at the latest version
      apt: name=nginx state=latest
      become: yes
    - name: start nginx
      service:
          name: nginx
          state: started
      become: yes
    - name: copy the nginx config file and restart nginx
      copy:
        src: /home/cloud_user/ansible/static_site.cfg
        dest: /etc/nginx/sites-available/static_site.cfg
      become: yes
    - name: create symlink
      file:
        src: /etc/nginx/sites-available/static_site.cfg
        dest: /etc/nginx/sites-enabled/default
        state: link
      become: yes
    - name: copy the content of the web site
      copy:
        src: /home/cloud_user/static-site/
        dest: /home/cloud_user/static-site
    - name: restart nginx
      service:
        name: nginx
        state: restarted
      become: yes
```
to perform syntax sanity check use: ```ansible-playbook nginx.yml --syntax-check```

## Cron job to check if application is runnig and if not send and email

We will run a cron job which will run regularly every 5mins and check if server returns a 200 status code if not, it will send and email
server-check.py holds the python code to do that task
edit crontab and add the entry to execute the python script
```
*/5 * * * * cloud_user `/usr/bin/python3 /home/cloud_user/server-check.py &> log.out`
```
Here we run our python file every 5 mins and log its stdout and stderr to log

if cron fails check ```tail -f /var/log/syslog``` for logs
