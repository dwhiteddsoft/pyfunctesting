# Python Function Testing - Service Bus Testing with Containers

This directory contains a copy of the code we are using for our test. The deployment od this is araw python code in a function app backed by an App Svc plan. 

**NOTE** Keep __init__.py main processing code sync'd up with the other projects 

**DEPLOY:** Use the webappcont.svcplan.template.json (and accompanying parameters file) to deploy the infrastructure to test on. Run this command:

*az group deployment create -g (your-rg-name) --template-file webappcont.svcplan.template.json --parameters @webappcont.svcplan.parameters.json --parameters "dockerRegistryPassword=password"*
