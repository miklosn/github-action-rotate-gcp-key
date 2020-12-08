# github-action-rotate-gcp-key

This action rotates GCP service account keys in with the following method:

1. Create a new key for the SA
2. Update the specified Github secret (in one or more repos)
3. Delete all keys which do not equal the newly created key and which are also older than 5 minutes (to prevent race errors)

## Example workflow

```yaml

name: Rotate GCP service account key
#on:
#  schedule:
#    - cron: '0 12 * * 1'
on: [workflow_dispatch]
jobs:
  rotate:
    name: rotate gcp key
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2.0.0
      - name: Setup GCP Service Account
        uses: google-github-actions/setup-gcloud@master
        with:
          service_account_key: ${{ secrets.GCP_SA_INFRA_KEY }}
          export_default_credentials: true
      - name: rotate gcp keys
        uses: miklosn/github-action-rotate-gcp-key@main
        with:
          projectId: "example"
          serviceAccount: "github-actions@example.iam.gserviceaccount.com"
          personalAccessToken: "${{ secrets.PERSONAL_ACCESS_TOKEN }}"
          repositories: ${{ github.repository }}
          secretName: "GCP_SA_INFRA_KEY"
```

## Inputs


projectId: GCP project id to operate on

serviceAccount: e-mail ID of the service account to operate on

personalAccessToken: github token with permission to add/update secrets on a repo basis

secretName: name of the Github secret to update

repositories: one or multiple github repos. If multiple repos are specified they need to be separated by commas. 
The secret will be updated in all repos.

