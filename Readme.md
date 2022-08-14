# LookML Field Audit
Command line python utility for making mass field updates when a sql change on the database breaks your LookML. If
you are renaming columns on the database end, Looker doesn't automatically pick up on this and queries will break. This utility
allows you to specify a view or views and update all fields that reference a given column with the up to date name

## Dependencies
* `lookml`
* `re`
* `github`

## Requirements
A `config.yml` in the directory where you are invoking this util. Must follow this syntax:

```yml
config:
    repo: '<repo_name>'
    access_token: '<personal access token (PAT)>'
```

## Example Commands