# HOW TO USE:
# Reference: https://developer.cisco.com/meraki/api/#!introduction

# 1. Within AD, set each computer account's ManagedBy attribute to the user account that the device is assigned to.
# 2. Find your Network ID. I'm not sure where this is, probably on the dashboard web page or in your settings online.
# 3. Create an API Key. Instructions can be found in the reference documentation linked above.
# 4. Find out what policy type your clients use within Meraki. You will need to make sure Set-MerakiClientName's "DevicePolicyType" parameter is set properly!
# 5. Install this powershell module by:
    # a) Create a folder in %ProgramFiles%\WindowsPowerShell\Modules with the name 'MerakiAPIDescriptionUpdater'
    # b) Copy this psm1 file into the directory you just created. The file name and the folder name must match!
# 6. Open a PowerShell window and run the command 'Sync-MerakiClientOwners -Token {your token here} -NetworkID {your network id here}'
# 7. If you have issue or anything to add, please leave a comment on my github under the reddit-help repo: https://github.com/SnoozingPinata/reddit-help

function Get-MerakiNetworkClients {
    Param (
        [cmdletbinding]

        [Parameter(
            Mandatory=$true,
            ValueFromPipelineByPropertyName=$true,
            Position=0
        )]
        [string] $Token,

        [Parameter(
            Mandatory=$true,
            ValueFromPipelineByPropertyName=$true,
            Position=1
        )]
        [string] $NetworkID
    )

    Begin {
        $baseUrl = 'https://api.meraki.com/api/v0/networks/'
        $urlEnding = '/clients'
        $url = $baseUrl + $NetworkID + $urlEnding
        Write-Debug "URL: $($url)"

        $header = [ordered]@{
            Content-Type = 'application/json';
            Accept = 'application/json';
            X-Cisco-Meraki-API-Key = '$Token'
        }
        $convertedHeader = ConvertTo-Json -InputObject $header

        Write-Debug "Header: $($header)"
        Write-Debug "Converted Header: $($convertedHeader)"
    }

    Process {
        $response = Invoke-WebRequest -Method GET -URI $url -Headers $convertedHeader
        return $response
    }
}

# I don't know for sure if this will update the Name attribute on the client. 
# I don't see a way to update it in the API documentation but it's a post request and the name value is not required so it's likely it will update the value.
function Set-MerakiClientName {
    Param (
        [cmdletbinding]

        [Parameter(
            Mandatory=$true,
            ValueFromPipelineByPropertyName=$true,
            Position=0
        )]
        [string] $Token,

        [Parameter(
            Mandatory=$true,
            ValueFromPipelineByPropertyName=$true,
            Position=1
        )]
        [string] $NetworkID,

        [Parameter(
            Mandatory=$true,
            ValueFromPipelineByPropertyName=$true,
            Position=2
        )]
        [string] $Name,

        [Parameter(
            Mandatory=$true,
            ValueFromPipelineByPropertyName=$true,
            Position=3
        )]
        [string] $MacAddress,

        [Parameter(
            ValueFromPipelineByPropertyName=$true,
            Position=4
        )]
        [ValidateSetAttribute("Normal","Group policy","Whitelisted","Blocked","Per connection")]
        [string] $DevicePolicyType = 'Normal',

        [Parameter(
            ValueFromPipelineByPropertyName=$true,
            Position=5
        )]
        [string] $GroupPolicyId
    )

    Begin {
        $baseUrl = 'https://api.meraki.com/api/v0/networks/'
        $urlEnding = '/clients/provision'
        $url = $baseUrl + $NetworkID + $urlEnding
        Write-Debug "URL: $($url)"

        $header = [ordered]@{
            Content-Type = 'application/json';
            Accept = 'application/json';
            X-Cisco-Meraki-API-Key = '$Token'
        }
        $convertedHeader = ConvertTo-Json -InputObject $header

        Write-Debug "Header: $($header)"
        Write-Debug "Converted Header: $($convertedHeader)"
    }

    Process {
        $body = [ordered]@{
            mac = "$($MacAddress)";
            name = "$($Name)";
            devicePolicy = "$($DevicePolicyType)";
            groupPolicyId = "$($GroupPolicyId)"
        }
        $convertedBody = ConvertTo-Json -InputObject $body

        $response = Invoke-WebRequest -Method POST -URI $url -Headers $convertedHeader -Body $convertedBody
        return $response
    }
}

function Get-ComputerAssignment {
    <#
        .SYNOPSIS
        Returns the name of each computer that is assigned to a user or returns all unassigned computers.
        .DESCRIPTION
        Returns the name of each computer that is assigned to a user or returns all unassigned computers. 
        Either Username must be defined or Unassigned must be used. 
        .PARAMETER UserName
        Returns all computers that are set as managed by for the user. 
        .PARAMETER Unassigned
        Switch: Returns the name of all enabled computers that do not have a value in the "ManagedBy" attribute.
        .INPUTS
        UserName accepts input from pipeline.
        .OUTPUTS
        Writes the name of the computer object.
        If called without defining the username or using the unassigned switch, returns a hash table of each computer's hostname as the key and the ManagedBy attribute as the value.
        .EXAMPLE
        Get-ComputerAssignment -Unassigned
        SpareComputer01
        .EXAMPLE
        Get-ComputerAssignment -UserName HWallace
        Desktop-HWallace
        .LINK
        Github source: https://github.com/SnoozingPinata/SamsADToolkit
        .LINK
        Author's website: www.samuelmelton.com
    #>

    [CmdletBinding()]
    Param (
        [Parameter(
            Position=0,
            ValueFromPipeline=$true)]
        [string[]] $UserName,

        [Parameter(
            Position=1)]
        [switch] $Unassigned
    )

    Begin {
    }

    Process {
        if ($Unassigned) {
            Get-ADComputer -Filter "Enabled -eq '$true'" -Properties ManagedBy | ForEach-Object -Process {
                If ($null -eq $_.ManagedBy) {
                    Write-Output $_.Name
                }
            }
        } elseif ($UserName){
            (Get-ADComputer -Filter "ManagedBy -eq '$UserName'").Name
        } else {
            $returnHash = @{}

            Get-ADComputer -Filter "Enabled -eq '$true'" -Properties ManagedBy | ForEach-Object -Process {
                $returnHash.Add($_.Name, $_.ManagedBy)
            }
            return $returnHash
        }
    }

    End {
    }
}

function Sync-MerakiClientOwners {
    Param (
        [cmdletbinding]

        [Parameter(
            Mandatory=$true,
            ValueFromPipelineByPropertyName=$true,
            Position=0
        )]
        [string] $Token,

        [Parameter(
            Mandatory=$true,
            ValueFromPipelineByPropertyName=$true,
            Position=1
        )]
        [string] $NetworkID
    )

    Process {
        $allClients = Get-MerakiNetworkClients -Token $Token -NetworkId $NetworkID

        foreach ($client in $allClients) {
            if ($null -ne $($client.id)) {
                $ownerName = Get-ComputerAssignment -UserName ($client.id)
                if ($null -ne $ownerName) {
                    Set-MerakiClientDescription -Token $Token -NetworkId $NetworkID -Name $ownerName -MacAddress ($client.mac)
                }
            }
        }
    }
}