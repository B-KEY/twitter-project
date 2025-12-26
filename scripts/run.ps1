param(
    [Parameter(Mandatory=$true)][string]$TweetUrl
)

$script = Join-Path $PSScriptRoot "..\src\working_twitter_automation.py"
python $script $TweetUrl
