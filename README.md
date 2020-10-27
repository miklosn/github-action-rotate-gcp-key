# github-action-rotate-gcp-key

This action rotates GCP service accounts in with the following method:

1. Create a new key
2. Update the specified Github secret (in one or more repos)
3. Delete all keys which do not equal the newly created key and which are also older than 1 minute (to prevent race errors)

## Input env vars

GOOGLE_APPLICATION_CREDENTIALS: not strictly required, it just needs a configured ADC env

PROJECT_ID: GCP project id to operate on

SERVICE_ACCOUNT: e-mail ID of the service account to operate on

PERSONAL_ACCESS_TOKEN: github token with permission to add/update secrets on a repo basis

GITHUB_SECRET_NAME: name of the Github secret to update

OWNER_REPOSITORY: one or multiple github repos. If multiple repos are specified they need to be separated by commas. 
The secret will be updated in all repos.

## Example workflow

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
      - name: Configure GCP credentials
        run: |
          echo -n ${{ secrets.GCP_SA_INFRA_KEY }} | base64 --decode > "${GITHUB_WORKSPACE}/infra.json"
          ls -la ${GITHUB_WORKSPACE}
      - name: rotate gcp keys
        uses: miklosn/github-action-rotate-gcp-key@v1.0
        env:
          PERSONAL_ACCESS_TOKEN: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
          PROJECT_ID: "example"
          OWNER_REPOSITORY: ${{ github.repository }}
          GOOGLE_APPLICATION_CREDENTIALS: "${{ github.workspace }}/infra.json"
          GITHUB_SECRET_NAME: "GCP_SA_INFRA_KEY"
          SERVICE_ACCOUNT: "github-actions@example.iam.gserviceaccount.com"

 