function New-RandomUser {
    param(
        [Parameter(ValueFromPipeline)]
        [string] $UserName,

        [int] $Length = 12,

        [switch] $WhatIf
    );

    process {

        $password = apg -a 1 -n 1 -MLCN -m $Length -x $Length

        if (-not $WhatIf) {
            useradd $UserName --create-home
            echo ${UserName}:${password} | chpasswd
        } else {
            Write-Host "useradd" $UserName --create-home
            Write-Host "echo" ${UserName}:${password} "| chpasswd"
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
\usepackage{mathpazo}
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

Get-UserNames -BaseName epqistmp -Number 40 | New-RandomUser | Format-UsersAsLaTeX | xelatex -job-name=password-tickets
