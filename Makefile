### Deploy configs

### Makefile internal coordination
flags=.makeFlags
VPATH=$(flags)

$(shell mkdir -p $(flags))

.PHONY: all clean default
define DEFAULT_TEXT
Available make rules:

eb:\tcreate AWS elasticbeanstalk application zip(found under app.publish/eb.zip after build)

endef

### Rules
export DEFAULT_TEXT

eb:
	mkdir -p app.publish
	rm -r app.publish/* || echo 'first build'
	cp -ar *.py requirements.txt flaskweb .ebextensions .platform app.publish/
	find app.publish -type f -name "*.sh" -exec chmod 0755 {} \+;	
	find app.publish -type f -name "*.sh" -exec dos2unix {} \+;
	cp -ar app.publish/.platform/hooks/postdeploy/* app.publish/.platform/confighooks/postdeploy/
	(cd app.publish && zip -r9 eb.zip .) 
