FROM hashicorp/terraform:0.12.6

LABEL "com.github.actions.name"="terraform plan"
LABEL "com.github.actions.description"="Run terraform plan"
LABEL "com.github.actions.icon"="book-open"
LABEL "com.github.actions.color"="purple"

LABEL "repository"="https://github.com/hashicorp/terraform-github-actions"
LABEL "homepage"="http://github.com/hashicorp/terraform-github-actions"
LABEL "maintainer"="HashiCorp Terraform Team <terraform@hashicorp.com>"

RUN apk --no-cache add jq curl
RUN curl -L https://github.com/cloudposse/tfmask/releases/download/0.2.0/tfmask_linux_amd64 -o /usr/bin/tfmask
RUN chmod +x /usr/bin/tfmask

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
