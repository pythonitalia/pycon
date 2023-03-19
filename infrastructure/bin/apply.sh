export TF_VAR_githash_users_backend=$(git rev-list -1 HEAD -- ../users-backend/)
export TF_VAR_githash_association_backend=$(git rev-list -1 HEAD -- ../association-backend/)
export TF_VAR_githash_pycon_backend=$(git rev-list -1 HEAD -- ../backend/)
export TF_VAR_githash_cms=$(git rev-list -1 HEAD -- ../cms/)

cd azure-applications && terraform apply && cd -
