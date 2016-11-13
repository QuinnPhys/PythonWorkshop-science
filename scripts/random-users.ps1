#!/usr/bin/env powershell

[cmdletbinding(SupportsShouldProcess=$true,ConfirmImpact="High")]
param(
    [string] $BaseName="epqistmp",
    [int] $Number = 40,
    [string] $JobName = "password-tickets",
    [string] $OutputDirectory = ".",
    [string] $DefaultShell = "/bin/bash"
)

function New-RandomUser {
    [cmdletbinding(SupportsShouldProcess=$true,ConfirmImpact="High")]
    param(
        [Parameter(ValueFromPipeline)]
        [string] $UserName,

        [int] $Length = 12,
        [string] $DefaultShell = "/bin/bash"
    );

    process {

        $password = apg -a 1 -n 1 -MLCN -m $Length -x $Length

        if ($PSCmdlet.ShouldProcess((hostname), "Create new user $UserName")) {
            useradd $UserName --create-home
            if (-not $?) {
                throw [System.Exception] "useradd failed."
            }

            echo ${UserName}:${password} | chpasswd
            if (-not $?) {
                throw [System.Exception] "chpasswd failed."
            }

            chsh $UserName -s $DefaultShell
            if (-not $?) {
                throw [System.Exception] "chsh failed."
            }
        } else {
            Write-Host "useradd" $UserName --create-home
            Write-Host "echo" ${UserName}:${password} "| chpasswd"
            Write-Host "chsh $UserName -s $DefaultShell"
        }

        Write-Output (New-Object -TypeName psobject -Prop (@{ UserName = $UserName; Password = $password }));

    }

}

function Get-UserNames {
    param(
        [string] $BaseName = "tmpuser",
        [int] $Number = 1
    )

    foreach ($idx in 1..$Number) {
        Write-Output "$BaseName$idx"
    }
}

function Get-FakeUsers {
    Write-Output (New-Object -TypeName psobject -Prop (
        @{ UserName = "foo"; Password = "f00" }
    ))
    Write-Output (New-Object -TypeName psobject -Prop (
        @{ UserName = "bar"; Password = "b4r" }
    ))
}

function Format-UsersAsLaTeX {
    param(
        [Parameter(ValueFromPipelineByPropertyName=$true)]
        [string]
        $UserName,

        [Parameter(ValueFromPipelineByPropertyName=$true)]
        [string]
        $Password
    )

    begin {
        Write-Output @"
\documentclass{article}
\usepackage{fontspec}
    \setmainfont{Palatino Linotype}
\usepackage{sourcecodepro}
\usepackage[flashCard,circlemark]{ticket}

\renewcommand{\ticketdefault}{%no background
}

\newcommand{\userpass}[2]{\ticket{%
    \put( 8,20){User:}%
    \put(18,20){\sourcecodepro{#1}}%
    \put( 8,16){Pass:}%
    \put(18,16){\sourcecodepro{#2}}%
}}
\begin{document}
"@
    }

    process {
        Write-Output ("\userpass{{{0}}}{{{1}}}" -f $UserName, $Password);
    }

    end {
        Write-Output @"
\end{document}
"@
    }

}

$conf = @{ Confirm = $ConfirmPreference -eq "High" }
Get-UserNames -BaseName $BaseName -Number $Number | New-RandomUser @conf | Format-UsersAsLaTeX | xelatex -jobname="$JobName" -output-directory="$OutputDirectory"
