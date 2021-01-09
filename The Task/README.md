## Basic Setup

To install nginx run below commands:
```
sudo apt update
sudo apt install nginx
```

Start service with:
```systemctl start nginx```

Check status:
```systemctl status nginx```

Verify if default nginx page shows up:
```curl localhost```
This should return the HTML content of the page

To replace default page with custom content:

* Create our own configuration file:
```
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        root /home/cloud_user/static-site;
        server_name _;
        location / {
                try_files $uri $uri/ =404;
        }
}
```

* Create a directory with our custom webpage at /home/cloud_user/static-site:
```
<h1>Test page</h1>
```

* Default symlink exists from sites-enabled to sites-default configuration, we need to replace that with the one we just created:
```
cd /etc/nginx/sites-enabled
sudo rm default
sudo ln -s ../sites-available/static_site.cfg default
```

* Restart nginx and verify
```
systemctl restart nginx
curl localhost
```

This should be returning our custom webpage