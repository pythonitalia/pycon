locals {
  email_templates_path = abspath("${path.root}/../../email-templates")
  build_output_path    = "${local.email_templates_path}/build_production/"
}

resource "aws_ses_template" "template" {
  for_each = fileset(local.build_output_path, "*.html")
  name     = "pythonit-${terraform.workspace}-${replace(each.key, ".html", "")}"
  subject  = "{{subject}}"
  html     = file("${local.build_output_path}/${each.key}")
  text     = file("${local.build_output_path}/${replace(each.key, ".html", ".txt")}")
}
