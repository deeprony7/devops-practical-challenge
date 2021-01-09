## Run Nginx with docker

I will use the base nginx image from dockerhub and have the default html page be mapped to custom html on localhost

```
docker run -d -p 8000:80 -v ~/static-site:/usr/share/nginx/html --name my-nginx nginx
```

So any time the code changes within static-site dir, it will reflect in the container too as `-v` flag maps host volume to container volume
