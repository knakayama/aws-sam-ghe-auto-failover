DOCKER_PATH = _YOUR_DOCKER_PATH_
S3_BUCKET = _YOUR_S3_BUCKET_
STACK_NAME = ghe-auto-failover

package:
	@[ -d .sam ] || mkdir .sam
	@aws cloudformation package \
		--template-file sam.yml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix sam/$(STACK_NAME)/`date '+%Y%m%d'` \
		--output-template-file .sam/packaged.yml

deploy:
	@if [ -f params/param.json ]; then \
		aws cloudformation deploy \
			--template-file .sam/packaged.yml \
			--stack-name $(STACK_NAME) \
			--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
			--parameter-overrides `cat params/param.json | jq -r '.Parameters | to_entries | map("\(.key)=\(.value|tostring)") | .[]' | tr '\n' ' ' | awk '{print}'` \
			--no-execute-changeset; \
	else \
		aws cloudformation deploy \
			--template-file .sam/packaged.yml \
			--stack-name $(STACK_NAME) \
			--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
			--no-execute-changeset; \
	fi

execute-changeset:
	@aws cloudformation execute-change-set \
		--stack-name $(STACK_NAME) \
		--change-set-name `aws cloudformation list-change-sets \
			--stack-name $(STACK_NAME) \
			--query 'reverse(sort_by(Summaries,&CreationTime))[0].ChangeSetName' \
			--output text`

docker-build:
	@cd src/handlers/$(DOCKER_PATH) \
		&& docker build . -t ghe-auto-failover/failover \
		&& docker run --rm -v `pwd`/vendored:/app/vendored ghe-auto-failover/failover

all: package deploy execute-changeset

.PHONY: package deploy execute-changeset docker-build all
