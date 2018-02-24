Traefik Proxy Plugin for Dokku
======

### :warning: This plugin is under active development :warning:

This project is powered by [Traefik](https://traefik.io/)  
Traefik is a reverse proxy, written in Go and works seamlessly with Docker.

This makes it the perfect reverse proxy for Dokku.  
No more worries about SSL certificates, HTTPS by default.  
Scaling? No problem.  
Restarting a container? Traefik reconfigures automatically.  

Traefik also comes with a Dashboard and API, opening up possibilities that were impossible with Nginx.

This plugin pulls the Traefik docker image on install and starts Traefik.  
You will be able to find the dashboard and API at `traefik.yourdomain.tld` after installation.



### Current triggers and actions

| Trigger              | Action                       |
|:---------------------|:-----------------------------|
|`proxy-build-config`  | (Re)create the flags file    |
|`proxy-enable`        | Enable proxying for the app  |
|`proxy-disable`       | Disable proxying for the app |
|`post-domains-update` | Grab domain updates          |
|`docker-args-deploy`  | Supply the flags file        |
