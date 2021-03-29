# flaskweb
This is a simple python flask web project with AWS elastic beanstalk support(in particular SSL via letsencrypt). 

It is intended for small development shop who don't want/like to spend time on more complicated DevOps like Ansible/Jenkins/Docker/Kubernetes etc.

The focus is not really about python/flask but more about how to deploy a flask project to elastic beanstalk(all with a single zip file).

Under linux/OS X, 'make eb' would generate a zip file which can be uploaded via AWS console(you have to create the eb environment via other means)

Under Windows, it can be published using VS 2019(which is my development environment) or make use of WSL 1(to build it just like linux). WSL is the preferred way as that would set up proper execution bits(chmod) and turn scripts in CRLF(under windows) into sh friendly file.

The initial deployment would create the EB environment with unfilled parameters which can then be manually changed via the AWS console(runtime setup). Alternatively, change the config file under .ebextensions before build if they are known before hand.

If enabled(CERT_xxx), it would automatically setup letsencrypt using the defined domain.

By default(CERT_TYPE = None), it would only use a stub cert(and would not do forced http->https redirect, but https:// is working but with cert warning obvious). Setting it to 'testing' would aquire a testing cert by letsenrypt(use this to test the flow). 'production' would acquire proper cert. Be warned that letsencrypt has a limit on how many cert per week(20 for production) so if you don't use your own domain and just the default .elasticbeanstalk.com one, it may not work if many people are doing the same thing

If the production cert is acquired, it would setup the periodic renew cronjob as well.

The setup also work for HA(i.e. behind ELB) but one has to manually setup the listener for port 443 ELB(as it needs cert from AWS cert manager). There is a helper script which would acquire the production cert from letsencrypt and upload it to AWS cert manager which can then be bound to the ELB. Note that AWS also has a limit on how many upload/import one can do within a year(so don't do this often for testing or it would hit the limit).

For those that must use ELB, ideally just let AWS do the cert issuing via the AWS cert manager, if you need custom domain rather than just the .ealsticbeanstalk.com(which you cannot control and must be through the letsencrypt way)

If you are interested in nodejs, I have a nodejs version here(which I need for running my own walletconnect bridge). That is an interesting one as it use websocket so allows me to test out the ELB -> nginx -> nodejs in websocket scenario.

https://github.com/garyng2000/node-walletconnect-bridge
